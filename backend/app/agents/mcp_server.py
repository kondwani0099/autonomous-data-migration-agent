"""MCP server exposure for the Uniplexity migration agent swarm.

Uses the built-in ADK ``to_mcp_server`` utility to expose the pipeline
agents as an MCP server, following the reference article
"Building AI Agents with Google ADK, FastAPI, and MCP".

Note: Requires ``mcp`` package installed (``pip install mcp``).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

# Lazy import — mcp package may not be installed in all environments.
if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP


def create_mcp_server() -> Any:
    """Create an MCP server exposing the migration pipeline agents.

    Returns:
        A ``FastMCP`` server with the agents registered as tools.

    Raises:
        ImportError: If the ``mcp`` package is not installed.
    """
    try:
        from google.adk.tools.mcp_tool._agent_to_mcp import to_mcp_server
    except ImportError as exc:
        raise ImportError(
            "MCP server requires the 'mcp' package. "
            "Install with: pip install mcp"
        ) from exc

    from app.agents.adk_agents import build_all_agents

    agents = build_all_agents()
    # Use the primary validation agent as the main MCP tool entry point.
    primary_agent = agents["validation_import"]
    return to_mcp_server(
        primary_agent,
        name="uniplexity-migration-agent",
        instructions=(
            "You are the Uniplexity Migration Agent. You help users migrate "
            "legacy data (scanned ledgers, PDFs, Excel) into the Uniplexity ERP. "
            "Use the pipeline to understand, map, clean, and validate records."
        ),
    )


async def run_mcp_server() -> None:
    """Run the MCP server over standard I/O."""
    server = create_mcp_server()
    server.run(transport="stdio")