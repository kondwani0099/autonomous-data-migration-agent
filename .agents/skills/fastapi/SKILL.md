---
name: fastapi
description: Guidance for building FastAPI routes, Pydantic v2 schemas, async endpoints, dependency injection, and middleware.
---

# FastAPI Skill Directive

<GUIDELINES>
1. **APIRouter Organization**: Group endpoints logically in `backend/app/api/v1/endpoints/`. Use explicit tags, summary descriptions, and response models.
2. **Pydantic v2 Schemas**: Define separate `Create`, `Update`, and `Response` schemas in `backend/app/schemas/`. Use strict field validation and `ConfigDict(from_attributes=True)`.
3. **Dependency Injection**: Inject database sessions, current users, and shared services using `FastAPI.Depends()`.
4. **Async Best Practices**: Declare endpoints with `async def` for I/O operations. Use async SQLAlchemy sessions (`AsyncSession`).
5. **Exception Handling**: Raise `HTTPException(status_code=..., detail=...)` with standard HTTP error status codes.
</GUIDELINES>
