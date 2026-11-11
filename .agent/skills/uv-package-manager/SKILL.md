---
tier: experimental
last_reviewed: 2026-11-10
content_hash: e6fe47ac090e8200ef2fce11478257ca16574fa746dc5d31463a4ab4e58b3e8d
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
date_added: 2026-02-27
description: Comprehensive guide to using uv, an extremely fast Python package installer and resolver written in Rust, for modern Python project management and dependency workflows.
name: uv-package-manager
risk: critical
source: community
---
# UV Package Manager
Comprehensive guide to using uv, an extremely fast Python package installer and resolver written in Rust, for modern Python project management and dependency workflows.
## Use this skill when
- Setting up new Python projects quickly
- Managing Python dependencies faster than pip
- Creating and managing virtual environments
- Installing Python interpreters
- Resolving dependency conflicts efficiently
- Migrating from pip/pip-tools/poetry
- Speeding up CI/CD pipelines
- Managing monorepo Python projects
- Working with lockfiles for reproducible builds
- Optimizing Docker builds with Python dependencies
## Do not use this skill when
- The task is unrelated to uv package manager
- You need a different domain or tool outside this scope
## Instructions
- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.
## Example
```bash
# Existing reviewed project: verify the lock before syncing.
uv lock --check
uv sync --locked
uv run --locked pytest
```
Inspect project build hooks/dependencies before installation or running code. Use an isolated environment and explicit authorization for downloads, installs and hook/config changes.
## Resources
- `resources/implementation-playbook.md` for detailed patterns and examples.
## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.