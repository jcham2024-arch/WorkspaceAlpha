# Development Workflows

Scope: development_workflows (senior-fullstack).
Load when: you need the development_workflows (senior-fullstack) detail described in SKILL.md.

## Contents

- Development Workflows

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Implementation and verification workflow

Start with an acceptance example and a narrow code change. Identify the affected API consumers and database constraints. Add or adjust meaningful tests for permissions, domain rules and integration failure handling.

Run the actual project commands and retain their outcomes. A skipped test, missing integration or unavailable environment is unknown, not a pass. Use fixtures for local provider behavior and distinguish them from a real authorized provider operation.

Prepare schema migration and rollback instructions, deployment target and operational checks when the feature needs them. Review the concrete result before publication. Keep paid transactions, external messages and production deployment within the user's explicit authorization.
