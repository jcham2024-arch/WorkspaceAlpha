# Starter Skill Set — Expansion Guide

The Baselayer workspace ships a **curated starter skill set** (12 skills) via the `starter` profile. The full master library (3,520 skills) remains available but is not the default.

## Starter Profile

**File:** `.agent/profiles/starter.md`  
**Skills:** 12 (all risk-safe)  
**Provision:** `python3 .harness/sync_active.py --profile starter`

| Skill | Purpose |
|-------|---------|
| `brainstorming` | Explore what the human actually wants before building |
| `writing-plans` | Write implementation plans for unfamiliar engineers |
| `thinking-first-principles` | Strip assumed constraints; rebuild from primitives |
| `thinking-margin-of-safety` | Size buffers under uncertainty |
| `skill-audit` | Pre-install security review of skills |
| `skill-check` | Validate skill structure against agentskills spec |
| `skill-gap-analysis` | Register capability gaps and plan remediation |
| `skill-host-compat` | Lint skill frontmatter for host-safe substitutions |
| `plan-canvas` | Present plans in a browser canvas for review |
| `plan-orchestrate` | Decompose plans into executable commands |
| `research-planning` | Generate structured research plans |
| `skill-comply` | Measure whether agents follow skills/rules/definitions |

## Expansion Path: Starter → Full Library

Expanding beyond the starter set requires explicit human approval. Follow this procedure:

### Step 1 — Review Available Skills

Browse the master library:

```bash
ls .agent/skills/          # All 3,520 skill folders
cat .agent/skills/CATEGORIZATION.md  # Categorization tally
```

### Step 2 — Select Additional Skills

Choose skills by task type/subtype from `CATEGORIZATION.md`. Avoid risk-flagged (`critical`/`offensive`) skills unless explicitly approved.

### Step 3 — Edit a Profile

Add skill names to a profile's frontmatter `skills:` list:

```yaml
skills:
  - brainstorming
  - writing-plans
  - <your-new-skill>
```

### Step 4 — Provision

```bash
python3 .harness/sync_active.py --profile <your-profile>
python3 .harness/gen_skills_index.py
```

### Step 5 — Verify

```bash
python3 validate.py
```

## "Provision One Skill" Example

```bash
# Add a single skill to an existing profile
# Edit .agent/profiles/conceptualizer.md frontmatter, add skill name
python3 .harness/sync_active.py --profile conceptualizer
python3 .harness/gen_skills_index.py
```

## What Stays

- Full master library: `.agent/skills/` (all 3,520 skills, untouched)
- Skill categorization: `.agent/skills/CATEGORIZATION.md`
- Broken/quarantined skills: `.agent/quarantine/registry.json`
- Provisioning bridge: `.harness/sync_active.py`

## What Changes

- Quickstart defaults to `starter` profile (not full library)
- `skills/index.json` reflects starter's 12 skills (not 3,520)
- `.harness/skills/` contains only starter skills (not full library)

---

*Edit `.agent/profiles/starter.md` to change the starter set. Re-run `sync_active.py --profile starter` after changes.*
