---
tier: "experimental"
last_reviewed: 2026-11-10
source_url: ""
source_ref: ""
source_commit: ""
content_hash: "6d8cd5ca0844aba8576d7bd5b7a39d123055122578ce78a3a24830af63b3de15"
fetched_at: "2026-11-10"
upstream_license: "unknown"
owner: "taskmaster"
---
name: django-tdd
description: Django testing strategies with pytest-django, TDD methodology, factory_boy, mocking, coverage, and testing Django REST Framework APIs. Use when writing Django or DRF tests with pytest-django, or driving a Django feature test-first.
tier: "experimental"
metadata:
  origin: ECC
---


# Django Testing with TDD

Test-driven development for Django applications using pytest, factory_boy, and Django REST Framework.

## When to Activate

- Writing new Django applications
- Implementing Django REST Framework APIs
- Testing Django models, views, and serializers
- Setting up testing infrastructure for Django projects

## TDD Workflow for Django

### Red-Green-Refactor Cycle


## Setup

### pytest Configuration


### Test Settings


### conftest.py


## Factory Boy

### Factory Setup


### Using Factories


## Model Testing

### Model Tests


## View Testing

### Django View Testing


## DRF API Testing

### Serializer Testing


### API ViewSet Testing


## Mocking and Patching

### Mocking External Services


### Mocking Email Sending


## Integration Testing

### Full Flow Testing


## Testing Best Practices

### DO

- **Use factories**: Instead of manual object creation
- **One assertion per test**: Keep tests focused
- **Descriptive test names**: `test_user_cannot_delete_others_post`
- **Test edge cases**: Empty inputs, None values, boundary conditions
- **Mock external services**: Don't depend on external APIs
- **Use fixtures**: Eliminate duplication
- **Test permissions**: Ensure authorization works
- **Keep tests fast**: Use `--reuse-db` and `--nomigrations`

### DON'T

- **Don't test Django internals**: Trust Django to work
- **Don't test third-party code**: Trust libraries to work
- **Don't ignore failing tests**: All tests must pass
- **Don't make tests dependent**: Tests should run in any order
- **Don't over-mock**: Mock only external dependencies
- **Don't test private methods**: Test public interface
- **Don't use production database**: Always use test database

## Coverage

### Coverage Configuration


### Coverage Goals

| Component | Target Coverage |
|-----------|-----------------|
| Models | 90%+ |
| Serializers | 85%+ |
| Views | 80%+ |
| Services | 90%+ |
| Utilities | 80%+ |
| Overall | 80%+ |

## Quick Reference

| Pattern | Usage |
|---------|-------|
| `@pytest.mark.django_db` | Enable database access |
| `client` | Django test client |
| `api_client` | DRF API client |
| `factory.create_batch(n)` | Create multiple objects |
| `patch('module.function')` | Mock external dependencies |
| `override_settings` | Temporarily change settings |
| `force_authenticate()` | Bypass authentication in tests |
| `assertRedirects` | Check for redirects |
| `assertTemplateUsed` | Verify template usage |
| `mail.outbox` | Check sent emails |

Remember: Tests are documentation. Good tests explain how your code should work. Keep them simple, readable, and maintainable.
