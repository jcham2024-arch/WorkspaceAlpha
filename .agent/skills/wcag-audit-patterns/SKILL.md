---
tier: "experimental"
last_reviewed: 2026-11-10
source_url: ""
source_ref: ""
source_commit: ""
content_hash: "f9bdf8f50792e038ebd05f9ae317fffcde7b30675651b04f54482806b209bdda"
fetched_at: "2026-11-10"
upstream_license: "unknown"
owner: "taskmaster"
---
name: wcag-audit-patterns
description: "Comprehensive guide to auditing web content against WCAG 2.2 guidelines with actionable remediation strategies."
tier: "experimental"
risk: safe
source: community
date_added: "2026-02-27"
---


# WCAG Audit Patterns

Comprehensive guide to auditing web content against WCAG 2.2 guidelines with actionable remediation strategies.

## Use this skill when

- Conducting accessibility audits
- Fixing WCAG violations
- Implementing accessible components
- Preparing for accessibility lawsuits
- Meeting ADA/Section 508 requirements
- Achieving VPAT compliance

## Do not use this skill when

- You need legal advice or formal certification
- You only want a quick automated scan without manual verification
- You cannot access the UI or source for remediation work

## Instructions

1. Run automated scans (axe, Lighthouse, WAVE) to collect initial findings.
2. Perform manual checks (keyboard navigation, focus order, screen reader flows).
3. Map each issue to a WCAG criterion, severity, and remediation guidance.
4. Re-test after fixes and document residual risk and compliance status.

Refer to `resources/implementation-playbook.md` for detailed patterns, checklists, and templates.

## Safety

- Avoid claiming legal compliance without expert review.
- Keep evidence of test steps and results for audit trails.

## Resources

- `resources/implementation-playbook.md` for detailed patterns, checklists, and templates.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
