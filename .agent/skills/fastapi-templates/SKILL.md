---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 6f5e09cf3ca68e15edfbf93791465539a7580b212abbfb4a93df4f58fb0c3a05
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
date_added: 2026-02-27
description: Create production-ready FastAPI projects with async patterns, dependency injection, and comprehensive error handling. Use when building new FastAPI applications or setting up backend API projects.
name: fastapi-templates
risk: critical
source: community
---
# FastAPI Project Templates
Starting-point FastAPI project structures with async patterns, dependency injection, middleware, and best practices for building high-performance APIs.
## Use this skill when
- Starting new FastAPI projects from scratch
- Implementing async REST APIs with Python
- Building high-performance web services and microservices
- Creating async applications with PostgreSQL, MongoDB
- Setting up API projects with proper structure and testing
## Do not use this skill when
- The task is unrelated to fastapi project templates
- You need a different domain or tool outside this scope
## Instructions
- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.
## Example
```text
Create a PostgreSQL-backed user API using the playbook. First define request/output/internal schemas and object authorization, then test registration, inactive-token rejection and forbidden cross-user reads. Report missing project files before claiming a runnable service.
```
## Resources
- `resources/implementation-playbook.md` for detailed patterns and examples.
## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.