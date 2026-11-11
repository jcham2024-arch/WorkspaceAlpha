---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 7221feb3459e6b94a58086e6c3ba8f0cabeb8c9d3649de5c693ca807fbc84e1d
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
description: Modern Perl 5.36+ idioms, best practices, and conventions for building robust, maintainable Perl applications. Use when writing or reviewing modern Perl 5.36+ code.
name: perl-patterns
origin: ECC
---
# Modern Perl Development Patterns
Idiomatic Perl 5.36+ patterns and best practices for building robust, maintainable applications.
## When to Activate
- Writing new Perl code or modules
- Reviewing Perl code for idiom compliance
- Refactoring legacy Perl to modern standards
- Designing Perl module architecture
- Migrating pre-5.36 code to modern Perl
## How It Works
Apply these patterns as a bias toward modern Perl 5.36+ defaults: signatures, explicit modules, focused error handling, and testable boundaries. The examples below are meant to be copied as starting points, then tightened for the actual app, dependency stack, and deployment model in front of you.
## Core Principles
### 1. Use `v5.36` Pragma
A single `use v5.36` replaces the old boilerplate and enables strict, warnings, and subroutine signatures.
### 2. Subroutine Signatures
Use signatures for clarity and automatic arity checking.
### 3. Context Sensitivity
Understand scalar vs list context — a core Perl concept.
### 4. Postfix Dereferencing
Use postfix dereference syntax for readability with nested structures.
### 5. The `isa` Operator (5.32+)
Infix type-check — replaces `blessed($o) && $o->isa('X')`.
## Error Handling
### eval/die Pattern
### Try::Tiny (Reliable Exception Handling)
### Native try/catch (5.40+)
## Modern OO with Moo
Prefer Moo for lightweight, modern OO. Use Moose only when its metaprotocol is needed.
### Moo Roles
### Native `class` Keyword (5.38+, Corinna)
## Regular Expressions
### Named Captures and `/x` Flag
### Precompiled Patterns
## Data Structures
### References and Safe Deep Access
## File I/O
### Three-Argument Open
### Path::Tiny for File Operations
## Module Organization
### Standard Project Layout
### Exporter Patterns
## Tooling
### perltidy Configuration (.perltidyrc)
### perlcritic Configuration (.perlcriticrc)
### Dependency Management (cpanfile + carton)
## Quick Reference: Modern Perl Idioms
| Legacy Pattern | Modern Replacement |
|---|---|
| `use strict; use warnings;` | `use v5.36;` |
| `my ($x, $y) = @_;` | `sub foo($x, $y) { ... }` |
| `@{ $ref }` | `$ref->@*` |
| `%{ $ref }` | `$ref->%*` |
| `open FH, "< $file"` | `open my $fh, '<:encoding(UTF-8)', $file` |
| `blessed hashref` | `Moo` class with types |
| `$1, $2, $3` | `$+{name}` (named captures) |
| `eval { }; if ($@)` | `Try::Tiny` or native `try/catch` (5.40+) |
| `BEGIN { require Exporter; }` | `use Exporter 'import';` |
| Manual file ops | `Path::Tiny` |
| `blessed($o) && $o->isa('X')` | `$o isa 'X'` (5.32+) |
| `builtin::true / false` | `use builtin 'true', 'false';` (5.36+, experimental) |
## Anti-Patterns
**Remember**: Modern Perl is clean, readable, and safe. Let `use v5.36` handle the boilerplate, use Moo for objects, and prefer CPAN's battle-tested modules over hand-rolled solutions.