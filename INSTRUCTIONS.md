# INSTRUCTIONS.md — Project Standards & Conventions

This document outlines backend, frontend, security, and testing conventions for the **Uniplexity Migration Agent** workspace.

---

## 1. Backend Engineering Conventions (Python / FastAPI / ADK)

- **Framework:** FastAPI with Pydantic v2 schemas and Google ADK for agent orchestration.
- **Python Version:** Python 3.11+. Use strict type hints on all functions (`def func(param: str) -> bool:`).
- **Asynchronous Execution:** Endpoints and network/database calls should be `async` where supported.
- **Error Handling:** Use standard FastAPI HTTP exceptions (`HTTPException(status_code=..., detail=...)`). Never return silent `None` or catch broad `Exception` without logging.
- **Agent Boundaries:** Each ADK agent in `app/agents/` must have a clearly defined role, prompt template, tool set, and schema boundary.
- **Data Models:** Store models in `app/models/schemas.py`. Keep business logic out of Pydantic models.

---

## 2. Frontend Engineering Conventions (React / Vite / TypeScript / Tailwind CSS)

- **Framework:** React 18 with TypeScript and Vite. Use functional components and modern React hooks.
- **Styling:** Vanilla Tailwind CSS with glassmorphism, harmonious dark mode themes, and smooth micro-animations.
- **State Management:** Keep local component state clear and manageable. Centralize API bindings in `src/services/api.ts`.
- **Component Separation:** Maintain focused UI components in `src/components/` and page-level containers in `src/pages/`.
- **Accessibility & UX:** All interactive elements (buttons, inputs) must have descriptive aria labels and unique ID attributes.

---

## 3. Security & Data Integrity

- **No Exposed Secrets:** Never commit API keys or GCP credentials to repository files. Use environment variables.
- **Sanitization:** Validate all incoming document files and clean user inputs prior to processing.
- **Audit Compliance:** Every data transformation or human clarification response must generate an audit log entry in Firestore.

---

## 4. Verification & Testing

- Before concluding any non-trivial edit, run `python scripts/verify.py` to confirm that unit tests and linters pass cleanly.
- Maintain test coverage in `backend/tests/`.
