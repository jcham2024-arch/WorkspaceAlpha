---
name: python-patterns
description: Pythonic idioms, PEP 8 standards, type hints, and best practices for building robust, efficient, and maintainable Python applications. Use when writing or reviewing Python code and idiomatic structure, typing, or PEP 8 is in question.
metadata:
  origin: ECC
---

# Python Development Patterns

Idiomatic Python patterns and best practices for building robust, efficient, and maintainable applications.

## When to Activate

- Writing new Python code
- Reviewing Python code
- Refactoring existing Python code
- Designing Python packages/modules

## Core Principles

### 1. Readability Counts

Python prioritizes readability. Code should be obvious and easy to understand.


### 2. Explicit is Better Than Implicit

Avoid magic; be clear about what your code does.


### 3. EAFP - Easier to Ask Forgiveness Than Permission

Python prefers exception handling over checking conditions.


## Type Hints

### Basic Type Annotations


### Modern Type Hints (Python 3.9+)


### Type Aliases and TypeVar


### Protocol-Based Duck Typing


## Error Handling Patterns

### Specific Exception Handling


### Exception Chaining


### Custom Exception Hierarchy


## Context Managers

### Resource Management


### Custom Context Managers


### Context Manager Classes


## Comprehensions and Generators

### List Comprehensions


### Generator Expressions


### Generator Functions


## Data Classes and Named Tuples

### Data Classes


### Data Classes with Validation


### Named Tuples


## Decorators

### Function Decorators


### Parameterized Decorators


### Class-Based Decorators


## Concurrency Patterns

### Threading for I/O-Bound Tasks


### Multiprocessing for CPU-Bound Tasks


### Async/Await for Concurrent I/O


## Package Organization

### Standard Project Layout

```
myproject/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── main.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── user.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api.py
│   └── test_models.py
├── pyproject.toml
├── README.md
└── .gitignore
```

### Import Conventions


### __init__.py for Package Exports


## Memory and Performance

### Using __slots__ for Memory Efficiency


### Generator for Large Data


### Avoid String Concatenation in Loops


## Python Tooling Integration

### Essential Commands


### pyproject.toml Configuration


## Quick Reference: Python Idioms

| Idiom | Description |
|-------|-------------|
| EAFP | Easier to Ask Forgiveness than Permission |
| Context managers | Use `with` for resource management |
| List comprehensions | For simple transformations |
| Generators | For lazy evaluation and large datasets |
| Type hints | Annotate function signatures |
| Dataclasses | For data containers with auto-generated methods |
| `__slots__` | For memory optimization |
| f-strings | For string formatting (Python 3.6+) |
| `pathlib.Path` | For path operations (Python 3.4+) |
| `enumerate` | For index-element pairs in loops |

## Anti-Patterns to Avoid


__Remember__: Python code should be readable, explicit, and follow the principle of least surprise. When in doubt, prioritize clarity over cleverness.
