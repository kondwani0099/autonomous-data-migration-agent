"""Agent 2: Context-Aware Schema Mapping Agent (Google ADK).

Maps raw document columns to the canonical target schema. When a real
GEMINI_API_KEY is configured, the mapping is performed by the LLM agent
(semantic reasoning). Otherwise it falls back to deterministic keyword matching.
"""

import json
import re
from typing import Any, Dict, List, Optional, Tuple

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agents.adk_agents import build_schema_mapping_agent
from app.agents.tools import map_columns_to_schema, get_category_schema
from app.core.config import settings


class SchemaMappingAgent:
    def __init__(self) -> None:
        self.name = "SchemaMappingAgent"
        self.adk_agent: LlmAgent = build_schema_mapping_agent()
        self._session_service = InMemorySessionService()

    def _ai_mapping_available(self) -> bool:
        key = getattr(settings, "GEMINI_API_KEY", "") or ""
        return bool(key) and not settings.MOCK_GCP and not key.lower().startswith("mock")

    async def map_columns(
        self, client_id: str, extracted_columns: List[str], data_category: str = "sales"
    ) -> Tuple[Dict[str, str], List[Dict[str, Any]]]:
        """Map raw columns to the Uniplexity ERP schema for the target category.

        Uses the LLM agent for semantic mapping when an API key is available,
        otherwise falls back to deterministic keyword-based mapping.
        """
        if self._ai_mapping_available() and extracted_columns:
            try:
                result = await self._map_with_ai(client_id, extracted_columns, data_category)
                if result is not None:
                    return result
            except Exception as e:  # noqa: BLE001 - fall back to deterministic mapping
                print(f"[SchemaMappingAgent] AI mapping failed, falling back: {e}")

        result = map_columns_to_schema(client_id, extracted_columns, data_category)
        return result["mappings"], result["clarifications"]

    async def _map_with_ai(
        self, client_id: str, extracted_columns: List[str], data_category: str
    ) -> Optional[Tuple[Dict[str, str], List[Dict[str, Any]]]]:
        """Run the schema mapping LLM agent and parse its JSON mapping decision."""
        schema = get_category_schema(data_category)
        target_cols = ", ".join(schema["columns"]) if schema["columns"] else "(none specified)"
        source_cols = ", ".join(extracted_columns)

        prompt = (
            "You are the Schema Mapping Agent for the Uniplexity ERP migration.\n\n"
            f"Target data format: {schema['label']} (category '{data_category}').\n"
            f"Canonical target columns: {target_cols}.\n\n"
            f"Detected source columns from the uploaded document: {source_cols}.\n\n"
            "Map each detected column to the most semantically similar canonical column. "
            "If a detected column has no reasonable match, map it to null (skip it). "
            "If a canonical column is matched more than once, keep the first and add a "
            "clarification question for the second. If any detected column is ambiguous, "
            "add a clarification question with options.\n\n"
            "Return STRICT JSON only (no markdown fences, no extra text) in this exact shape:\n"
            '{"mappings": {"<detected column>": "<canonical column or null>"}, '
            '"clarifications": [{"question": "...", "options": ["..."], "context": "..."}]}'
        )

        text = await self._run_llm(prompt)
        parsed = self._parse_mapping_json(text)
        if not parsed or not isinstance(parsed.get("mappings"), dict):
            return None

        mappings = {k: v for k, v in parsed["mappings"].items() if v}
        clarifications = parsed.get("clarifications") or []
        for c in clarifications:
            if isinstance(c, dict):
                c.setdefault("agent", self.name)
                c.setdefault("options", ["Yes", "No", "Skip"])
        return mappings, clarifications

    async def _run_llm(self, prompt: str) -> str:
        """Run the ADK LlmAgent and return its final text response."""
        runner = Runner(
            app_name=self.adk_agent.name or self.name,
            agent=self.adk_agent,
            session_service=self._session_service,
        )
        session = await self._session_service.create_session(
            app_name=runner.app_name, user_id="pipeline"
        )
        final_text = ""
        async for event in runner.run_async(
            user_id="pipeline",
            session_id=session.id,
            new_message=types.Content(role="user", parts=[types.Part(text=prompt)]),
        ):
            if event.is_final_response() and event.content:
                for part in event.content.parts:
                    if part.text:
                        final_text += part.text
        return final_text

    @staticmethod
    def _parse_mapping_json(text: str) -> Optional[Dict[str, Any]]:
        """Extract a JSON mapping object from an LLM response (tolerates markdown)."""
        if not text:
            return None
        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\{[\s\S]*\}", text)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    return None
            return None
