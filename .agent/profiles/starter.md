---
name: starter
role: Curated starter skill set — 12 vetted skills for getting a new project up and running. Provision with: python3 .harness/sync_active.py --profile starter
model-tier: medium-thinking
stage: 01-navigate
skills:
  - brainstorming
  - writing-plans
  - thinking-first-principles
  - thinking-margin-of-safety
  - skill-audit
  - skill-check
  - skill-gap-analysis
  - skill-host-compat
  - plan-canvas
  - plan-orchestrate
  - research-planning
  - skill-comply
tools:
  - .agent/tools/context.py search
  - .agent/tools/context.py context
reads:
  - .context/manifest.json
  - skills/index.json
verify: "Starter provisions cleanly; all 12 skills active in .harness/skills/; risk-flagged skills excluded."
owner: "taskmaster"
---

# Starter — Curated Skill Set (12 skills)

A small, vetted entry point into the 3,520-skill master library. Intended for new projects and first-time users. Expand to the full library only with explicit approval.

## Included Skills

| # | Skill | Purpose | Risk |
|---|-------|---------|------|
| 1 | brainstorming | Find out what the human actually wants before anything gets built | safe |
| 2 | writing-plans | Write implementation plans for engineers who haven't seen the codebase | safe |
| 3 | thinking-first-principles | Separate physics from convention; rebuild from primitives | safe |
| 4 | thinking-margin-of-safety | Size buffers under uncertainty; not free slack for laziness | safe |
| 5 | skill-audit | Pre-install review: inspect skills for permissions, deps, suspicious behavior | safe |
| 6 | skill-check | Validate skills against the agentskills specification | safe |
| 7 | skill-gap-analysis | Register capability gaps; plan training or acquisition | safe |
| 8 | skill-host-compat | Lint skill frontmatter for Codex/Cursor-safe substitutions | safe |
| 9 | plan-canvas | Present plans in a browser canvas for human annotation and approval | safe |
| 10 | plan-orchestrate | Decompose plans into ECC slash commands per step | safe |
| 11 | research-planning | Generate structured research plans with methodology, structure, dependencies | safe |
| 12 | skill-comply | Measure whether agents actually follow skills, rules, and definitions | safe |

## Expansion Path

To expand beyond the starter set:

```bash
# 1. Review remaining skills in .agent/skills/ (3,508 skills)
# 2. Select additional skills by category/task type
# 3. Create or edit a profile's frontmatter skills list
# 4. Provision: python3 .harness/sync_active.py --profile <your-profile>
# 5. Approval: expanding beyond starter requires explicit human approval
```

**Risk-flagged skills** (critical/offensive) are NOT auto-provisioned. They require explicit profile approval before inclusion.

## Links

- Master library: `.agent/skills/` (3,520 skills)
- Full catalog: `.agent/skills/CATEGORIZATION.md`
- Broken/quarantined: `.agent/quarantine/registry.json`
- Provisioning script: `.harness/sync_active.py`
- Skill index: `skills/index.json`
