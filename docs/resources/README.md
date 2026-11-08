# Resources — Skills Archive Provenance

Archive status: the raw dump (.archive/Agentsandskills/, 686M,
3,510 sources) was imported into .agent/skills/ — 3,463 copied as
valid folders, 47 "404: Not Found" sources quarantined (see
.agent/skills/IMPORT_REPORT.md), indexed in .agent/skills/INDEX.md
+ INDEX.csv (3,520 folders). The archive was cleared after
verification; workspace shrank 689M → 157M. The dump itself was
never baselayer-indexed.

## Provenance

The dump aggregates 13 buckets (see .archive/Agentsandskills/agent.md
and .archive/Agentsandskills/AgentSkills/DATABASE.md for the full
inventory, which is stale — counts disagree across files, by-source/
lists only 6 of 13 buckets, harness-skills-names.txt lists 28 of 60
installed). Every SKILL.md keeps original frontmatter; nothing here
is rewritten. (The dump's OVERLAPS/INSTALLATION/DATABASE files are
no longer present post-clear; treat as historical notes.)

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

## How to use the master library

1. Search .agent/skills/INDEX.csv (skill_name, source bucket,
   imported folder, risk, status) for a skill; skill-picker routes
   by task once provisioned.
2. Provision one confirmed skill at a time into .harness/skills/
   via a profile's frontmatter + provision.py; never bulk-copy.
3. Check OVERLAPS-derived names: imported duplicates live under
   `<source>__<name>`; the flat curated copy wins for the plain name.
4. Re-run python3 .agent/tools/gen_skills_index.py to refresh
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
Keys live in .agent/.env (gitignored). See .agent/agent.md.
