"""Agent 1: Multimodal Document Understanding Agent (Google ADK)."""

from typing import Dict, Any
from google.adk.agents import LlmAgent
from app.agents.adk_agents import build_document_understanding_agent
from app.agents.tools import extract_document_columns, extract_raw_records
from app.models.schemas import DocumentType


class DocumentUnderstandingAgent:
    def __init__(self) -> None:
        self.name = "DocumentUnderstandingAgent"
        self.adk_agent: LlmAgent = build_document_understanding_agent()

    async def process_document(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """Extract text, tables, column headers, and document classification."""
        columns = extract_document_columns(file_path, file_type)
        raw_records = extract_raw_records(file_path, file_type)
        return {
            "document_type": DocumentType(columns["document_type"]),
            "detected_columns": columns["detected_columns"],
            "raw_records": raw_records,
            "confidence_score": columns["confidence_score"],
        }
