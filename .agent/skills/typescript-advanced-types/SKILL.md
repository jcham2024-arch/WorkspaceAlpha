---
tier: "experimental"
last_reviewed: 2026-11-10
source_url: ""
source_ref: ""
source_commit: ""
content_hash: "f1855c56cbce51864f775239538f7a3a9983d28c8f5ec2cba7005f04706b96f7"
fetched_at: "2026-11-10"
upstream_license: "unknown"
owner: "taskmaster"
---
name: typescript-advanced-types
description: "Comprehensive guidance for mastering TypeScript's advanced type system including generics, conditional types, mapped types, template literal types, and utility types for building robust, type-safe applications."
tier: "experimental"
risk: safe
source: community
date_added: "2026-02-27"
---


# TypeScript Advanced Types

Comprehensive guidance for mastering TypeScript's advanced type system including generics, conditional types, mapped types, template literal types, and utility types for building robust, type-safe applications.

## Use this skill when

- Building type-safe libraries or frameworks
- Creating reusable generic components
- Implementing complex type inference logic
- Designing type-safe API clients
- Building form validation systems
- Creating strongly-typed configuration objects
- Implementing type-safe state management
- Migrating JavaScript codebases to TypeScript

## Do not use this skill when

- The task is unrelated to typescript advanced types
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

## Example

Use `Expect<AssertEqual<Result, Expected>>` for a positive type assertion and
`@ts-expect-error` for an intentional rejected call. Also validate API JSON at
runtime; a generic response type does not inspect the returned object.
