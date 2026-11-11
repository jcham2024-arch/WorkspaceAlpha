# Security Checklist

Scope: security-checklist (agentic-awesome-skills__security-and-hardening).
Load when: you need the security-checklist (agentic-awesome-skills__security-and-hardening) detail described in SKILL.md.

## Contents

- Security Checklist

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Application security review checklist

## Inputs

Identify the feature, trust boundaries, stored data, external effects and authorization scope.

## Procedure and verification

Trace inputs to persistence and outputs. Enforce resource ownership independently from login; test another tenant and a denied role. Allowlist writable fields and response fields. Use parameterized queries and contextual output handling. For outbound URLs, consider resolution, redirects and network egress together. Inspect actual logs and errors for secrets. Test rejected requests for absence of side effects and record reproducible findings.

## Limitations

Use staging or local tests within authorization. A checklist does not prove every vulnerability absent. Keep server-side controls, rollback and any untested integration explicit.
