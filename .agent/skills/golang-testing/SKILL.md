---
name: golang-testing
description: Go testing patterns including table-driven tests, subtests, benchmarks, fuzzing, and test coverage. Follows TDD methodology with idiomatic Go practices. Use when writing Go tests — table-driven cases, subtests, benchmarks, fuzzing, or coverage.
metadata:
  origin: ECC
---

# Go Testing Patterns

Comprehensive Go testing patterns for writing reliable, maintainable tests following TDD methodology.

## When to Activate

- Writing new Go functions or methods
- Adding test coverage to existing code
- Creating benchmarks for performance-critical code
- Implementing fuzz tests for input validation
- Following TDD workflow in Go projects

## TDD Workflow for Go

### The RED-GREEN-REFACTOR Cycle

```
RED     → Write a failing test first
GREEN   → Write minimal code to pass the test
REFACTOR → Improve code while keeping tests green
REPEAT  → Continue with next requirement
```

### Step-by-Step TDD in Go


## Table-Driven Tests

The standard pattern for Go tests. Enables comprehensive coverage with minimal code.


### Table-Driven Tests with Error Cases


## Subtests and Sub-benchmarks

### Organizing Related Tests


### Parallel Subtests


## Test Helpers

### Helper Functions


### Temporary Files and Directories


## Golden Files

Testing against expected output files stored in `testdata/`.


## Mocking with Interfaces

### Interface-Based Mocking


## Benchmarks

### Basic Benchmarks


### Benchmark with Different Sizes


### Memory Allocation Benchmarks


## Fuzzing (Go 1.18+)

### Basic Fuzz Test


### Fuzz Test with Multiple Inputs


## Test Coverage

### Running Coverage


### Coverage Targets

| Code Type | Target |
|-----------|--------|
| Critical business logic | 100% |
| Public APIs | 90%+ |
| General code | 80%+ |
| Generated code | Exclude |

### Excluding Generated Code from Coverage


## HTTP Handler Testing


## Testing Commands


## Best Practices

**DO:**
- Write tests FIRST (TDD)
- Use table-driven tests for comprehensive coverage
- Test behavior, not implementation
- Use `t.Helper()` in helper functions
- Use `t.Parallel()` for independent tests
- Clean up resources with `t.Cleanup()`
- Use meaningful test names that describe the scenario

**DON'T:**
- Test private functions directly (test through public API)
- Use `time.Sleep()` in tests (use channels or conditions)
- Ignore flaky tests (fix or remove them)
- Mock everything (prefer integration tests when possible)
- Skip error path testing

## Integration with CI/CD


**Remember**: Tests are documentation. They show how your code is meant to be used. Write them clearly and keep them up to date.
