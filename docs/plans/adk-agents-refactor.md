# Plan: Refactor Agents to Google ADK with MCP Support

## Objective
Convert the current mock/stub agent implementations into real Google ADK
`LlmAgent` instances with tools, following the reference article
"Building AI Agents with Google ADK, FastAPI, and MCP". Expose the agents
both through the existing FastAPI pipeline and as an MCP server.

## Reference Patterns (from article)
1. Define tool functions with type hints.
2. Wrap tools in `FunctionTool` and attach to `LlmAgent`.
3. Serve via FastAPI using ADK's `get_fast_api_app` or custom endpoints.
4. Expose tools via MCP using `adk_to_mcp_tool_type` / `to_mcp_server`.

## Affected Files
- `backend/app/agents/tools.py` (NEW) — shared ADK tool functions
- `backend/app/agents/document_understanding.py` — ADK agent
- `backend/app/agents/schema_mapping.py` — ADK agent
- `backend/app/agents/data_cleaning.py` — ADK agent
- `backend/app/agents/validation_import.py` — ADK agent
- `backend/app/agents/pipeline.py` — orchestration using ADK runners
- `backend/app/agents/mcp_server.py` (NEW) — MCP server exposure
- `backend/requirements.txt` — add `google-adk`, `mcp`
- `backend/app/main.py` — optional MCP/agent-info endpoints

## Design
- Each agent becomes an `LlmAgent` with a `name`, `model`, `instruction`,
  and `tools=[...]`.
- Tool functions are plain Python functions with type hints, wrapped via
  `FunctionTool`.
- The pipeline runs agents via ADK `Runner` with `InMemorySessionService`.
- MCP server exposes the agents via `to_mcp_server` (ADK 2.7.1 built-in).

## Risks
- `mcp` package not yet installed — must add to requirements.
- ADK 2.7.1 API differs slightly from article (uses `to_mcp_server`).
- Gemini API key required for real LLM calls; keep mock fallback.

## Acceptance Criteria
- `pytest` passes.
- Agents import cleanly and expose tools.
- MCP server can be constructed.