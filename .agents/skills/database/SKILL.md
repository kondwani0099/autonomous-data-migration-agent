---
name: database
description: Guidance for SQLAlchemy 2.0 ORM models, Alembic migrations, database indexes, N+1 query elimination, and safety.
---

# Database Skill Directive

<GUIDELINES>
1. **SQLAlchemy 2.0 Declarative**: Define models in `backend/app/models/` using `Mapped[]` and `mapped_column()`.
2. **Alembic Migrations**: Generate migration scripts for all schema changes (`alembic revision --autogenerate -m "..."`). Never modify tables manually in production databases.
3. **Query Optimization**: Avoid N+1 query problems by using `joinedload()` or `selectinload()` when querying relationships.
4. **Indexes & Constraints**: Add indexes to foreign keys and columns frequently used in `WHERE`, `ORDER BY`, or `JOIN` clauses.
5. **Data Safety**: Destructive column drops or table deletions REQUIRE human review and approval.
</GUIDELINES>
