"""FastAPI Application Main Entry Point.

Integrates Google ADK agents with FastAPI, following the reference article
"Building AI Agents with Google ADK, FastAPI, and MCP".
"""

import argparse
import asyncio
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings
from app.api.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
async def health_check() -> dict:
    return {"status": "healthy"}


@app.get("/agent-info")
async def agent_info() -> dict:
    """Provide agent swarm information (ADK integration)."""
    from app.agents.adk_agents import build_all_agents

    agents = build_all_agents()
    return {
        "agents": {
            name: {
                "description": agent.description,
                "model": agent.model,
                "tools": [t.name for t in agent.tools] if agent.tools else [],
            }
            for name, agent in agents.items()
        }
    }


# Serve Frontend static build files if present (Production Container mode)
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    assets_dir = os.path.join(static_dir, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str) -> FileResponse:
        if full_path.startswith("api") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            raise HTTPException(status_code=404, detail="API path not found")
        file_path = os.path.join(static_dir, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(static_dir, "index.html"))
else:
    @app.get("/")
    async def root() -> dict:
        return {
            "app": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "status": "running",
            "docs_url": "/docs",
        }


def run_server(mode: str = "web") -> None:
    """Run the server in the specified mode (web or mcp)."""
    if mode == "mcp":
        import uvicorn
        print("Starting MCP server mode...")
        # MCP mode: run via stdio transport
        from app.agents.mcp_server import run_mcp_server
        asyncio.run(run_mcp_server())
    else:
        import uvicorn
        print("Starting Web server mode...")
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=9999,
            reload=False,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Uniplexity Migration Agent Server")
    parser.add_argument(
        "--mode",
        choices=["web", "mcp"],
        default="web",
        help="Run as web server or MCP server (default: web)",
    )
    args = parser.parse_args()
    run_server(mode=args.mode)
