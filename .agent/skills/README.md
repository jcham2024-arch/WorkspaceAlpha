# Skills — Master Library + Selection Evals (3,520 folders, 154MB)

.agent/skills/ is the complete master library: the full import of the
.archive/Agentsandskills dump (3,510 sources → 3,463 imported; 47
broken quarantined; INDEX.md/INDEX.csv hold every row with source
bucket, imported folder, risk flag, and status).

- Curated 57 (1.6MB) live flat under their canonical names.
- Imported duplicates of curated names sit under
  `<source-bucket>__<name>` so provenance is never overwritten.
- 47 "404: Not Found" sources are NOT copied (see IMPORT_REPORT.md);
  re-source them before installing.
- Risk-flagged skills (critical / offensive) are imported but are
  never provisioned by default — an explicit per-profile decision.

Profiles in .agent/profiles/ dictate what gets provisioned into
.harness/skills/ (the currently used set) via:

    python3 .agent/tools/provision.py --profile <role>

Rules (see SKILL_AUTHORING.md — the master guidance):
- One folder per skill; frontmatter (<name>/SKILL.md) authoritative.
- Body < 500 lines; progressive disclosure (frontmatter always
  loaded, body on trigger, references on demand, one level deep).
- Keep descriptions < 60 words (they are Layer 1 — always loaded),
  body < ~1k tokens, references/ on demand (progressive disclosure).
- Install additional dump skills one at a time, diffed first
  (docs/resources/README.md).
- After provisioning, run: python3 .harness/gen_skills_index.py

## Skill-selection evals (one per profile)

Tune a skill's description until selection is reliable; that line
is Layer 1 and is load-bearing. Run after every index change and
log the outcome in memory/learnings.md.

| Profile | Eval prompt (task) | Expected skill |
|---|---|---|
| orchestrator | "Break this 5-step feature into parallelizable pieces" | dispatching-parallel-agents |
| coder | "The login test fails on expired tokens" | systematic-debugging |
| researcher | "Compare three message queues for our event pipeline" | tech-stack-evaluator |
| reviewer | "Our PR grew 800 lines — check it before merge" | requesting-code-review |
