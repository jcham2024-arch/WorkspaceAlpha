---
tier: "experimental"
last_reviewed: 2026-11-10
source_url: ""
source_ref: ""
source_commit: ""
content_hash: "488f5a04e532a7d3c05ffd39c609bed7df328a03ad4117c0bb11cb8a78059814"
fetched_at: "2026-11-10"
upstream_license: "unknown"
owner: "taskmaster"
---
name: concise-planning
description: "Use when a user asks for a plan for a coding task, to generate a clear, actionable, and atomic checklist."
tier: "experimental"
risk: safe
source: community
date_added: "2026-02-27"
---


# Concise Planning

## Goal

Turn a user request into a **single, actionable plan** with atomic steps.

## Workflow

### 1. Scan Context

- Read `README.md`, docs, and relevant code files.
- Identify constraints (language, frameworks, tests).

### 2. Minimal Interaction

- Ask **at most 1–2 questions** and only if truly blocking.
- Make reasonable assumptions for non-blocking unknowns.

### 3. Generate Plan

Use the following structure:

- **Approach**: 1-3 sentences on what and why.
- **Scope**: Bullet points for "In" and "Out".
- **Action Items**: A list sized to the actual task, with atomic, ordered actions (Verb-first).
- **Validation**: At least one item for testing.

## Plan Template

```markdown
# Plan

<High-level approach>

## Scope

- In:
- Out:

## Action Items

- [ ] <Step 1: Discovery>
- [ ] <Step 2: Implementation>
- [ ] <Step 3: Implementation>
- [ ] <Step 4: Validation/Testing>
- [ ] <Step 5: Rollout/Commit>

## Open Questions

- <Question 1 (max 3)>
```

## Checklist Guidelines

- **Atomic**: Each step should be a single logical unit of work.
- **Verb-first**: "Add...", "Refactor...", "Verify...".
- **Concrete**: Name specific files or modules when possible.

## When to Use
Use when the user asks for a coding plan and the outcome, scope, dependencies and verification should become a short ordered checklist.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
