"""Agent 3: Data Cleaning, Normalization & Anomaly Detection Agent (Google ADK)."""

from typing import Dict, Any, List, Tuple
from google.adk.agents import LlmAgent
from app.agents.adk_agents import build_data_cleaning_agent
from app.agents.tools import clean_and_normalize_records
from app.models.schemas import DataAnomaly


class DataCleaningAgent:
    def __init__(self) -> None:
        self.name = "DataCleaningAgent"
        self.adk_agent: LlmAgent = build_data_cleaning_agent()

    async def clean_and_normalize(
        self, raw_records: List[Dict[str, Any]], column_mappings: Dict[str, str]
    ) -> Tuple[List[Dict[str, Any]], List[DataAnomaly]]:
        """Normalize values, standardize dates, group product variants, flag anomalies."""
        result = clean_and_normalize_records(raw_records, column_mappings)
        anomalies = [
            DataAnomaly(**a) if isinstance(a, dict) else a
            for a in result["anomalies"]
        ]
        return result["clean_records"], anomalies
