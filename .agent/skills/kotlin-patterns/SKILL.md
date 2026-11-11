---
tier: "experimental"
last_reviewed: 2026-11-10
source_url: ""
source_ref: ""
source_commit: ""
content_hash: "5522b79771483b9b05046099c10780dc11c0df8ba63de37cad7991b356d4fee3"
fetched_at: "2026-11-10"
upstream_license: "unknown"
owner: "taskmaster"
---
name: kotlin-patterns
description: Idiomatic Kotlin patterns, best practices, and conventions for building robust, efficient, and maintainable Kotlin applications with coroutines, null safety, and DSL builders. Use when writing or reviewing Kotlin code and idiomatic structure or null safety is in question.
tier: "experimental"
metadata:
  origin: ECC
---


# Kotlin Development Patterns

Idiomatic Kotlin patterns and best practices for building robust, efficient, and maintainable applications.

## When to Use

- Writing new Kotlin code
- Reviewing Kotlin code
- Refactoring existing Kotlin code
- Designing Kotlin modules or libraries
- Configuring Gradle Kotlin DSL builds

## How It Works

This skill enforces idiomatic Kotlin conventions across seven key areas: null safety using the type system and safe-call operators, immutability via `val` and `copy()` on data classes, sealed classes and interfaces for exhaustive type hierarchies, structured concurrency with coroutines and `Flow`, extension functions for adding behaviour without inheritance, type-safe DSL builders using `@DslMarker` and lambda receivers, and Gradle Kotlin DSL for build configuration.

## Examples

**Null safety with Elvis operator:**

**Sealed class for exhaustive results:**

**Structured concurrency with async/await:**

## Core Principles

### 1. Null Safety

Kotlin's type system distinguishes nullable and non-nullable types. Leverage it fully.


### 2. Immutability by Default

Prefer `val` over `var`, immutable collections over mutable ones.


### 3. Expression Bodies and Single-Expression Functions

Use expression bodies for concise, readable functions.


### 4. Data Classes for Value Objects

Use data classes for types that primarily hold data.


## Sealed Classes and Interfaces

### Modeling Restricted Hierarchies


### Sealed Interfaces for API Responses


## Scope Functions

### When to Use Each


### Anti-Patterns


## Extension Functions

### Adding Functionality Without Inheritance


## Coroutines

### Structured Concurrency


### Flow for Reactive Streams


### Cancellation and Cleanup


## Delegation

### Property Delegation


### Interface Delegation


## DSL Builders

### Type-Safe Builders


### Configuration DSL


## Sequences for Lazy Evaluation


## Gradle Kotlin DSL

### build.gradle.kts Configuration


## Error Handling Patterns

### Result Type for Domain Operations


### require, check, error


## Collection Operations

### Idiomatic Collection Processing


## Quick Reference: Kotlin Idioms

| Idiom | Description |
|-------|-------------|
| `val` over `var` | Prefer immutable variables |
| `data class` | For value objects with equals/hashCode/copy |
| `sealed class/interface` | For restricted type hierarchies |
| `value class` | For type-safe wrappers with zero overhead |
| Expression `when` | Exhaustive pattern matching |
| Safe call `?.` | Null-safe member access |
| Elvis `?:` | Default value for nullables |
| `let`/`apply`/`also`/`run`/`with` | Scope functions for clean code |
| Extension functions | Add behavior without inheritance |
| `copy()` | Immutable updates on data classes |
| `require`/`check` | Precondition assertions |
| Coroutine `async`/`await` | Structured concurrent execution |
| `Flow` | Cold reactive streams |
| `sequence` | Lazy evaluation |
| Delegation `by` | Reuse implementation without inheritance |

## Anti-Patterns to Avoid


**Remember**: Kotlin code should be concise but readable. Leverage the type system for safety, prefer immutability, and use coroutines for concurrency. When in doubt, let the compiler help you.

## Platform variants

OS-specific companions for this skill:

- [Android](platforms/android.md)
