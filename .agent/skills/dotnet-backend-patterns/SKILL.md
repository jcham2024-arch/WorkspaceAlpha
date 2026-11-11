---
tier: experimental
last_reviewed: 2026-11-10
content_hash: b710d7e06e403644ad2508879759c86b21989d49b99c3757e9c53a75f794009a
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
date_added: 2026-02-27
description: ""Master C#/.NET patterns for building production-grade APIs, MCP servers, and enterprise backends with modern best practices (2024/2025).""
name: dotnet-backend-patterns
risk: safe
source: community
---
# .NET Backend Development Patterns
Master C#/.NET patterns for building production-grade APIs, MCP servers, and enterprise backends with modern best practices (2024/2025).
## Use this skill when
- Developing new .NET Web APIs or MCP servers
- Reviewing C# code for quality and performance
- Designing service architectures with dependency injection
- Implementing caching strategies with Redis
- Writing unit and integration tests
- Optimizing database access with EF Core or Dapper
- Configuring applications with IOptions pattern
- Handling errors and implementing resilience patterns
## Do not use this skill when
- The project is not using .NET or C#
- You only need frontend or client guidance
- The task is unrelated to backend architecture
## Template boundaries
Examples target .NET 8-era APIs and SQL Server; package/provider versions must be
pinned and compiled in the destination application. Assets are partial sketches,
not a standalone project: supply interfaces, DTO namespaces, options and schema.
Use one shared domain Product type when combining them. Authorization/tenant
filters precede reads, writes and cache access; the single-tenant sample keys are
not suitable for multi-tenant data. No migration or production write is implied.
## Instructions
- Define architecture boundaries, modules, and layering.
- Apply DI, async patterns, and resilience strategies.
- Validate data access performance and caching.
- Add tests and observability for critical flows.
- If detailed patterns are required, open `resources/implementation-playbook.md`.
## Resources
- `resources/implementation-playbook.md` for detailed .NET patterns and examples.
## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
## Platform variants
OS-specific companions for this skill:
- [Windows](platforms/windows.md)