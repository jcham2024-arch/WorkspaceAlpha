---
tier: experimental
last_reviewed: 2026-11-10
content_hash: cb3c7835c377acabc06921e5a95cf3e1f958c6f91cc08d4122d2697ed7585bdd
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
date_added: 2026-02-27
description: Architecture and integration patterns for React Native development with Expo, including navigation, state management, native modules, and offline-first architecture.
name: react-native-architecture
risk: safe
source: community
---
# React Native Architecture
Architecture and integration patterns for React Native development with Expo, including navigation, state management, native modules, and offline-first architecture.
## Use this skill when
- Starting a new React Native or Expo project
- Implementing complex navigation patterns
- Integrating native modules and platform APIs
- Building offline-first mobile applications
- Optimizing React Native performance
- Setting up CI/CD for mobile releases
## Do not use this skill when
- The task is unrelated to react native architecture
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
For a catalog app, cache public product reads offline, keep session tokens in
platform secure storage, and block offline purchases until an idempotent order
outbox and server reconciliation are implemented.