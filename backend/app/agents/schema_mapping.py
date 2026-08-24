"""Agent 2: Context-Aware Schema Mapping Agent (Google ADK)."""

from typing import Dict, Any, List, Tuple
from google.adk.agents import LlmAgent
from app.agents.adk_agents import build_schema_mapping_agent
from app.agents.tools import map_columns_to_schema


class SchemaMappingAgent:
    def __init__(self) -> None:
        self.name = "SchemaMappingAgent"
        self.adk_agent: LlmAgent = build_schema_mapping_agent()

    async def map_columns(
        self, client_id: str, extracted_columns: List[str]
    ) -> Tuple[Dict[str, str], List[Dict[str, Any]]]:
        """Map raw columns to Uniplexity ERP schema; generate clarification triggers if ambiguous."""
        result = map_columns_to_schema(client_id, extracted_columns)
        return result["mappings"], result["clarifications"]
