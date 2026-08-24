"""ADK agent factory for the Uniplexity migration agent swarm.

Builds each pipeline stage as a ``google.adk.agents.LlmAgent`` with
``FunctionTool``-wrapped tools, following the reference article
"Building AI Agents with Google ADK, FastAPI, and MCP".
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

from app.agents import tools as agent_tools
from app.core.config import settings
from app.models.schemas import DataAnomaly


def _tool(fn: Any) -> FunctionTool:
    """Wrap a plain function in an ADK FunctionTool."""
    return FunctionTool(fn)


def build_document_understanding_agent() -> LlmAgent:
    """Agent 1: Multimodal document understanding."""
    return LlmAgent(
        name="DocumentUnderstandingAgent",
        model=settings.GEMINI_MODEL,
        description="Extracts text, tables, column headers, and classifies legacy documents.",
        instruction=(
            "You are the Document Understanding Agent. Given an uploaded legacy "
            "document (scanned ledger, PDF, Excel, or CSV), extract the column "
            "headers and raw tabular records, and classify the document type. "
            "Use the provided tools to extract columns and raw records."
        ),
        tools=[
            _tool(agent_tools.extract_document_columns),
            _tool(agent_tools.extract_raw_records),
        ],
    )


def build_schema_mapping_agent() -> LlmAgent:
    """Agent 2: Context-aware schema mapping."""
    return LlmAgent(
        name="SchemaMappingAgent",
        model=settings.GEMINI_MODEL,
        description="Maps raw ledger columns to the Uniplexity ERP schema and raises clarifications.",
        instruction=(
            "You map raw column headers from a legacy document to the canonical "
            "Uniplexity ERP schema. When a column is ambiguous, generate a "
            "human-in-the-loop clarification question with options. Use the "
            "map_columns_to_schema tool."
        ),
        tools=[
            _tool(agent_tools.map_columns_to_schema),
        ],
    )


def build_data_cleaning_agent() -> LlmAgent:
    """Agent 3: Data cleaning, normalization & anomaly detection."""
    return LlmAgent(
        name="DataCleaningAgent",
        model=settings.GEMINI_MODEL,
        description="Normalizes values, standardizes dates, groups product variants, and flags anomalies.",
        instruction=(
            "You clean and normalize raw records before import. Standardize dates "
            "to ISO format, normalize product name variants, and flag numeric "
            "anomalies. Use the clean_and_normalize_records tool."
        ),
        tools=[
            _tool(agent_tools.clean_and_normalize_records),
        ],
    )


def build_validation_import_agent() -> LlmAgent:
    """Agent 4: Validation & import."""
    return LlmAgent(
        name="ValidationImportAgent",
        model=settings.GEMINI_MODEL,
        description="Generates dry-run previews and commits validated records to the ERP.",
        instruction=(
            "You validate cleaned records, generate a dry-run preview for human "
            "approval, and commit approved records to the target ERP. Use the "
            "generate_dry_run_preview and commit_records_to_erp tools."
        ),
        tools=[
            _tool(agent_tools.generate_dry_run_preview),
            _tool(agent_tools.commit_records_to_erp),
        ],
    )


def build_all_agents() -> Dict[str, LlmAgent]:
    """Build all four pipeline agents keyed by name."""
    return {
        "document_understanding": build_document_understanding_agent(),
        "schema_mapping": build_schema_mapping_agent(),
        "data_cleaning": build_data_cleaning_agent(),
        "validation_import": build_validation_import_agent(),
    }