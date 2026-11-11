# Deprecation Policy

How skills and profiles are retired without breaking harnesses.

## Tier Progression to Quarantine

| Stage | Tier | Notice Period | Action |
|-------|------|---------------|--------|
| Active | `core` / `curated` | — | Fully provisionable |
| Deprecated | `experimental` | None | Still usable, not default |
| Quarantined | `quarantine` | Immediate | Not provisionable; `SKILL.md` = "404: Not Found" |

## Deprecation Process

1. **Decide**: Maintainer decides a skill or profile should be retired
2. **Tier change**: Move skill from `core`/`curated` to `experimental` (demotion)
3. **Review period**: 30 days minimum — skill remains usable but not default-provisionable
4. **Quarantine**: Move skill to `quarantine` tier; add to `.agent/quarantine/registry.json`
5. **Archive**: Remove skill folder from `.agent/skills/` (after notice period)

## Profile Deprecation

Profiles follow the same pattern:
1. Add `status: deprecated` to profile frontmatter
2. 30-day notice period — profile still works but shows deprecation warning
3. Remove profile file from `.agent/profiles/`

## What Breaks

- **Harnesses referencing a quarantined skill**: `validate.py` fails if any active profile references a quarantine-tier skill
- **Harnesses referencing a removed profile**: `sync_active.py` fails with "unknown profile"
- **No silent breakage**: All deprecation is validated at build/provision time

## Links

- Quarantine registry: `.agent/quarantine/registry.json`
- Quarantine process: `docs/operations/quarantine.md`
- Tier definitions: `.agent/skills/TIERS.md`
- Skill lifecycle: `docs/operations/skill-lifecycle.md`
- Contract version: `docs/integration/harness-contract.md` (semver for breaking changes)

---

*Deprecation follows semver: removing a skill or profile is a breaking change requiring a major contract_version bump.*
