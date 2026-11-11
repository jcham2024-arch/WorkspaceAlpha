---
tier: experimental
last_reviewed: 2026-11-10
content_hash: a92bbb106290f3ed0de518f440c0ac8998370a93d83e6698d60e2b9fd2634904
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
date_added: 2026-02-27
description: Implement the minimal code needed to make failing tests pass in the TDD green phase.
name: tdd-workflows-tdd-green
risk: critical
source: community
---
# TDD Green Phase
Implement the smallest correct behavior for an agreed failing test while preserving existing requirements, security boundaries and interfaces. Read the bundled playbook as illustrative material, not an executable tool.
## Use this skill when
- Moving from red to green in a TDD cycle
- Implementing minimal behavior to satisfy tests
- You want to keep implementation intentionally simple
## Do not use this skill when
- You are refactoring for design or performance
- Tests are already passing and you need new requirements
- You need a full architectural redesign
## Instructions
1. Review failing tests and identify the smallest fix.
2. Implement the minimal change to pass the next test.
3. Run tests after each change to confirm progress.
4. Record shortcuts or debt for the refactor phase.
## Safety
- Avoid bypassing tests to make them pass.
- Keep changes scoped to the failing behavior only.
## Resources
- `resources/implementation-playbook.md` for detailed patterns and examples.
## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.