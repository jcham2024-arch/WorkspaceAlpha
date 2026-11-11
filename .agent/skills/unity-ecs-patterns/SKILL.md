---
tier: experimental
last_reviewed: 2026-11-10
content_hash: eed1625980f0374e7d17df622d2b7c36b37e15e2f75dfe59e3ee0248926d206b
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
date_added: 2026-02-27
description: Production patterns for Unity's Data-Oriented Technology Stack (DOTS) including Entity Component System, Job System, and Burst Compiler.
name: unity-ecs-patterns
risk: safe
source: community
---
# Unity ECS Patterns
Production patterns for Unity's Data-Oriented Technology Stack (DOTS) including Entity Component System, Job System, and Burst Compiler.
## Use this skill when
- Building high-performance Unity games
- Managing thousands of entities efficiently
- Implementing data-oriented game systems
- Optimizing CPU-bound game logic
- Converting OOP game code to ECS
- Using Jobs and Burst for parallelization
## Do not use this skill when
- The task is unrelated to unity ecs patterns
- You need a different domain or tool outside this scope
## Instructions
- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.
## Example
```text
Implement Speed plus a MovementSystem using the pinned Entities package. Profile a fixed entity cohort before/after; verify movement once per frame and job dependencies before enabling parallel execution.
```
## Resources
- `resources/implementation-playbook.md` for detailed patterns and examples.
## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.