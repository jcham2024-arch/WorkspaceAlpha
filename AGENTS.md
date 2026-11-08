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
- `id` — stable identifier, also an anchor in `wiki/index.html`
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
`wiki/index.html#<node_id>`

Cite that anchor when reporting conclusions. The wiki is the human audit
surface; it is generated from the same graph, not maintained separately.
Do NOT edit `wiki/index.html` or `.context/manifest.json` — they are
build artifacts. To change knowledge, edit `docs/` and `.context/graph.json`,
then run `python3 seed.py && python3 build.py`.

## 5. Token budget

- Instructions and routing: 15% of window
- Task execution: 70%
- Verification reserve: 15%
- If a node's `bytes` exceeds 20% of your remaining budget, read its
  `summary` first and ask for authorization before hydrating.

## 6. Build commands (do not run unless asked)

```
python3 seed.py     # docs/ → graph.json (idempotent, preserves valid edges)
python3 build.py    # graph.json → manifest.json + wiki/index.html
```

## 7. What lives where

| Path | Purpose |
|---|---|
| `.context/graph.json` | Canonical DAG — source of truth |
| `.context/manifest.json` | Generated routing table (read this) |
| `.context/index.md` | Plain-file fallback index |
| `docs/` | Existing documentation — read via byte ranges only |
| `wiki/index.html` | Generated human wiki — do not edit |
| `AGENTS.md` | This file — entry router |

## 8. Non-negotiables

- Never modify files under `docs/` unless the task explicitly says to.
- Never modify `.context/graph.json` unless the task is "add a node/edge".
- Never modify `.context/manifest.json` or `wiki/index.html` — regenerate them.
- Cite `wiki/index.html#<node_id>` for every claim you derive from a node.

## 9. Skills

Local skills live in `.harness/skills/` (57 healthy skills, 1.7M).
Invoke one with skill_view(name="..."). The slim router is
`skills/index.json` (name + description + path only — never add
descriptions to the docs manifest). Archive provenance and trust
rules are in `docs/resources/README.md` (the 686M dump under
`.archive/` is NOT indexed; install one confirmed skill at a time).

| Path | Purpose |
|---|---|
| `.harness/skills/<name>/SKILL.md` | Canonical skill text (run/sync source) |
| `skills/index.json` | Slim skills router (regen: `.harness/gen_skills_index.py`) |
| `docs/resources/` | Archive provenance, trust tiers, PM shortlist |

Read `memory/learnings.md` at session start; append one line per
session on what you learned. Root map: `llms.txt` (agents) and
`README.md` (humans).

## 10. Agent layer (.agent/)

`.agent/` holds agent-side resources, tools, skills, and MCP. It
consumes the baselayer and never writes it (§9 contract in
`.agent/README.md`). It is gitignored (local example).

| Path | Purpose |
|---|---|
| `.agent/mcp/server.py` | MCP server (stdlib JSON-RPC stdio) |
| `.agent/tools/context.py` | compile_context / read_section core |
| `.agent/skills/<role>/<skill>/SKILL.md` | Role-owned skill packages |
| `.agent/profiles/*.md` | Specialized agents (orchestrator, researcher, builder, reviewer, operator) |
| `.agent/.env` | Keys (gitignored; template `.env.example`) |

Match each task to a profile in `.agent/profiles/README.md` and
state the match in the reply. Workflow stages are numbered folders:
`01-navigate/` → `02-plan/` → `03-execute/` → `04-verify/`, each
with a `PROMPT.md`. Follow them in order for non-trivial tasks.
