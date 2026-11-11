# AGENTS.md — Context Navigation Entry Point

This repository uses a DAG-routed documentation system. Follow this protocol.

## 1. Orientation

1. Identify target files or task archetype.
2. Read `.context/manifest.json` — the routing table.
3. Select nodes whose `summary` matches; follow `requires` edges transitively.
4. Do not browse `docs/` directly; hydrate by byte range only.

## 2. Chunk access

Every node carries: `id`, `sha256`, `byte_range`, `bytes`, `summary`, `content_ref`, `tags`. Read `summary` first; hydrate by reading `byte_range[0]` to `byte_range[1]`.

## 3. Missing context

If no node matches: record the gap under `doc_gap_detected` in your report. Do not invent rules.

## 4. Human audit surface

Every node has an anchor at `.wiki/index.html#<node_id>`. Do not edit `.wiki/index.html` or `.context/manifest.json` — regenerate via `python3 .wiki/seed.py && python3 .wiki/build.py`.

## 5. Token budget

Instructions ~15%, task execution ~70%, verification reserve ~15%.

## 6. Build

`python3 .wiki/seed.py && python3 .wiki/build.py && python3 validate.py`

## 7. What lives where

| Path | Purpose |
|------|---------|
| `.context/graph.json` | Canonical DAG — source of truth |
| `.context/manifest.json` | Generated routing table |
| `.context/prompt-graph.json` | Prompt DAG (Unified Prompt Stack) |
| `.context/index.md` | Plain-file fallback index |
| `docs/` | Baselayer-indexed docs (read via byte ranges) |
| `docs/specs/` | Technical specifications |
| `docs/contracts/` | Decision records, interfaces |
| `docs/operations/` | Operational docs |
| `docs/adr/` | Architecture Decision Records |
| `docs/skills/` | Skill documentation index |
| `.wiki/index.html` | Generated human wiki — do not edit |
| `wiki/` | Generated prompt wiki views |
| `.agent/skills/` | Master skill library (3,520 skills) |
| `.agent/profiles/` | 9 agent profiles (with tier field) |
| `.agent/tools/` | Pipeline, audit, knowledge, MCP |
| `.harness/skills/` | Currently-used set — provisioned per profile |
| `skills/index.json` | Slim skills router |
| `adapters/` | Model adapters (Unified Prompt Stack) |
| `assembly/` | DAG compiler (Unified Prompt Stack) |
| `envelope/` | Delegation envelopes (Unified Prompt Stack) |
| `schemas/` | JSON Schemas (Unified Prompt Stack) |
| `provenance/` | Per-turn provenance records (Unified Prompt Stack) |
| `validate.py` | Step-6 validator (pre-commit hook) |
| `memory/learnings.md` | Persistent learnings |

## 8. Agent layer (.agent/)

`.agent/` holds ALL agent resources. Profiles now include a `tier:` field.

| Path | Purpose |
|------|---------|
| `.agent/skills/<name>/SKILL.md` | Master skill library |
| `.agent/tools/run.py` | Pipeline runner |
| `.agent/tools/mcp/server.py` | MCP server (stdio JSON-RPC) |
| `.agent/profiles/*.md` | Agent roles — conceptualizer, taskmaster, coder, researcher, reviewer, managers |
| `.agent/tools/release.py` | Releases |
| `.agent/.env` | Keys (gitignored) |

Match each task to a profile in `.agent/profiles/README.md`.

## 9. Unified Prompt Stack (WA-UNIFIED-002)

Six-node DAG compiler on the baselayer: **Prompt DAG** → **Envelope schemas** → **Model Adapters** → **Provenance Recorder** → **Wiki Views**.

| Component | Path |
|-----------|------|
| Prompt DAG | `.context/prompt-graph.json` |
| Envelope schemas | `envelope/handoff-envelope.schema.json`, `envelope/return-envelope.schema.json` |
| DAG Compiler | `assembly/` (manifest_reader, slicer, budgeter, assembler) |
| Prompt Prefixes | `assembly/prefix/` (orchestrator, manager, production) |
| Model Adapters | `adapters/` (deepseek_v32, nemotron_35, dispatch) |
| Provenance Recorder | `provenance/recorder.py` |
| Wiki Views | `wiki/views/generator.py` |

## 10. New Tools

| Tool | Path |
|------|------|
| normalize_skills.py | `tools/normalize_skills.py` |
| cleanup_skills.py | `tools/cleanup_skills.py` |
| fix_double_separator.py | `tools/fix_double_separator.py` |
| fix_yaml_lists.py | `tools/fix_yaml_lists.py` |
| remove_empty_fields.py | `tools/remove_empty_fields.py` |
| fix_quoting.py | `tools/fix_quoting.py` |
| generate_skill_index.py | `tools/generate_skill_index.py` |
| find_duplicate_skills.py | `tools/find_duplicate_skills.py` |
| backfill_tiers.py | `tools/backfill_tiers.py` |
| backfill_last_reviewed.py | `tools/backfill_last_reviewed.py` |
| dedup.py | `tools/dedup.py` |
| stale.py | `tools/stale.py` |

Match each task to a profile in `.agent/profiles/README.md` and state the match in the reply.
