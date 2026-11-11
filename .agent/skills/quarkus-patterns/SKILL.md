---
tier: experimental
last_reviewed: 2026-11-10
content_hash: a50babc2777b58d3822564f9adeca2636314fd718aebd38cbe40eafcb89c9a6c
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
description: Quarkus 3.x LTS architecture patterns with Camel for messaging, RESTful API design, CDI services, data access with Panache, and async processing. Use for Java Quarkus backend work with event-driven architectures. Use when building or reviewing a Quarkus service, especially with Camel messaging or Panache data access.
name: quarkus-patterns
origin: ECC
---
# Quarkus Development Patterns
Quarkus 3.x architecture and API patterns for cloud-native, event-driven services with Apache Camel.
## When to Activate
- Building REST APIs with JAX-RS or RESTEasy Reactive
- Structuring resource → service → repository layers
- Implementing event-driven patterns with Apache Camel and RabbitMQ
- Configuring Hibernate Panache, caching, or reactive streams
- Adding validation, exception mapping, or pagination
- Setting up profiles for dev/staging/production environments (YAML config)
- Custom logging with LogContext and Logback/Logstash encoder
- Working with CompletableFuture for async operations
- Implementing conditional flow processing
- Working with GraalVM native compilation
## Service Layer with Multiple Dependencies
**Key Patterns:**
- `@RequiredArgsConstructor` for constructor injection via Lombok
- `@Slf4j` for Logback logging
- `@Transactional` on service methods that write through Panache or repositories
- Validate input before persistence or message publication
- Event tracking for success/error scenarios
- Async Camel message publishing
## Custom Logging Context Pattern (Logback)
**Logback Configuration (logback.xml):**
## Event Service Pattern
## Camel Message Publishing (RabbitMQ)
**Camel Route Configuration:**
## Camel Direct Routes (In-Memory)
## Camel File Processing
## Camel Bean Invocation
## REST API Structure
## Repository Pattern (Panache Repository)
## Service Layer with Transactions
## DTOs and Validation
## Exception Mapping
## CompletableFuture Async Operations
## Caching
## Configuration as YAML
## Health Checks
## Dependencies (Maven)
## Best Practices
### Architecture
- Use `@RequiredArgsConstructor` with Lombok for constructor injection
- Keep service layer thin; delegate complex logic to specialized classes
- Use Camel routes for message routing and integration patterns
- Prefer Panache Repository pattern for data access
### Event-Driven
- Always track operations with EventService (success/error events)
- Use Camel `direct:` endpoints for in-memory routing
- Use `spring-rabbitmq` component for RabbitMQ integration
- Implement async publishing with `ProducerTemplate.asyncSendBody()`
### Logging
- Use Logback with Logstash encoder for structured logging
- Propagate LogContext through service calls with `SafeAutoCloseable`
- Add contextual information to LogContext for request tracing
- Use `@Slf4j` instead of manual logger instantiation
### Async Operations
- Use CompletableFuture for non-blocking I/O operations
- Call `.join()` when you need to wait for completion
- Handle exceptions from CompletableFuture properly
- Pass LogContext to async operations for tracing
### Configuration
- Use YAML configuration (`quarkus-config-yaml`)
- Profile-aware configuration for dev/test/prod environments
- Externalize sensitive configuration to environment variables
- Use `@ConfigProperty` for type-safe config injection
### Validation
- Validate at resource layer with `@Valid`
- Use Bean Validation annotations on DTOs
- Map exceptions to proper HTTP responses with `@Provider`
### Transactions
- Use `@Transactional` on service methods that modify data
- Keep transactions short and focused
- Avoid calling async operations within transactions
### Testing
- Use `camel-quarkus-junit5` for route testing
- Use AssertJ for assertions
- Mock all external dependencies
- Test conditional flow logic thoroughly
### Quarkus-Specific
- Stay on latest LTS version (3.x)
- Use Quarkus dev mode for hot reload
- Add health checks for production readiness
- Test native compilation compatibility periodically