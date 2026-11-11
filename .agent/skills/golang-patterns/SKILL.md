---
name: golang-patterns
description: Idiomatic Go patterns, best practices, and conventions for building robust, efficient, and maintainable Go applications. Use when writing or reviewing Go code and idiomatic structure or conventions are in question.
metadata:
  origin: ECC
---

# Go Development Patterns

Idiomatic Go patterns and best practices for building robust, efficient, and maintainable applications.

## When to Activate

- Writing new Go code
- Reviewing Go code
- Refactoring existing Go code
- Designing Go packages/modules

## Core Principles

### 1. Simplicity and Clarity

Go favors simplicity over cleverness. Code should be obvious and easy to read.


### 2. Make the Zero Value Useful

Design types so their zero value is immediately usable without initialization.


### 3. Accept Interfaces, Return Structs

Functions should accept interface parameters and return concrete types.


## Error Handling Patterns

### Error Wrapping with Context


### Custom Error Types


### Error Checking with errors.Is and errors.As


### Never Ignore Errors


## Concurrency Patterns

### Worker Pool


### Context for Cancellation and Timeouts


### Graceful Shutdown


### errgroup for Coordinated Goroutines


### Avoiding Goroutine Leaks


## Interface Design

### Small, Focused Interfaces


### Define Interfaces Where They're Used


### Optional Behavior with Type Assertions


## Package Organization

### Standard Project Layout


### Package Naming


### Avoid Package-Level State


## Struct Design

### Functional Options Pattern


### Embedding for Composition


## Memory and Performance

### Preallocate Slices When Size is Known


### Use sync.Pool for Frequent Allocations


Never return or retain `buf.Bytes()` from a pooled buffer past `Put`: copy it, or let the caller pass in an `io.Writer` so no copy is needed.

### Avoid String Concatenation in Loops


## Go Tooling Integration

### Essential Commands


### Recommended Linter Configuration (.golangci.yml)


## Quick Reference: Go Idioms

| Idiom | Description |
|-------|-------------|
| Accept interfaces, return structs | Functions accept interface params, return concrete types |
| Errors are values | Treat errors as first-class values, not exceptions |
| Don't communicate by sharing memory | Use channels for coordination between goroutines |
| Make the zero value useful | Types should work without explicit initialization |
| A little copying is better than a little dependency | Avoid unnecessary external dependencies |
| Clear is better than clever | Prioritize readability over cleverness |
| gofmt is no one's favorite but everyone's friend | Always format with gofmt/goimports |
| Return early | Handle errors first, keep happy path unindented |

## Anti-Patterns to Avoid


**Remember**: Go code should be boring in the best way - predictable, consistent, and easy to understand. When in doubt, keep it simple.
