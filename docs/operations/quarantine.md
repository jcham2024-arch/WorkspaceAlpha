# Quarantine Ledger — Broken Skills

The master skill library (3,520 skills in `.agent/skills/`) imports from `.archive/` dump sources. Skills whose `SKILL.md` returns "404: Not Found" at the source are **quarantined** — they are not copied into `.agent/skills/` and must never appear in any active profile.

## Quarantine Registry

**File:** `.agent/quarantine/registry.json`  
**Format:** One entry per broken skill:
```json
{
  "id": "<skill-name>",
  "source": "<source-bucket>",
  "reason": "<why quarantined>",
  "date_quarantined": "<date>",
  "owner": "<who decided>"
}
```

**Current count:** 47 quarantined skills (see `INDEX.md` for the full import report).

## Intake Process

1. **Detect**: `import_all_skills.py` flags any `SKILL.md` starting with "404:" as broken
2. **Quarantine**: Skill is not copied to `.agent/skills/`; entry added to `registry.json`
3. **Report**: `IMPORT_REPORT.md` updated with count and first 20 names
4. **Review**: Skill owner investigates whether source can be fixed

## Review Process

A quarantined skill can be reviewed at any time:

1. Check if the source `SKILL.md` has been restored at the original bucket/path
2. If restored, re-run `python3 .agent/tools/import_all_skills.py`
3. If skill imports successfully, remove entry from `registry.json`
4. Re-run `validate.py` to confirm no active profile references it

## Un-Quarantine Process

1. Verify source `SKILL.md` is no longer "404: Not Found"
2. Remove entry from `.agent/quarantine/registry.json`
3. Re-run `import_all_skills.py` to import the skill into `.agent/skills/`
4. Re-run `validate.py` to confirm no issues
5. Optionally add to a profile's `skills:` list for provisioning

## Validator Check

`validate.py` includes a quarantine check: it fails if any quarantined skill ID appears in any active profile's frontmatter `skills:` list. This prevents accidentally provisioning a broken skill.

Run: `python3 validate.py`

## Links

- Registry: `.agent/quarantine/registry.json`
- Import report: `.agent/skills/IMPORT_REPORT.md`
- Quarantined skills: `.agent/skills/_quarantine/` (2 folders with 404 SKILL.md)
- Import script: `.agent/tools/import_all_skills.py`

---

*Edit `registry.json` to add/remove quarantined skills. Re-run `validate.py` after changes.*
