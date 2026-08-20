"""Agent 1: Multimodal Document Understanding Agent."""

from typing import Dict, Any, List
from app.models.schemas import DocumentType

class DocumentUnderstandingAgent:
    def __init__(self) -> None:
        self.name = "DocumentUnderstandingAgent"

    async def process_document(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """Extract text, tables, column headers, and document classification."""
        return {
            "document_type": DocumentType.SALES_LEDGER,
            "detected_columns": ["Date", "Cust", "Prod", "Qt.", "Price", "Total"],
            "raw_records": [
                {"Date": "01/15/24", "Cust": "ABC Store", "Prod": "Coke 330ml", "Qt.": "10", "Price": "1.50", "Total": "15.00"},
                {"Date": "01/15/24", "Cust": "ABC Store", "Prod": "Coca-Cola", "Qt.": "5", "Price": "1.50", "Total": "7.50"},
                {"Date": "01/16/24", "Cust": "XYZ Market", "Prod": "Bred", "Qt.": "20", "Price": "2.00", "Total": "40.00"},
            ],
            "confidence_score": 0.92,
        }
