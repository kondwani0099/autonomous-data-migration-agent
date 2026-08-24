"""Agent 4: Validation & Import Agent (Google ADK)."""

from typing import Dict, Any, List
from google.adk.agents import LlmAgent
from app.agents.adk_agents import build_validation_import_agent
from app.agents.tools import generate_dry_run_preview, commit_records_to_erp
from app.models.schemas import DataPreview, DataAnomaly


class ValidationImportAgent:
    def __init__(self) -> None:
        self.name = "ValidationImportAgent"
        self.adk_agent: LlmAgent = build_validation_import_agent()

    async def generate_preview(
        self, job_id: str, clean_records: List[Dict[str, Any]], anomalies: List[DataAnomaly]
    ) -> DataPreview:
        """Generate dry-run preview before human approval."""
        result = generate_dry_run_preview(job_id, clean_records, anomalies)
        return DataPreview(**result)

    async def commit_import(self, job_id: str, clean_records: List[Dict[str, Any]]) -> int:
        """Commit validated records to target Uniplexity ERP database."""
        result = commit_records_to_erp(job_id, clean_records)
        return result["imported_records"]
