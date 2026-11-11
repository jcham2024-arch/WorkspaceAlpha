# Skill Tiering — WorkspaceAlpha

The master skill library (3,520 skills in `.agent/skills/`) uses an explicit four-tier
lifecycle so that "broken vs. not" is no longer the only distinction between skills.

## Tiers

| Tier | Meaning | Default-provisionable? | Reviewed? | Tested? |
|------|---------|----------------------|-----------|---------|
| **core** | Vetted, tested, in the starter set | Yes | Yes | Yes |
| **curated** | Reviewed, not default | No (on request) | Yes | Yes |
| **experimental** | Auto-sourced, unreviewed | No | No | No |
| **quarantine** | Broken (`SKILL.md` = "404: Not Found") | No | N/A | N/A |

## Promotion / Demotion Rules

| From → To | Rule |
|-----------|------|
| experimental → curated | Human review completes; skill passes `skill-check`; reviewer signs off |
| curated → core | Skill demonstrates repeated production use; added to starter profile or equivalent |
| experimental → quarantine | Skill found broken (`SKILL.md` = "404: Not Found") at import time |
| any → quarantine | Skill's `SKILL.md` returns "404: Not Found" or fails basic validation |
| quarantine → experimental | Source restored; skill re-imports successfully |

## Frontmatter Fields

Every skill's `SKILL.md` frontmatter must include:

```yaml
---
name: <skill-id>
description: <one-line purpose>
tier: core \| curated \| experimental \| quarantine
last_reviewed: YYYY-MM-DD
owner: <person-or-role>
---
```

Additional provenance fields (see `docs/operations/quarantine.md` and `ops/strategic-improvements` Task 6):

```yaml
source_url: <URL>
source_ref: <branch-or-tag>
source_commit: <sha>
content_hash: <sha256>
fetched_at: YYYY-MM-DD
upstream_license: <SPDX identifier>
```

## Validation Rules (enforced by `validate.py`)

1. **Every skill has a `tier:` field** — fail if missing.
2. **`core` skill must be tested** — fail if a `core` skill has no associated test coverage.
3. **`quarantine` skill in active profile** — fail if any active profile lists a `quarantine`-tier skill.
4. **`tier` value is valid** — must be one of `core`, `curated`, `experimental`, `quarantine`.

## Backfill

Skills without a `tier:` field are backfilled as `experimental`. Skills listed in the quarantine registry
(`.agent/quarantine/registry.json`) are set to `quarantine`. Skills in the starter profile
(`.agent/profiles/starter.md`) are `core` by default.
