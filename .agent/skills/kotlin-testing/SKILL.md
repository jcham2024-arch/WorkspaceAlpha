---
tier: "experimental"
last_reviewed: 2026-11-10
source_url: ""
source_ref: ""
source_commit: ""
content_hash: "cc4af22d87b46cbff3b6e0aa4677bf4261df071ee23183a9eccae7af7a3e7312"
fetched_at: "2026-11-10"
upstream_license: "unknown"
owner: "taskmaster"
---
name: kotlin-testing
description: Kotlin testing patterns with Kotest, MockK, coroutine testing, property-based testing, and Kover coverage. Follows TDD methodology with idiomatic Kotlin practices. Use when writing Kotlin tests with Kotest or MockK, or testing coroutines and checking coverage.
tier: "experimental"
metadata:
  origin: ECC
---


# Kotlin Testing Patterns

Comprehensive Kotlin testing patterns for writing reliable, maintainable tests following TDD methodology with Kotest and MockK.

## When to Use

- Writing new Kotlin functions or classes
- Adding test coverage to existing Kotlin code
- Implementing property-based tests
- Following TDD workflow in Kotlin projects
- Configuring Kover for code coverage

## How It Works

1. **Identify target code** — Find the function, class, or module to test
2. **Write a Kotest spec** — Choose a spec style (StringSpec, FunSpec, BehaviorSpec) matching the test scope
3. **Mock dependencies** — Use MockK to isolate the unit under test
4. **Run tests (RED)** — Verify the test fails with the expected error
5. **Implement code (GREEN)** — Write minimal code to pass the test
6. **Refactor** — Improve the implementation while keeping tests green
7. **Check coverage** — Run `./gradlew koverHtmlReport` and verify 80%+ coverage

## Examples

The following sections contain detailed, runnable examples for each testing pattern:

### Quick Reference

- **Kotest specs** — StringSpec, FunSpec, BehaviorSpec, DescribeSpec examples in [Kotest Spec Styles](#kotest-spec-styles)
- **Mocking** — MockK setup, coroutine mocking, argument capture in [MockK](#mockk)
- **TDD walkthrough** — Full RED/GREEN/REFACTOR cycle with EmailValidator in [TDD Workflow for Kotlin](#tdd-workflow-for-kotlin)
- **Coverage** — Kover configuration and commands in [Kover Coverage](#kover-coverage)
- **Ktor testing** — testApplication setup in [Ktor testApplication Testing](#ktor-testapplication-testing)

### TDD Workflow for Kotlin

#### The RED-GREEN-REFACTOR Cycle

```
RED     -> Write a failing test first
GREEN   -> Write minimal code to pass the test
REFACTOR -> Improve code while keeping tests green
REPEAT  -> Continue with next requirement
```

#### Step-by-Step TDD in Kotlin


### Kotest Spec Styles

#### StringSpec (Simplest)


#### FunSpec (JUnit-like)


#### BehaviorSpec (BDD Style)


#### DescribeSpec (RSpec Style)


### Kotest Matchers

#### Core Matchers


#### Custom Matchers


### MockK

#### Basic Mocking


#### Coroutine Mocking


#### Argument Capture


#### Spy and Partial Mocking


### Coroutine Testing

#### runTest for Suspend Functions


#### Testing Flows


#### TestDispatcher


### Property-Based Testing

#### Kotest Property Testing


#### Custom Generators


### Data-Driven Testing

#### withData in Kotest


### Test Lifecycle and Fixtures

#### BeforeTest / AfterTest


#### Kotest Extensions


### Kover Coverage

#### Gradle Configuration


#### Coverage Commands


#### Coverage Targets

| Code Type | Target |
|-----------|--------|
| Critical business logic | 100% |
| Public APIs | 90%+ |
| General code | 80%+ |
| Generated / config code | Exclude |

### Ktor testApplication Testing


### Testing Commands


### Best Practices

**DO:**
- Write tests FIRST (TDD)
- Use Kotest's spec styles consistently across the project
- Use MockK's `coEvery`/`coVerify` for suspend functions
- Use `runTest` for coroutine testing
- Test behavior, not implementation
- Use property-based testing for pure functions
- Use `data class` test fixtures for clarity

**DON'T:**
- Mix testing frameworks (pick Kotest and stick with it)
- Mock data classes (use real instances)
- Use `Thread.sleep()` in coroutine tests (use `advanceTimeBy`)
- Skip the RED phase in TDD
- Test private functions directly
- Ignore flaky tests

### Integration with CI/CD


**Remember**: Tests are documentation. They show how your Kotlin code is meant to be used. Use Kotest's expressive matchers to make tests readable and MockK for clean mocking of dependencies.

## Platform variants

OS-specific companions for this skill:

- [Android](platforms/android.md)
