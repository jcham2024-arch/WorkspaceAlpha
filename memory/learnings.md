# Learnings

Persistent memory for this workspace. Append one line per session:
what was learned, in what context. Read this file at the start of
every session (see AGENTS.md §9).

## Entries

- 2026-11-07: Root BOOTSTRAPPER.md written (whole-system spec:
  directory contract, §3 pipeline, §4 skill authoring schema, §7
  build-from-scratch checklist). Skill lifecycle — new skills get
  audited, categorized, and provisioned via profiles.

- 2026-11-07: Baselayer bootstrapped; skills split into slim index
  (skills/index.json) because docs/skills catalog bloated manifest
  761 B → 148 KB. Layer-1 router must stay under ~15% of context.
- 2026-11-07: Three archive skills are broken at source (SKILL.md =
  "404: Not Found"): caveman, karpathy-coder, llm-cost-optimizer.
  Always verify disk state before trusting index counts.
- 2026-11-07: The .archive/ dump must never be git-added (686M).
  .agent/.env is gitignored; keys live there, not in chat or memory.
