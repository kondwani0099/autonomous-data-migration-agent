"""Shared ADK tool functions for the Uniplexity migration agent swarm.

Each function is a plain Python callable with type hints, designed to be
wrapped in a ``google.adk.tools.FunctionTool`` and attached to an
``LlmAgent``. This mirrors the pattern from the reference article
"Building AI Agents with Google ADK, FastAPI, and MCP".
"""

from __future__ import annotations

import datetime
from typing import Any, Dict, List, Tuple

from app.models.schemas import DataAnomaly, DocumentType


# ---------------------------------------------------------------------------
# Agent 1: Document Understanding tools
# ---------------------------------------------------------------------------
def extract_document_columns(file_path: str, file_type: str) -> Dict[str, Any]:
    """Extract column headers and classify a legacy document.

    Args:
        file_path: Path or GCS URI of the uploaded document.
        file_type: MIME/extension type (e.g. 'csv', 'xlsx', 'pdf', 'png').

    Returns:
        A dict with ``document_type``, ``detected_columns``, and
        ``confidence_score``.
    """
    # In production this would call Gemini multimodal understanding.
    # Here we return a deterministic mock for the sales-ledger sample.
    return {
        "document_type": DocumentType.SALES_LEDGER.value,
        "detected_columns": ["Date", "Cust", "Prod", "Qt.", "Price", "Total"],
        "confidence_score": 0.92,
    }


def extract_raw_records(file_path: str, file_type: str) -> List[Dict[str, Any]]:
    """Extract raw tabular records from a legacy document.

    Args:
        file_path: Path or GCS URI of the uploaded document.
        file_type: MIME/extension type.

    Returns:
        A list of raw record dicts keyed by the detected column headers.
    """
    return [
        {"Date": "01/15/24", "Cust": "ABC Store", "Prod": "Coke 330ml", "Qt.": "10", "Price": "1.50", "Total": "15.00"},
        {"Date": "01/15/24", "Cust": "ABC Store", "Prod": "Coca-Cola", "Qt.": "5", "Price": "1.50", "Total": "7.50"},
        {"Date": "01/16/24", "Cust": "XYZ Market", "Prod": "Bred", "Qt.": "20", "Price": "2.00", "Total": "40.00"},
    ]


# ---------------------------------------------------------------------------
# Agent 2: Schema Mapping tools
# ---------------------------------------------------------------------------
def map_columns_to_schema(
    client_id: str, extracted_columns: List[str]
) -> Dict[str, Any]:
    """Map raw ledger columns to the Uniplexity ERP schema.

    Args:
        client_id: Target client identifier.
        extracted_columns: Column headers detected by the document agent.

    Returns:
        A dict with ``mappings`` (raw -> canonical) and ``clarifications``
        (list of human-in-the-loop questions when confidence is low).
    """
    mappings = {
        "Date": "sale_date",
        "Cust": "customer_name",
        "Prod": "product_name",
        "Qt.": "quantity",
        "Price": "unit_price",
        "Total": "total_amount",
    }

    clarifications = [
        {
            "question": "What does 'Qt.' mean in this ledger context?",
            "options": ["Quantity", "Quarts (Volume)", "Other"],
            "context": "Column 'Qt.' found near 'Price' and 'Total'",
            "agent": "SchemaMappingAgent",
        }
    ]
    return {"mappings": mappings, "clarifications": clarifications}


# ---------------------------------------------------------------------------
# Agent 3: Data Cleaning & Normalization tools
# ---------------------------------------------------------------------------
def normalize_product_name(product_name: str) -> str:
    """Normalize product name variants to a canonical form."""
    variants = {
        "Coke 330ml": "Coca-Cola",
        "Coke": "Coca-Cola",
        "Bred": "Sliced Bread",
    }
    return variants.get(product_name, product_name)


def normalize_date(raw_date: str) -> str:
    """Convert a legacy date string to ISO 8601 (YYYY-MM-DD)."""
    if "/" in raw_date:
        parts = raw_date.split("/")
        if len(parts) == 3:
            try:
                return f"20{parts[2]}-{int(parts[0]):02d}-{int(parts[1]):02d}"
            except ValueError:
                return raw_date
    return raw_date


def clean_and_normalize_records(
    raw_records: List[Dict[str, Any]], column_mappings: Dict[str, str]
) -> Dict[str, Any]:
    """Normalize values, standardize dates, and flag anomalies.

    Args:
        raw_records: Records as extracted by the document agent.
        column_mappings: Raw -> canonical column mapping.

    Returns:
        A dict with ``clean_records`` and ``anomalies``.
    """
    clean_records: List[Dict[str, Any]] = []
    anomalies: List[Dict[str, Any]] = []

    for idx, rec in enumerate(raw_records):
        mapped_row = {column_mappings.get(k, k): v for k, v in rec.items()}

        # Normalize product names
        prod = mapped_row.get("product_name", "")
        mapped_row["product_name"] = normalize_product_name(prod)

        # Normalize dates
        raw_date = mapped_row.get("sale_date", "")
        mapped_row["sale_date"] = normalize_date(raw_date)

        # Flag numeric anomalies
        try:
            qty = int(mapped_row.get("quantity", 0))
            if qty <= 0:
                anomalies.append(
                    {
                        "record_index": idx,
                        "field": "quantity",
                        "reason": "Non-positive quantity",
                        "severity": "error",
                        "value": mapped_row.get("quantity"),
                    }
                )
        except (TypeError, ValueError):
            anomalies.append(
                {
                    "record_index": idx,
                    "field": "quantity",
                    "reason": "Non-numeric quantity",
                    "severity": "error",
                    "value": mapped_row.get("quantity"),
                }
            )

        clean_records.append(mapped_row)

    return {"clean_records": clean_records, "anomalies": anomalies}


# ---------------------------------------------------------------------------
# Agent 4: Validation & Import tools
# ---------------------------------------------------------------------------
def generate_dry_run_preview(
    job_id: str, clean_records: List[Dict[str, Any]], anomalies: List[DataAnomaly]
) -> Dict[str, Any]:
    """Generate a dry-run preview before human approval."""
    return {
        "job_id": job_id,
        "total_records": len(clean_records),
        "clean_count": len(clean_records) - len(anomalies),
        "anomalies": [a.model_dump() if hasattr(a, "model_dump") else a for a in anomalies],
        "sample_records": clean_records[:50],
        "audit_trail": [],
    }


def commit_records_to_erp(
    job_id: str, clean_records: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Commit validated records to the target Uniplexity ERP database."""
    return {"job_id": job_id, "imported_records": len(clean_records)}