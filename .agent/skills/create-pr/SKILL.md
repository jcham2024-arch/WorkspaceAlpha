---
tier: "experimental"
last_reviewed: 2026-11-10
source_url: ""
source_ref: ""
source_commit: ""
content_hash: "53d4c59b50af4b696ed1c22c4e06e33c9723928d41c137bfc4cac26d43d9f1b2"
fetched_at: "2026-11-10"
upstream_license: "unknown"
owner: "taskmaster"
---
name: create-pr
description: Alias for pr-writer. Use when users explicitly ask for "create-pr" or reference the legacy skill name. Redirects to the canonical PR writing workflow.
tier: "experimental"
risk: critical
source: community
date_added: "2026-01-30"
---


# Alias: create-pr

This skill name is kept for compatibility.

## When to Use
- The user explicitly asks for `create-pr` or refers to the legacy skill name.
- You need to redirect pull request creation work to the canonical `pr-writer` workflow.
- The task is specifically about writing or updating a pull request rather than general git operations.

Use the available `pr-writer` skill as the canonical workflow for creating and editing pull requests. If the client requires qualified skill names, use the qualifier for the plugin that supplied this skill rather than assuming an external namespace.

Confirm that `pr-writer` is actually installed; otherwise report the dependency missing. Repository-native maintainer and merge rules still apply.

If invoked via `create-pr`, run the same workflow and conventions documented in `pr-writer`.

## Example

**User request:**

> Create a pull request for the current branch, follow the repository template, and include the validation results.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
