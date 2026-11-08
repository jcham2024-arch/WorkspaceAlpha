# Resources — Skills Archive Provenance

Raw archive: .archive/Agentsandskills/ (10,052 files, 686M, 3,509
SKILL.md in dump/ across 13 buckets). Curated set: .harness/skills/
(57 healthy skills, 1.7M) + slim skills/index.json router.
The dump is NOT baselayer-indexed; this file is the routing surface
for the archive.

## Provenance

The dump aggregates 13 buckets (see .archive/Agentsandskills/agent.md
and .archive/Agentsandskills/AgentSkills/DATABASE.md for the full
inventory, which is stale — counts disagree across files, by-source/
lists only 6 of 13 buckets, harness-skills-names.txt lists 28 of 60
installed). Every SKILL.md keeps original frontmatter; nothing here
is rewritten.

Why is the dump not indexed?

- 136M of 150M is dump/agentic-awesome-skills (2,947 skills), with
  uniform frontmatter but no per-skill quality signal. Auto-ingesting
  it would swamp the router (3,509 nodes, most low-signal) and break
  the 150-line AGENTS.md token budget.
- Bulk install is prohibited by OVERLAPS.md / INSTALLATION.md.
  Install one skill at a time, diff it first.
- Trust spread: security-offensive skills (active-directory-attacks,
  windows-privilege-escalation, apk-reverse, XSS, api-fuzzing) carry
  risk: offensive/critical and impose their own confirmation gates.
  Never auto-install security skills, x402 (USDC payments, installed
  copy included), or any skill with executable scripts/ without
  review — scripts ship unsigned.
- License field is inconsistent (MIT in some, absent in others);
  external GitHub URL dependencies exist (e.g. aws-skills router).

Integrity findings

- 3 installed skills are broken at source (SKILL.md = "404: Not
  Found" in both .harness/skills and dump/): caveman, karpathy-coder,
  llm-cost-optimizer. Excluded from the workspace copy (57, not 60).
- caveman, karpathy-coder, llm-cost-optimizer names collide with
  healthy skills elsewhere (dump/ponytail has a real caveman pack;
  andrej-karpathy is the healthy Karpathy skill) — check OVERLAPS.md
  before installing any dump copy.
- agent.md count claims (60 vs 28 vs 27 installed, 3,405 vs 3,413
  vs 3,509 total, 14 sources for 13 buckets) are mutually inconsistent.
  Treat DATABASE.md/INDEX.csv as approximate; verify on disk.

## How to use the archive

1. skill-picker routes by task, or grep catalog/<domain>.md.
2. Never bulk-copy dump/ — copy one confirmed skill folder (SKILL.md
   plus scripts/references/assets) into .harness/skills/.
3. Check OVERLAPS.md for duplicate names before installing.
4. Re-run python3 .harness/gen_skills_index.py to refresh
   skills/index.json after adding skills, then rebuild.

## Buckets (rough size)

- agentic-awesome-skills 136M — 2,947 skills; weakest signal, biggest cost.
- ecc-skills 7.5M, ecc-agents-skills 1.1M — enterprise agent patterns.
- engineering-skills, research-skills, thinking-skills, browser-use,
  websearch-skills, self-improvement-skills, jdb-agentic-debugger,
  ponytail, superpowers, agent-skills — curated small sets.

## Agent layer

.agent/ holds the agent-side runtime: resources/, tools/, and mcp/.
They consume .context/manifest.json and never write it.
Keys live in .agent/.env (gitignored). See .agent/README.md.
