# Skill Lifecycle

Governance for the master skill library (`.agent/skills/`): tier promotion,
review cadence, and demotion rules.

## Tiers

Defined in `.agent/skills/TIERS.md`:

| Tier | Meaning | Default-provisionable? |
|------|---------|----------------------|
| **core** | Vetted, tested, in starter set | Yes |
| **curated** | Reviewed, not default | No (on request) |
| **experimental** | Auto-sourced, unreviewed | No |
| **quarantine** | Broken (`SKILL.md` = "404: Not Found") | No |

## Review Cadence

| Tier | Frequency | Owner |
|------|-----------|-------|
| **core** | Quarterly | Profile owner + conceptualizer |
| **curated** | Semi-annual | Profile owner |
| **experimental** | Ad-hoc (on use) | Skill author |
| **quarantine** | On source restore | taskmaster |

## Promotion / Demotion

| Transition | Rule | Required |
|------------|------|----------|
| experimental → curated | Human review completes; passes `skill-check`; reviewer signs off | Review + sign-off |
| curated → core | Demonstrated production use; added to starter profile | Starter profile update |
| any → quarantine | `SKILL.md` returns "404: Not Found" or fails validation | Automatic (import script) |
| quarantine → experimental | Source restored; skill re-imports successfully | Re-import + validation |

## Stale Skill Detection

Run `python3 tools/stale.py` to list skills unreviewed for > 180 days, grouped by tier.
Stale core skills are escalated for review; stale curated skills are flagged;
stale experimental skills may be demoted to quarantine.

## Tools

- `tools/backfill_tiers.py` — backfill `tier:` field (one-time migration)
- `tools/backfill_last_reviewed.py` — backfill `last_reviewed:` field (one-time migration)
- `tools/dedup.py` — find duplicate/overlapping skills (report only)
- `tools/stale.py` — list unreviewed skills by tier
- `validate.py` — enforces tier field presence, valid values, quarantine invariants

## Adding a New Skill

1. Create `.agent/skills/<name>/SKILL.md` with frontmatter including `tier:`, `last_reviewed:`, `owner:`
2. Default tier is `experimental`
3. Run `python3 validate.py` to confirm no violations
4. Promote to `curated` or `core` through the review process above
