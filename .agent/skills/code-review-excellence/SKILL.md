---
tier: "experimental"
last_reviewed: 2026-11-10
source_url: ""
source_ref: ""
source_commit: ""
content_hash: "ab8d94e78096638d88d7e4e743e18c995d47ab5a84f3c6de749104a221a6c5d9"
fetched_at: "2026-11-10"
upstream_license: "unknown"
owner: "taskmaster"
---
name: code-review-excellence
description: "Transform code reviews from gatekeeping to knowledge sharing through constructive feedback, systematic analysis, and collaborative improvement."
tier: "experimental"
risk: safe
source: community
date_added: "2026-02-27"
---


# Code Review Excellence

Transform code reviews from gatekeeping to knowledge sharing through constructive feedback, systematic analysis, and collaborative improvement.

## Use this skill when

- Reviewing pull requests and code changes
- Establishing code review standards
- Mentoring developers through review feedback
- Auditing for correctness, security, or performance

## Do not use this skill when

- There are no code changes to review
- The task is a design-only discussion without code
- You need to implement fixes instead of reviewing

## Instructions

- Read context, requirements, and test signals first.
- Review for correctness, security, performance, and maintainability.
- Provide actionable feedback with severity and rationale.
- Ask clarifying questions when intent is unclear.
- If detailed checklists are required, open `resources/implementation-playbook.md`.

## Output Format

- High-level summary of findings
- Issues grouped by severity (blocking, important, minor)
- Suggestions and questions
- Test and coverage notes

## Resources

- `resources/implementation-playbook.md` for detailed review patterns and templates.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
