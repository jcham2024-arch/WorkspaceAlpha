---
name: backend-patterns
description: Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes. Use when building or reviewing Node.js, Express, or Next.js API routes and their data access.
license: MIT
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

### Simple In-Memory Rate Limiter


## Background Jobs & Queues

### Simple Queue Pattern


## Logging & Monitoring

### Structured Logging


**Remember**: Backend patterns enable scalable, maintainable server-side applications. Choose patterns that fit your complexity level.
