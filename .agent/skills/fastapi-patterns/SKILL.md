---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 35d533cf8a71ff8f0fb5a2a562204763d3bf05aae7f1456f6f8a242ff683b80d
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
description: FastAPI best practices covering project structure, Pydantic v2 schemas, dependency injection, async handlers, authentication, authorization, transactional service layers, and testing with httpx and pytest. Use when building or reviewing FastAPI apps — Pydantic schemas, dependencies, async handlers, auth, or tests.
name: fastapi-patterns
origin: ECC
---
# FastAPI Patterns
Modern, production-grade FastAPI development: project layout, Pydantic v2 schemas, dependency injection, async patterns, auth, transactional service methods, and testing.
## Project Structure
---
## App Factory and Lifespan
---
## Configuration with pydantic-settings
---
## Pydantic Schemas (v2)
---
## Dependency Injection
---
## Router and Endpoint Design
---
## Service Layer
> **Note on Database Design:** Application-level unique handling requires an underlying unique database index (e.g., `unique=True` on your SQLAlchemy mapping attributes). Without underlying constraints, application layer error-catching cannot safely prevent concurrent race conditions.
---
## Testing with httpx and pytest
---
## Anti-Patterns
---
## Best Practices
- Always declare a typed `response_model` to prevent accidental PII/data leaks and output clean OpenAPI schemas.
- Consolidate standard middleware dependency injections via type-aliasing: `DbDep = Annotated[AsyncSession, Depends(get_db)]`.
- Wrap database mutation boundaries gracefully within transactions inside your service layer, catching structural database errors directly.
- Parse JWT parameters defensively, expecting potential string/integer cast mismatches from modern payload variations.
- Enforce deterministic sorting (e.g., `.order_by(Model.id)`) on all offset/limit paginated endpoints to avoid data skips.
- Isolate authorization checks from core authentication dependencies to provide precise REST status signals (`401` vs `403`).