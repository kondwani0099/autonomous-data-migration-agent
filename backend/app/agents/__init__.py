"""Google ADK Agent Swarm package for Uniplexity Data Migration."""

from .document_understanding import DocumentUnderstandingAgent
from .schema_mapping import SchemaMappingAgent
from .data_cleaning import DataCleaningAgent
from .validation_import import ValidationImportAgent
from .pipeline import MigrationPipeline
from .adk_agents import build_all_agents

# MCP server is optional — requires ``mcp`` package installed.
try:
    from .mcp_server import create_mcp_server, run_mcp_server
except ImportError:
    create_mcp_server = None  # type: ignore
    run_mcp_server = None  # type: ignore

__all__ = [
    "DocumentUnderstandingAgent",
    "SchemaMappingAgent",
    "DataCleaningAgent",
    "ValidationImportAgent",
    "MigrationPipeline",
    "build_all_agents",
    "create_mcp_server",
    "run_mcp_server",
]
