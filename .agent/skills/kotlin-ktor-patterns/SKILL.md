---
name: kotlin-ktor-patterns
description: Ktor server patterns including routing DSL, plugins, authentication, Koin DI, kotlinx.serialization, WebSockets, and testApplication testing. Use when building a Ktor server — routing, plugins, auth, DI, serialization, or tests.
metadata:
  origin: ECC
---

# Ktor Server Patterns

Comprehensive Ktor patterns for building robust, maintainable HTTP servers with Kotlin coroutines.

## When to Activate

- Building Ktor HTTP servers
- Configuring Ktor plugins (Auth, CORS, ContentNegotiation, StatusPages)
- Implementing REST APIs with Ktor
- Setting up dependency injection with Koin
- Writing Ktor integration tests with testApplication
- Working with WebSockets in Ktor

## Application Structure

### Standard Ktor Project Layout


### Application Entry Point


## Routing DSL

### Basic Routes


### Route Organization with Authenticated Routes


## Content Negotiation & Serialization

### kotlinx.serialization Setup


### Serializable Models


### Custom Serializers


## Authentication

### JWT Authentication


### Auth Routes


## Status Pages (Error Handling)


## CORS Configuration


## Koin Dependency Injection

### Module Definition


### Using Koin in Routes


### Koin for Testing


## Request Validation


## WebSockets


## testApplication Testing

### Basic Route Testing


### Testing Authenticated Routes


## Configuration

### application.yaml


### Reading Config


## Quick Reference: Ktor Patterns

| Pattern | Description |
|---------|-------------|
| `route("/path") { get { } }` | Route grouping with DSL |
| `call.receive<T>()` | Deserialize request body |
| `call.respond(status, body)` | Send response with status |
| `call.parameters["id"]` | Read path parameters |
| `call.request.queryParameters["q"]` | Read query parameters |
| `install(Plugin) { }` | Install and configure plugin |
| `authenticate("name") { }` | Protect routes with auth |
| `by inject<T>()` | Koin dependency injection |
| `testApplication { }` | Integration testing |

**Remember**: Ktor is designed around Kotlin coroutines and DSLs. Keep routes thin, push logic to services, and use Koin for dependency injection. Test with `testApplication` for full integration coverage.

## Platform variants

OS-specific companions for this skill:

- [Android](platforms/android.md)
