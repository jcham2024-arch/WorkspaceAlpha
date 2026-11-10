# Decision: Q4 — Skill Categorization Schema Stability Guarantee

## Question

What stability guarantees does the skill categorization schema provide? Can categories, subtypes, levels, or OS variants be added/removed/renamed without breaking downstream tooling (provisioning, skill picker, index generation)?

## Chosen Value

**Schema versioning with additive-only changes to the canonical CSV.** The categorization schema (`CATEGORIZATION.csv` in `.agent/skills/`) is versioned. Only additive changes (new categories, subtypes, levels, OS values) are permitted without a major version bump. Renaming or removing existing values requires a major version increment and a migration plan.

## Approver

taskmaster (orchestration), conceptualizer (human-facing) — 2026-11-10

## Evidence

- Current categorization: 3,520 skills across 57 curated + 3,463 imported
- Categories: task_type (12), task_subtype (47), level (4), os (5: cross/android/windows/linux/mac)
- Provisioning script (`.harness/sync_active.py`) reads CSV columns by name
- Skill picker and index generator depend on column presence
- Python CSV `DictReader` tolerates extra columns but fails on missing columns

## Rationale

The categorization schema is a **contract between the master library and the provisioning pipeline**. Downstream consumers (provisioning, skill picker, index generator, audit tool) read the CSV by column name. Industry practice for such contracts:

1. **Additive changes are safe** — new enum values don't break readers
2. **Renames/removals are breaking** — readers reference values by string
3. **Versioning signals intent** — major version = breaking change, minor = additive
4. **Migration tooling required for breaking changes** — not optional

This mirrors semantic versioning for data contracts (cf. Protobuf, Avro, JSON Schema evolution rules).

## Constraint on Future Specs

- **Forbidden**: Removing or renaming any value in `task_type`, `task_subtype`, `level`, or `os` columns without a major version bump and migration script
- **Required**: New categories/subtypes/levels/OS values must be documented in the CSV header comment with addition date
- **Required**: `skill_manage` create/patch must validate against current schema version before accepting a skill
- **Required**: Provisioning script must log a warning (not fail) on unknown enum values to allow forward compatibility

## Links

- Spec: `docs/specs/skill-lifecycle-spec.md` (planned)
- Tracking: `open-questions.md` (Q4)
- Implementation: `.agent/skills/CATEGORIZATION.csv`, `.harness/sync_active.py`, `.agent/tools/gen_skills_index.py`

---

*Decision recorded 2026-11-10. Schema version starts at v1.0.0 (current).*
