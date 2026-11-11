---
tier: "experimental"
last_reviewed: 2026-11-10
source_url: ""
source_ref: ""
source_commit: ""
content_hash: "7cc747d9a673679dad7a38700a4ff78dfab25ad8218d55b98eedc6a1642d10ee"
fetched_at: "2026-11-10"
upstream_license: "unknown"
owner: "taskmaster"
---
name: laravel-tdd
description: Laravel testing strategies with PHPUnit, Pest, model factories, HTTP tests, Sanctum authentication testing, mocking, and coverage. Use when writing Laravel tests with PHPUnit or Pest, or driving a Laravel feature test-first.
tier: "experimental"
metadata:
  origin: ECC
---


# Laravel Testing with TDD

Test-driven development for Laravel applications using PHPUnit, Pest, Laravel factories, and testing helpers.

## When to Activate

- Writing new Laravel applications or features
- Implementing API endpoints with Sanctum or Passport authentication
- Testing Eloquent models, relationships, scopes, and accessors
- Setting up testing infrastructure for Laravel projects
- Writing feature tests for HTTP controllers and form requests
- Mocking external services (queues, mail, notifications, HTTP)

## TDD Workflow for Laravel

### Red-Green-Refactor Cycle


## Setup

### PHPUnit Configuration


### Base TestCase Setup


## Model Factories


### Using Factories


## Model Testing


## Feature / HTTP Testing


## JSON API Testing


## Sanctum API Auth Testing


## Mocking and Fakes

### HTTP Fake


### Mail Fake


### Notification Fake


### Queue Fake


### Storage Fake


### Event Fake


## Artisan Command Tests


## Authorization Tests


## Pest Feature Tests


## Coverage


### Coverage Goals

| Component | Target |
|-----------|--------|
| Models | 95%+ |
| Actions/Services | 90%+ |
| Form Requests | 90%+ |
| Controllers | 85%+ |
| Policies | 95%+ |
| Overall | 80%+ |

## Testing Best Practices

### DO

- Use factories over manual `create()` calls
- One logical assertion per test
- Descriptive names: `test_guests_cannot_create_products`
- Test edge cases and authorization boundaries
- Mock external services with `Http::fake()`, `Mail::fake()`
- Use `RefreshDatabase` for clean state

### DON'T

- Don't test Laravel internals (trust the framework)
- Don't make tests dependent on each other
- Don't over-mock — mock only service boundaries
- Don't test private methods — test through the public interface
- Don't couple tests to HTML structure

## Quick Reference

| Pattern | Usage |
|---------|-------|
| `RefreshDatabase` | Reset database between tests |
| `$this->actingAs($user)` | Authenticate as user |
| `$this->withToken($token)` | Bearer token auth for APIs |
| `Model::factory()->create()` | Create model with factory |
| `Model::factory()->count(5)->create()` | Create multiple records |
| `Http::fake([...])` | Mock HTTP calls |
| `Mail::fake()` | Trap sent mail |
| `Notification::fake()` | Trap sent notifications |
| `Queue::fake()` | Trap queued jobs |
| `Event::fake()` | Trap dispatched events |
| `Storage::fake('public')` | Trap file operations |
| `assertDatabaseHas` | Assert DB row exists |
| `assertSoftDeleted` | Assert soft-delete |
| `assertSessionHasErrors` | Assert validation errors |
| `assertForbidden` | Assert 403 status |

## Related Skills

- `laravel-patterns` — Laravel architecture, Eloquent, routing, and API patterns
- `laravel-security` — Laravel authentication, authorization, and secure coding
- `tdd-workflow` — The repo-wide RED -> GREEN -> REFACTOR loop
- `backend-patterns` — General backend API and database patterns
