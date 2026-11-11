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
| `BOOTSTRAPPER.md` | Whole-system build spec (current system, structure, conventions) |
| `llms.txt` | Machine-readable map of the tree |
| `Baselayer.md` | Bootstrap spec (input, input only) |
| `seed.py` / `build.py` (.wiki/) | Compiler: docs/ → graph → manifest + wiki |
| `.context/` | graph.json (source of truth), manifest.json, index.md |
| `docs/` | Baselayer-indexed docs (only tree seed scans) |
| `docs/architecture.md` | Architecture diagram (ASCII) |
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
python3 .agent/tools/gen_skills_index.py   # after skill changes
```

## 5-Minute Quickstart

1. **Clone** the repo and `cd` into it.
2. **Bootstrap** the baselayer:

   ```bash
   python3 .wiki/seed.py && python3 .wiki/build.py
   ```

3. **Validate**:

   ```bash
   python3 validate.py
   ```

4. **Provision** the starter skill set:

   ```bash
   python3 .harness/sync_active.py --profile starter
   python3 .harness/gen_skills_index.py
   ```

5. **Run the reference adapter** to verify end-to-end consumption:

   ```bash
   python3 tools/reference_adapter.py
   ```

You should see `PASS: all invariants pass` and active skills listed. Total time: under 5 minutes.

## Quickstart (Starter Set → Core Tier)

By default, provision the **starter skill set** (12 vetted skills, all `core` tier):

```bash
python3 .harness/sync_active.py --profile starter
python3 .harness/gen_skills_index.py
```

To use the full master library (3,520 skills across core/curated/experimental/quarantine tiers),
edit a profile's `skills:` frontmatter list and re-run `sync_active.py`. Expansion beyond starter
requires explicit human approval. Quarantined skills are never provisionable.

## Test

```bash
python3 -m unittest discover -s tests -v
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
- Secrets: `docs/operations/secrets.md` — key storage, rotation, leak response.

## License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

Third-party skills in `.agent/skills/` have various licenses; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for details. Seven skills carry a "tools-registry License" (Apache 2.0 with hosted-service restriction) — review before commercial SaaS distribution.
