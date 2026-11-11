---
name: rust-testing
description: Rust testing patterns including unit tests, integration tests, async testing, property-based testing, mocking, and coverage. Follows TDD methodology. Use when writing Rust tests — unit, integration, async, property-based, or coverage.
metadata:
  origin: ECC
---

# Rust Testing Patterns

Comprehensive Rust testing patterns for writing reliable, maintainable tests following TDD methodology.

## When to Use

- Writing new Rust functions, methods, or traits
- Adding test coverage to existing code
- Creating benchmarks for performance-critical code
- Implementing property-based tests for input validation
- Following TDD workflow in Rust projects

## How It Works

1. **Identify target code** — Find the function, trait, or module to test
2. **Write a test** — Use `#[test]` in a `#[cfg(test)]` module, rstest for parameterized tests, or proptest for property-based tests
3. **Mock dependencies** — Use mockall to isolate the unit under test
4. **Run tests (RED)** — Verify the test fails with the expected error
5. **Implement (GREEN)** — Write minimal code to pass
6. **Refactor** — Improve while keeping tests green
7. **Check coverage** — Use cargo-llvm-cov, target 80%+

## TDD Workflow for Rust

### The RED-GREEN-REFACTOR Cycle

```
RED     → Write a failing test first
GREEN   → Write minimal code to pass the test
REFACTOR → Improve code while keeping tests green
REPEAT  → Continue with next requirement
```

### Step-by-Step TDD in Rust



## Unit Tests

### Module-Level Test Organization


### Assertion Macros


## Error and Panic Testing

### Testing `Result` Returns


### Testing Panics


## Integration Tests

### File Structure


### Writing Integration Tests


## Async Tests

### With Tokio


## Test Organization Patterns

### Parameterized Tests with `rstest`


### Test Helpers


## Property-Based Testing with `proptest`

### Basic Property Tests


### Custom Strategies


## Mocking with `mockall`

### Trait-Based Mocking


## Doc Tests

### Executable Documentation


## Benchmarking with Criterion



## Test Coverage

### Running Coverage


### Coverage Targets

| Code Type | Target |
|-----------|--------|
| Critical business logic | 100% |
| Public API | 90%+ |
| General code | 80%+ |
| Generated / FFI bindings | Exclude |

## Testing Commands


## Best Practices

**DO:**
- Write tests FIRST (TDD)
- Use `#[cfg(test)]` modules for unit tests
- Test behavior, not implementation
- Use descriptive test names that explain the scenario
- Prefer `assert_eq!` over `assert!` for better error messages
- Use `?` in tests that return `Result` for cleaner error output
- Keep tests independent — no shared mutable state

**DON'T:**
- Use `#[should_panic]` when you can test `Result::is_err()` instead
- Mock everything — prefer integration tests when feasible
- Ignore flaky tests — fix or quarantine them
- Use `sleep()` in tests — use channels, barriers, or `tokio::time::pause()`
- Skip error path testing

## CI Integration


**Remember**: Tests are documentation. They show how your code is meant to be used. Write them clearly and keep them up to date.
