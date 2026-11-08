# Decisions

ADR-lite: decision + context + rationale. Append-only.

## Entries

- 2026-11-07 | decision: .agent/ is the master folder, .harness/ is the active set | tags: skills,provisioning
  Rationale: profiles dictate per-role skill lists; the full master
  (3,520 skills) lives in .agent/skills and only a role's slice
  ever reaches .harness/skills.
