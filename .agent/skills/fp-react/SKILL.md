---
tier: experimental
last_reviewed: 2026-11-10
content_hash: bce52211fdfcf00a34f81ea6346204f12a35dbae71ce505a88fad21903298759
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
author: fp-ts-skills
date_added: 2026-01-30
description: Practical patterns for using fp-ts with React - hooks, state, forms, data fetching. Includes version-specific React examples; verify framework/client boundaries.
name: fp-react
risk: critical
source: community
tags: "[fp-ts, react, typescript, hooks, state-management, forms, data-fetching, remote-data, react-19, next-js]"
version: 2.0.0
---
# Functional Programming in React
Practical patterns for React apps. Untested integration sketches; decode external data and verify lifecycle behavior.
---
## Detailed Guide
Read [the detailed guide](references/detailed-guide.md) before executing this skill. It retains the complete procedure and reference material. Treat its safety, prerequisites, and validation requirements as mandatory. For focused work, load the relevant sections; for end-to-end work, read the guide completely.
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