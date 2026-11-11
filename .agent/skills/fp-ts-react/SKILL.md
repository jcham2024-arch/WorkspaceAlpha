---
tier: "experimental"
last_reviewed: 2026-11-10
source_url: ""
source_ref: ""
source_commit: ""
content_hash: "4f0749c5231eca5280db66beb9a42206b7c94c8cb555256d4981cfc623abf3d5"
fetched_at: "2026-11-10"
upstream_license: "unknown"
owner: "taskmaster"
---
name: fp-ts-react
description: "Practical patterns for using fp-ts with React - hooks, state, forms, data fetching. Use when building React apps with functional programming patterns. Includes version-specific React patterns requiring project verification."
tier: "experimental"
risk: safe
source: "https://github.com/whatiskadudoing/fp-ts-skills"
date_added: "2026-02-27"
---


# Functional Programming in React

Practical patterns for React apps. Untested integration sketches; validate external JSON and request lifecycle behavior.

## Detailed Guide

Read [the detailed guide](references/detailed-guide.md) before executing this skill. It retains the complete procedure and reference material. Treat its safety, prerequisites, and validation requirements as mandatory. For focused work, load the relevant sections; for end-to-end work, read the guide completely.

## When to Use This Skill

- When building React apps with fp-ts for type-safe state management
- When handling loading/error/success states in data fetching
- When implementing form validation with error accumulation
- When using React 18/19 or Next.js 14/15 with functional patterns

---

## When to Use What

| Situation | Use |
|-----------|-----|
| Value might not exist | `Option<T>` |
| Operation might fail (sync) | `Either<E, A>` |
| Async operation might fail | `TaskEither<E, A>` |
| Need loading/error/success UI | `RemoteData<E, A>` |
| Form with multiple validations | `Either` with validation applicative |
| Dependency injection | Context + `ReaderTaskEither` |
| Prevent re-renders with fp-ts | `useMemo` or `fp-ts-react-stable-hooks` |

---

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
