"""Google ADK Migration Pipeline Orchestrator."""

from typing import Dict, Any
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

    async def run_document_job(self, job_id: str, client_id: str, file_path: str, file_type: str) -> Dict[str, Any]:
        """Execute full sequential pipeline for a single document."""
        doc_result = await self.doc_agent.process_document(file_path, file_type)
        mappings, clarifications = await self.schema_agent.map_columns(client_id, doc_result["detected_columns"])
        clean_records, anomalies = await self.cleaning_agent.clean_and_normalize(doc_result["raw_records"], mappings)
        preview = await self.validation_agent.generate_preview(job_id, clean_records, anomalies)
        
        return {
            "doc_result": doc_result,
            "mappings": mappings,
            "clarifications": clarifications,
            "clean_records": clean_records,
            "anomalies": anomalies,
            "preview": preview,
        }

migration_pipeline = MigrationPipeline()
