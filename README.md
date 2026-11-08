# Baselayer Workspace

An offline, DAG-routed documentation workspace for agentic coding.
Two surfaces compiled from one canonical graph (`.context/graph.json`):
an offline HTML wiki for humans (`.wiki/index.html`) and a token-efficient
router for agents (`AGENTS.md` + `.context/manifest.json`). A 3,520-skill
master library (`.agent/skills/`, categorized by task type/subtype)
and a small MCP runtime layer sit on top; the 686M raw archive was
absorbed into the master and cleared.

## Layout

| Path | Purpose |
|---|---|
| `AGENTS.md` | Agent router (read first) |
| `llms.txt` | Machine-readable map of the tree |
| `Baselayer.md` | Bootstrap spec (input, input only) |
| `seed.py` / `build.py` (.wiki/) | Compiler: docs/ → graph → manifest + wiki |
| `.context/` | graph.json (source of truth), manifest.json, index.md |
| `docs/` | Baselayer-indexed docs (only tree seed scans) |
| `wiki/` | Generated human wiki (never hand-edit) |
| `.harness/skills/` | Currently-used set — provisioned per active profile |
| `skills/index.json` | Slim skills router (name + description + path) |
| `.agent/` | Agent runtime: master skills (3,520), 9 profiles (human-facing conceptualizer ↔ protocol ↔ subagent-facing taskmaster, coder, researcher, reviewer, + 3 domain managers, + wiki-producer), tools, provisioner, mcp/, .env (gitignored) |
| `.wiki/` | Render pipeline: seed.py + build.py + index.html, and `.wiki/agent.md` (wiki production guide) |
| `.archive/` | Cleared after full import (gitignored) |
| `01-navigate/` … `04-verify/` | ICM stage folders (+ output contracts) |
| `validate.py` · `.githooks/` | Step-6 check + pre-commit hook |
| `memory/learnings.md` | Persistent learnings (append post-session) |

## Build

```bash
python3 .wiki/seed.py   # docs/ → .context/graph.json (idempotent)
python3 .wiki/build.py  # graph.json → manifest.json + .wiki/index.html
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
- The master library (3,520 skills) is categorized in
  `.agent/skills/CATEGORIZATION.md`; the 47 broken sources are
  quarantined in IMPORT_REPORT.md; bulk-installing is prohibited.
