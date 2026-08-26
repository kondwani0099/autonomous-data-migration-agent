"""Document parser service for extracting tabular data from various file types.

Supports:
- CSV: pandas
- Excel (.xlsx): pandas + openpyxl
- PDF: pdfplumber (table extraction)
- Images (.png, .jpg, .jpeg): Gemini Vision API for table/text extraction
"""

from __future__ import annotations

import io
import os
from typing import Any, Dict, List, Optional

import pandas as pd
import pdfplumber
from PIL import Image

from app.core.config import settings


class DocumentParser:
    """Parse documents and extract tabular data."""

    SUPPORTED_EXTENSIONS = {
        "csv": "csv",
        "xlsx": "excel",
        "xls": "excel",
        "pdf": "pdf",
        "png": "image",
        "jpg": "image",
        "jpeg": "image",
    }

    def __init__(self) -> None:
        self._gemini_client: Optional[Any] = None
        if settings.GEMINI_API_KEY and not settings.MOCK_GCP:
            from google import genai
            self._gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def get_file_type(self, file_ext: str) -> str:
        """Get the parser type for a file extension."""
        return self.SUPPORTED_EXTENSIONS.get(file_ext.lower(), "unknown")

    def parse_csv(self, file_data: bytes) -> Dict[str, Any]:
        """Parse CSV file and extract columns + records."""
        df = pd.read_csv(io.BytesIO(file_data))
        columns = df.columns.tolist()
        records = df.where(df.notnull(), None).to_dict(orient="records")
        # Convert numpy types to Python native types
        records = self._serialize_records(records)
        return {
            "detected_columns": columns,
            "raw_records": records,
            "confidence_score": 0.95,
            "total_records": len(records),
        }

    def parse_excel(self, file_data: bytes) -> Dict[str, Any]:
        """Parse Excel file and extract columns + records from first sheet."""
        df = pd.read_excel(io.BytesIO(file_data), engine="openpyxl")
        columns = df.columns.tolist()
        records = df.where(df.notnull(), None).to_dict(orient="records")
        records = self._serialize_records(records)
        return {
            "detected_columns": columns,
            "raw_records": records,
            "confidence_score": 0.95,
            "total_records": len(records),
        }

    def parse_pdf(self, file_data: bytes) -> Dict[str, Any]:
        """Parse PDF and extract tables using pdfplumber."""
        all_records: List[Dict[str, Any]] = []
        all_columns: List[str] = []

        with pdfplumber.open(io.BytesIO(file_data)) as pdf:
            for i, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                if not tables:
                    continue

                for table in tables:
                    if not table:
                        continue

                    # First row is typically headers
                    headers = [str(cell).strip() if cell else f"column_{j}" for j, cell in enumerate(table[0])]
                    data_rows = table[1:] if len(table) > 1 else []

                    for row in data_rows:
                        record = {}
                        for j, header in enumerate(headers):
                            if j < len(row):
                                record[header] = str(row[j]).strip() if row[j] else None
                        if record:
                            all_records.append(record)

                    if not all_columns:
                        all_columns = headers

        # Collect all unique columns
        if all_records and not all_columns:
            all_columns = list(all_records[0].keys())

        return {
            "detected_columns": all_columns,
            "raw_records": all_records,
            "confidence_score": 0.85,
            "total_records": len(all_records),
        }

    async def parse_image(self, file_data: bytes) -> Dict[str, Any]:
        """Parse image using Gemini Vision API to extract table/text data."""
        if not self._gemini_client:
            return {
                "detected_columns": [],
                "raw_records": [],
                "confidence_score": 0.0,
                "total_records": 0,
                "error": "GEMINI_API_KEY not configured",
            }

        try:
            # Validate image
            image = Image.open(io.BytesIO(file_data))
            image.verify()
            # Re-open after verify
            image = Image.open(io.BytesIO(file_data))

            # Get file extension
            mime_type = "image/png" if image.format == "PNG" else "image/jpeg"

            from google.genai.types import Part, HttpOptions

            part = Part.from_bytes(data=file_data, mime_type=mime_type)

            prompt = """Extract all tabular data from this image. 
            Return the data in a structured format:
            1. First identify all column headers
            2. Then list each row of data under the correct columns
            
            If this is a handwritten ledger, do your best to interpret the handwriting.
            Return ONLY a JSON object with this structure:
            {
              "columns": ["col1", "col2", ...],
              "records": [{"col1": "val1", "col2": "val2"}, ...]
            }"""

            response = self._gemini_client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[prompt, part],
                config={"http_options": HttpOptions(api_version="v1alpha", api_version_fallback=False)},
            )

            import json
            import re

            text = response.text

            # Extract JSON from response (handle markdown code blocks)
            json_match = re.search(r'\{[\s\S]*"columns"[\s\S]*\}', text)
            if json_match:
                data = json.loads(json_match.group())
                columns = data.get("columns", [])
                records = data.get("records", [])
                return {
                    "detected_columns": columns,
                    "raw_records": records,
                    "confidence_score": 0.80,
                    "total_records": len(records),
                }

            # Fallback: return empty with the raw text
            return {
                "detected_columns": [],
                "raw_records": [],
                "confidence_score": 0.3,
                "total_records": 0,
                "extracted_text": text,
            }

        except Exception as e:
            return {
                "detected_columns": [],
                "raw_records": [],
                "confidence_score": 0.0,
                "total_records": 0,
                "error": str(e),
            }

    def parse_document(self, file_data: bytes, file_ext: str) -> Dict[str, Any]:
        """Parse a document based on its extension. Returns sync result."""
        file_type = self.get_file_type(file_ext)

        if file_type == "csv":
            return self.parse_csv(file_data)
        elif file_type == "excel":
            return self.parse_excel(file_data)
        elif file_type == "pdf":
            return self.parse_pdf(file_data)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")

    async def parse_document_async(self, file_data: bytes, file_ext: str) -> Dict[str, Any]:
        """Parse a document based on its extension. Handles async (images)."""
        file_type = self.get_file_type(file_ext)

        if file_type == "image":
            return await self.parse_image(file_data)
        else:
            return self.parse_document(file_data, file_ext)

    @staticmethod
    def _serialize_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert numpy/pandas types to Python native types for JSON serialization."""
        import numpy as np

        serialized = []
        for record in records:
            new_record = {}
            for key, value in record.items():
                if isinstance(value, (np.integer,)):
                    new_record[key] = int(value)
                elif isinstance(value, (np.floating,)):
                    new_record[key] = float(value)
                elif isinstance(value, np.ndarray):
                    new_record[key] = value.tolist()
                elif pd.isna(value):
                    new_record[key] = None
                else:
                    new_record[key] = value
            serialized.append(new_record)
        return serialized


document_parser = DocumentParser()