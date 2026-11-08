# .wiki — Render Pipeline

All wiki rendering lives here; nothing else lives here.

- `seed.py` — `docs/` → `.context/graph.json` (manifest of sections)
- `build.py` — `graph.json` → `.context/manifest.json` + `index.html`
- `index.html` — the generated human wiki (never hand-edit)

Inputs: `docs/` (sections), `.context/graph.json` (DAG).
Outputs: `.context/manifest.json` + `index.html`.
Validate: `python3 validate.py` from the workspace root.
