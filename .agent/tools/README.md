# Tools — Scripts, MCP & Resource Pointers

Scripts (all run from the workspace root):

- `context.py` — compile_context(target_files) / read_section(node_id)
  core (CLI + importable). Used by the MCP server.
- `provision.py` — sync `.agent/harness/skills/` to a profile's declared
  skills (from the master library in ../skills/).
- `split_references.py` — move code blocks out of oversized SKILL.md
  bodies into `references/` (standard format).
- `classify_os.py` — add the `os` column (android|windows|linux|mac|cross)
  to `.agent/skills/CATEGORIZATION.csv`.
- `build_platforms.py` — generate per-OS companion files
  (`platforms/<os>.md`) for OS-tagged skills.
- `categorize.py`, `import_all_skills.py` — library categorization
  and archive import (historical; already run).

MCP: `mcp/server.py` (stdlib JSON-RPC stdio), contract in `mcp/README.md`.

## Resources (pointers)

- Baselayer docs: `docs/` (indexed into `.context/graph.json` by seed.py).
- Skills currently used: `.agent/harness/skills/` + slim `skills/index.json`.
- Master library (3,520 skills, categorized): `../skills/` —
  task type/subtype/level/os in `CATEGORIZATION.md`/CSV.
- Archive provenance + trust tiers: `docs/resources/README.md`.
- PM shortlist: `docs/resources/project-management.md`.
- Keys: `.agent/.env` (gitignored) — never commit.
