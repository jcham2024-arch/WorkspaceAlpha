# AGENTS.md — Context Navigation Entry Point

This repository uses a DAG-routed documentation system. You are not expected
to grep, search, or read documentation files wholesale. Follow this protocol.

## 1. Orientation (read once per task)

1. Identify the **target files** or **task archetype** for the current task.
2. Read `.context/manifest.json` — it is small, and it is the routing table.
3. Select the nodes whose `summary` matches the task. Follow `requires`
   edges transitively. Stop when no further `requires` edges are relevant.
4. Do not browse `docs/` directly. Do not `grep` for content. Do not read
   whole files to find one section.

## 2. Chunk access (section-level, never file-level)

Every node in the manifest carries:
- `id` — stable identifier, also an anchor in `.wiki/index.html`
- `sha256` — content hash for provenance
- `byte_range` — exact slice of the source file
- `bytes` — size of the section
- `summary` — one-line orientation

Use `summary` first. Hydrate the section only when the summary is
insufficient. To hydrate, read exactly `byte_range[0]` through
`byte_range[1]` from `content_ref`. Never read the whole file.

## 3. Missing context

If no node matches a rule you need:
- Do NOT invent a rule. Do NOT search the web to fill the gap.
- Record the gap explicitly in your final report under `doc_gap_detected`.
- The human operator will convert the gap into a new node in
  `.context/graph.json` on the next build.

## 4. Human audit surface

Every node you receive has an anchor in the offline wiki at:
`.wiki/index.html#<node_id>`

Cite that anchor when reporting conclusions. The wiki is the human audit
surface; it is generated from the same graph, not maintained separately.
Do NOT edit `.wiki/index.html` or `.context/manifest.json` — they are
build artifacts. To change knowledge, edit `docs/` and `.context/graph.json`,
then run `python3 .wiki/seed.py && python3 .wiki/build.py`.

## 5. Token budget

- Instructions and routing: 15% of window
- Task execution: 70%
- Verification reserve: 15%
- If a node's `bytes` exceeds 20% of your remaining budget, read its
  `summary` first and ask for authorization before hydrating.

## 6. Build commands (do not run unless asked)

```
python3 .wiki/seed.py   # docs/ → graph.json (idempotent, preserves valid edges)
python3 .wiki/build.py  # graph.json → manifest.json + .wiki/index.html
python3 validate.py # §3 Step-6 check (also pre-commit hook)
python3 .harness/gen_skills_index.py   # after skill changes
python3 .agent/tools/audit.py         # skill schema compliance (exit 1 on failure)
python3 .agent/tools/run.py build      # all of the above in one command
```

## 7. What lives where

| Path | Purpose |
|---|---|
| `.context/graph.json` | Canonical DAG — source of truth |
| `.context/manifest.json` | Generated routing table (read this) |
| `.context/index.md` | Plain-file fallback index |
| `docs/` | Existing documentation — read via byte ranges only |
| `.wiki/index.html` | Generated human wiki — do not edit |
| `validate.py` | Step-6 validator (also wired as pre-commit hook) |
| `.harness/skills/` | Currently-used set — provisioned per active profile |
| `.agent/` | Agent runtime: master skills, 8 profiles, tools, MCP (gitignored) |
| `.archive/` | Cleared after full import (gitignored) |
| `01-navigate/` … `04-verify/` | ICM stage folders (+ output contracts) |
| `memory/learnings.md` | Persistent learnings (append post-session) |
| `AGENTS.md` | This file — entry router |

## 8. Non-negotiables

- Never modify files under `docs/` unless the task explicitly says to.
- Never modify `.context/graph.json` unless the task is "add a node/edge".
- Never modify `.context/manifest.json` or `.wiki/index.html` — regenerate them.
- Cite `.wiki/index.html#<node_id>` for every claim you derive from a node.

## 9. Skills

`.harness/skills/` is the currently-used set, provisioned per active
profile (default: conceptualizer, 4 skills). Master library lives at
`.agent/skills/` (3,520 skills: 57 curated + 3,463 imported;
categorized by task type/subtype/level/os in CATEGORIZATION.csv;
platform variants in PLATFORMS.md + platforms/). Invoke
one with skill_view(name="...").
The slim router is `skills/index.json` (name + description + path
only — never add descriptions to the docs manifest). Archive
provenance/trust rules are in `docs/resources/README.md` (archive
absorbed and cleared after full import; bulk-install is prohibited).

| `.agent/skills/<name>/SKILL.md` | Master library (3,520 skills) |
| `.harness/skills/<name>/SKILL.md` | Currently-used set (provisioned) |
| `skills/index.json` | Slim router (regen: `gen_skills_index.py`) |

Provisioning: `python3 .agent/tools/provision.py --profile <name>`
syncs `.harness/skills/` to the profile's declared skills.

Read `memory/learnings.md` at session start (knowledge detail in §10).

## 10. Knowledge system (memory/)

Persistent knowledge (human Markdown is the truth; index is generated):

| File | Kind | Write when |
|---|---|---|
| `memory/JOURNAL.md` | work | task finishes (stage 04) |
| `memory/ERRORS.md` | error | failure diagnosed |
| `memory/LESSONS.md` | lesson | principle emerges |
| `memory/DECISIONS.md` | decision | trade-off settled |
| `memory/learnings.md` | session bullets | session ends |

Procedure (stage 04): `python3 .agent/tools/knowledge.py add --kind
{work,error,lesson,decision} --title "..." [--tags ...] [--body "..."]`
(appends AND syncs `.context/knowledge.db` + `memory/index.json`).
Query: `knowledge.py search <words>` / `last --kind work -n 5`.
Search this memory before planning; cite file + date.

## 11. Agent layer (.agent/)

`.agent/` holds ALL agent resources: the master skill library,
tools, MCP, and the specialized agent profiles. A profile's
frontmatter `skills:` list decides what gets provisioned.

| Path | Purpose |
|---|---|
| `.agent/skills/<name>/SKILL.md` | Master skill library (3,520: 57 curated + 3,463 imported) |
| `.agent/tools/provision.py` | Profile → `.harness/skills/` sync |
| `.agent/tools/mcp/server.py` | MCP server (stdlib JSON-RPC stdio) |
| `.agent/tools/context.py` | compile_context / read_section core |
| `.agent/profiles/*.md` | Specialized agents — human-facing conceptualizer ↔ protocol ↔ subagent-facing taskmaster (incl. planning + supervision), then coder, researcher, reviewer, plus research-manager, coding-manager, review-manager, and wiki-producer (human HTML production, matched from `.wiki/agent.md`) |
| `.agent/.env` | Keys (gitignored; template `.env.example`) |
| `BOOTSTRAPPER.md` | Whole-system build spec (system, structure, conventions, skill lifecycle) |

Match each task to a profile in `.agent/profiles/README.md` and
state the match in the reply. Workflow stages are numbered folders:
`01-navigate/` → `02-plan/` → `03-execute/` → `04-verify/`, each
with a `PROMPT.md` plus an output contract (`targets.md`, `plan.md`,
`changes.md`, `verification.md`). Follow them in order.
