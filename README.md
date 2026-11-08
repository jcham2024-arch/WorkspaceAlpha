# Baselayer Workspace

An offline, DAG-routed documentation workspace for agentic coding.
Two surfaces compiled from one canonical graph (`.context/graph.json`):
an offline HTML wiki for humans (`wiki/index.html`) and a token-efficient
router for agents (`AGENTS.md` + `.context/manifest.json`). Curated
agent skills (57) and a small MCP runtime layer sit on top; the 686M
raw skill archive is quarantined out of tree.

## Layout

| Path | Purpose |
|---|---|
| `AGENTS.md` | Agent router (read first) |
| `llms.txt` | Machine-readable map of the tree |
| `Baselayer.md` | Bootstrap spec (input, input only) |
| `seed.py` / `build.py` | Compiler: docs/ → graph → manifest + wiki |
| `.context/` | graph.json (source of truth), manifest.json, index.md |
| `docs/` | Baselayer-indexed docs (only tree seed scans) |
| `wiki/` | Generated human wiki (never hand-edit) |
| `.harness/skills/` | Currently-used set — provisioned per active profile |
| `skills/index.json` | Slim skills router (name + description + path) |
| `.agent/` | Agent runtime: master skills, 4 profiles (orchestrator/coder/researcher/reviewer), tools, provisioner, mcp/, .env (gitignored) |
| `.archive/` | Raw 686M archive (gitignored, never indexed) |
| `01-navigate/` … `04-verify/` | ICM stage folders (+ output contracts) |
| `validate.py` · `.githooks/` | Step-6 check + pre-commit hook |
| `memory/learnings.md` | Persistent learnings (append post-session) |

## Build

```bash
python3 seed.py     # docs/ → .context/graph.json (idempotent)
python3 build.py    # graph.json → manifest.json + wiki/index.html
python3 .harness/gen_skills_index.py   # after skill changes
```

Validated by the §3 Step-6 script in `Baselayer.md`. Python 3.14
verified; zero external dependencies at build time.

## Conventions

- `docs/` is read-only to the build; `graph.json` is the only writable
  knowledge file — edit docs or graph, then rebuild.
- Skills are one folder per name, `SKILL.md` frontmatter authoritative;
  descriptions are load-bearing (progressive disclosure Layer 1).
- Secrets live only in `.agent/.env` (gitignored); `.env.example` is the
  committed template.
- The `.archive/` dump is never indexed or bulk-installed; copy one
  confirmed skill at a time.
