"""Google ADK Migration Pipeline Orchestrator.

Runs the four pipeline agents sequentially via ADK ``Runner`` with
``InMemorySessionService``, following the reference article
"Building AI Agents with Google ADK, FastAPI, and MCP".
"""

from typing import Dict, Any
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agents.adk_agents import build_all_agents
from app.agents.document_understanding import DocumentUnderstandingAgent
from app.agents.schema_mapping import SchemaMappingAgent
from app.agents.data_cleaning import DataCleaningAgent
from app.agents.validation_import import ValidationImportAgent


class MigrationPipeline:
    def __init__(self) -> None:
        self.doc_agent = DocumentUnderstandingAgent()
        self.schema_agent = SchemaMappingAgent()
        self.cleaning_agent = DataCleaningAgent()
        self.validation_agent = ValidationImportAgent()

        # Build ADK agents for Runner-based execution
        self.adk_agents = build_all_agents()
        self._runners: Dict[str, Runner] = {}
        self._session_service = InMemorySessionService()

        # Pre-build runners for each agent
        for key, agent in self.adk_agents.items():
            self._runners[key] = Runner(
                app_name=agent.name or key,
                agent=agent,
                session_service=self._session_service,
            )

    async def _run_adk_agent(
        self, agent_key: str, request: str
    ) -> str:
        """Run a single ADK agent via Runner and return the final text."""
        runner = self._runners[agent_key]
        session = await self._session_service.create_session(
            app_name=runner.app_name, user_id="pipeline"
        )
        final_text = ""
        async for event in runner.run_async(
            user_id="pipeline",
            session_id=session.id,
            new_message=types.Content(role="user", parts=[types.Part(text=request)]),
        ):
            if event.is_final_response() and event.content:
                for part in event.content.parts:
                    if part.text:
                        final_text += part.text
        return final_text

    async def run_document_job(
        self,
        job_id: str,
        client_id: str,
        file_path: str,
        file_type: str,
        data_category: str = "sales",
    ) -> Dict[str, Any]:
        """Execute full sequential pipeline for a single document."""
        doc_result = await self.doc_agent.process_document(file_path, file_type)
        mappings, clarifications = await self.schema_agent.map_columns(
            client_id, doc_result["detected_columns"], data_category
        )
        clean_records, anomalies = await self.cleaning_agent.clean_and_normalize(
            doc_result["raw_records"], mappings, data_category
        )
        preview = await self.validation_agent.generate_preview(
            job_id, clean_records, anomalies
        )

        return {
            "doc_result": doc_result,
            "mappings": mappings,
            "clarifications": clarifications,
            "clean_records": clean_records,
            "anomalies": anomalies,
            "preview": preview,
        }


migration_pipeline = MigrationPipeline()
