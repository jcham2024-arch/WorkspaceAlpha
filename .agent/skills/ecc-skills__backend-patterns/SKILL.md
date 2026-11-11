---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 54859dd5bb6266f57f6b819a09ac7ef135a7a2d4e4d1e924f05f41fe4ed8f32b
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
description: Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes. Use when building or reviewing Node.js, Express, or Next.js API routes and their data access.
name: backend-patterns
origin: ECC
---
# Backend Development Patterns
Backend architecture patterns and best practices for scalable server-side applications.
## When to Activate
- Designing REST or GraphQL API endpoints
- Implementing repository, service, or controller layers
- Optimizing database queries (N+1, indexing, connection pooling)
- Adding caching (Redis, in-memory, HTTP cache headers)
- Setting up background jobs or async processing
- Structuring error handling and validation for APIs
- Building middleware (auth, logging, rate limiting)
## API Design Patterns
### RESTful API Structure
### Repository Pattern
### Service Layer Pattern
### Middleware Pattern
## Database Patterns
### Query Optimization
### N+1 Query Prevention
### Transaction Pattern
## Caching Strategies
### Redis Caching Layer
### Cache-Aside Pattern
## Error Handling Patterns
### Centralized Error Handler
### Retry with Exponential Backoff
## Authentication & Authorization
### JWT Token Validation
### Role-Based Access Control
## Rate Limiting
Rate limiting must use a shared store such as Redis, a gateway, or the
platform's native limiter. Do not use per-process in-memory counters for
production APIs: they reset on deploy, split across replicas, and fail open in
serverless or multi-instance environments.
Keep the backend layer responsible for choosing the integration point and error
shape; use `api-design` for the HTTP contract and `security-review` for abuse
case review.
## Background Jobs & Queues
### Simple Queue Pattern
## Logging & Monitoring
### Structured Logging
**Remember**: Backend patterns enable scalable, maintainable server-side applications. Choose patterns that fit your complexity level.