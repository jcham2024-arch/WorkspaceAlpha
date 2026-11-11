---
tier: "experimental"
last_reviewed: 2026-11-10
source_url: ""
source_ref: ""
source_commit: ""
content_hash: "0b91c8946f7d15748ef1a03162e45d0bdf84a10f4f03f6e714775e6786d194cd"
fetched_at: "2026-11-10"
upstream_license: "unknown"
owner: "taskmaster"
---
name: python-testing
description: Python testing strategies using pytest, TDD methodology, fixtures, mocking, parametrization, and coverage requirements. Use when writing pytest tests — fixtures, mocks, parametrization, or coverage.
tier: "experimental"
metadata:
  origin: ECC
---


# Python Testing Patterns

Comprehensive testing strategies for Python applications using pytest, TDD methodology, and best practices.

## When to Activate

- Writing new Python code (follow TDD: red, green, refactor)
- Designing test suites for Python projects
- Reviewing Python test coverage
- Setting up testing infrastructure

## Core Testing Philosophy

### Test-Driven Development (TDD)

Always follow the TDD cycle:

1. **RED**: Write a failing test for the desired behavior
2. **GREEN**: Write minimal code to make the test pass
3. **REFACTOR**: Improve code while keeping tests green


### Coverage Requirements

- **Target**: 80%+ code coverage
- **Critical paths**: 100% coverage required
- Use `pytest --cov` to measure coverage


## pytest Fundamentals

### Basic Test Structure


### Assertions


## Fixtures

### Basic Fixture Usage


### Fixture with Setup/Teardown


### Fixture Scopes


### Fixture with Parameters


### Using Multiple Fixtures


### Autouse Fixtures


### Conftest.py for Shared Fixtures (Flask)


## Parametrization

### Basic Parametrization


### Multiple Parameters


### Parametrize with IDs


### Parametrized Fixtures


## Markers and Test Selection

### Custom Markers


### Run Specific Tests


### Configure Markers in pytest.ini


## Mocking and Patching

### Mocking Functions


### Mocking Return Values


### Mocking Exceptions


### Mocking Context Managers


### Using Autospec


### Mock Class Instances


### Mock Property


## Testing Async Code

### Async Tests with pytest-asyncio


### Async Fixture (FastAPI)

`ASGITransport` does not run lifespan events. Install `asgi-lifespan` and wrap the client in `LifespanManager` when the app uses startup or shutdown handlers. See [FastAPI's async testing guidance](https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/async-tests.md).


### Mocking Async Functions


## Testing Exceptions

### Testing Expected Exceptions


### Testing Exception Attributes


## Testing Side Effects

### Testing File Operations


### Testing with pytest's tmp_path Fixture


### Testing with tmpdir Fixture


## Test Organization

### Directory Structure

```
tests/
├── conftest.py                 # Shared fixtures
├── __init__.py
├── unit/                       # Unit tests
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_utils.py
│   └── test_services.py
├── integration/                # Integration tests
│   ├── __init__.py
│   ├── test_api.py
│   └── test_database.py
└── e2e/                        # End-to-end tests
    ├── __init__.py
    └── test_user_flow.py
```

### Test Classes


## Best Practices

### DO

- **Follow TDD**: Write tests before code (red-green-refactor)
- **Test one thing**: Each test should verify a single behavior
- **Use descriptive names**: `test_user_login_with_invalid_credentials_fails`
- **Use fixtures**: Eliminate duplication with fixtures
- **Mock external dependencies**: Don't depend on external services
- **Test edge cases**: Empty inputs, None values, boundary conditions
- **Aim for 80%+ coverage**: Focus on critical paths
- **Keep tests fast**: Use marks to separate slow tests

### DON'T

- **Don't test implementation**: Test behavior, not internals
- **Don't use complex conditionals in tests**: Keep tests simple
- **Don't ignore test failures**: All tests must pass
- **Don't test third-party code**: Trust libraries to work
- **Don't share state between tests**: Tests should be independent
- **Don't catch exceptions in tests**: Use `pytest.raises`
- **Don't use print statements**: Use assertions and pytest output
- **Don't write tests that are too brittle**: Avoid over-specific mocks

## Common Patterns

### Testing API Endpoints (Flask)


### Testing Database Operations


### Testing Class Methods


## pytest Configuration

### pytest.ini


### pyproject.toml


## Running Tests


## Quick Reference

| Pattern | Usage |
|---------|-------|
| `pytest.raises()` | Test expected exceptions |
| `@pytest.fixture()` | Create reusable test fixtures |
| `@pytest.mark.parametrize()` | Run tests with multiple inputs |
| `@pytest.mark.slow` | Mark slow tests |
| `pytest -m "not slow"` | Skip slow tests |
| `@patch()` | Mock functions and classes |
| `tmp_path` fixture | Automatic temp directory |
| `pytest --cov` | Generate coverage report |
| `assert` | Simple and readable assertions |

**Remember**: Tests are code too. Keep them clean, readable, and maintainable. Good tests catch bugs; great tests prevent them.
