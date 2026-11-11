---
tier: "experimental"
last_reviewed: 2026-11-10
source_url: ""
source_ref: ""
source_commit: ""
content_hash: "0cb6607b5a982554bfc5af35f74cc1b6b24b5de27392ab7f0a706eefdc1ac951"
fetched_at: "2026-11-10"
upstream_license: "unknown"
owner: "taskmaster"
---
name: kaizen
description: "Guide for continuous improvement, error proofing, and standardization. Use this skill when the user wants to improve code quality, refactor, or discuss process improvements."
tier: "experimental"
risk: critical
source: community
date_added: "2026-02-27"
---


# Kaizen: Continuous Improvement

## Detailed Guide

Read [the detailed guide](references/detailed-guide.md) before executing this skill. It retains the complete procedure and reference material. Treat its safety, prerequisites, and validation requirements as mandatory. For focused work, load the relevant sections; for end-to-end work, read the guide completely.

## When to Use
**Apply within the requested scope for:**

- Code implementation and refactoring
- Architecture and design decisions
- Process and workflow improvements
- Error handling and validation

**Philosophy:** Quality through incremental progress and prevention, not perfection through massive effort.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

## Example

When a total accepts `NaN`, add finite-number validation at its input boundary,
verify finite/negative cases, and review the small diff before broader refactoring.
Do not treat an example snippet as evidence that tests passed.
