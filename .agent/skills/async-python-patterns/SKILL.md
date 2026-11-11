---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 267c8148d4407b24912ac0159d0675786bb16f5471e8b701e182ca3e407538ae
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
date_added: 2026-02-27
description: Comprehensive guidance for implementing asynchronous Python applications using asyncio, concurrent programming patterns, and async/await for building high-performance, non-blocking systems.
name: async-python-patterns
risk: safe
source: community
---
# Async Python Patterns
Comprehensive guidance for implementing asynchronous Python applications using asyncio, concurrent programming patterns, and async/await for building high-performance, non-blocking systems.
## Use this skill when
- Building async web APIs (FastAPI, aiohttp, Sanic)
- Implementing concurrent I/O operations (database, file, network)
- Creating web scrapers with concurrent requests
- Developing real-time applications (WebSocket servers, chat systems)
- Processing multiple independent tasks simultaneously
- Building microservices with async communication
- Optimizing I/O-bound workloads
- Implementing async background tasks and queues
## Do not use this skill when
- The workload is CPU-bound with minimal I/O.
- A simple synchronous script is sufficient.
- The runtime environment cannot support asyncio/event loop usage.
## Instructions
- Clarify workload characteristics (I/O vs CPU), targets, and runtime constraints.
- Pick concurrency patterns (tasks, gather, queues, pools) with cancellation rules.
- Add timeouts, backpressure, and structured error handling.
- Include testing and debugging guidance for async code paths.
- If detailed examples are required, open `resources/implementation-playbook.md`.
Refer to `resources/implementation-playbook.md` for detailed patterns and examples.
## Resources
- `resources/implementation-playbook.md` for detailed patterns and examples.
## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.