# agent.md — Wiki Production

This folder renders the system's LLM-optimized docs into human HTML.
Audience: a human reading on a phone or browser, not a model.

What gets rendered

- `docs/` (provenance, project docs, specs) — indexed by
  `.wiki/seed.py` into sections, then rendered by `.wiki/build.py`
  into `index.html` (offline, anchor-addressable).
- Human context: the wiki explains WHAT exists and WHY; the LLM
  docs keep routing (see root `AGENTS.md` + `.context/manifest.json`).

Working rules

1. Only `docs/` is indexed. Root spec files (`Baselayer.md`),
   runtime folders (`.agent/`), and generated artifacts are never
   in the wiki — they are toolchain, not content.
2. Never hand-edit `index.html` or `manifest.json`. Change docs/,
   then rebuild.
3. Node ids double as anchors (`#docs/...::section`); the wiki is
   the human audit surface — cite them in reports.
4. Human language rule: short paragraphs, one idea each, bullets
   for parallel points, tables only for aligned rows. No jargon
   dumps, no walls of text.

Agent: this folder's producer profile is
`.agent/profiles/wiki-producer.md` — same rule set, different
audience. When the two conflict, the human-readable surface wins
for generated prose.

## Layout (this folder)

```
.wiki/
├── agent.md      ← this file
├── README.md     ← pipeline (inputs/outputs)
├── seed.py       ← docs/ → graph.json
├── build.py      ← graph.json → manifest.json + index.html
└── index.html    ← generated wiki (never hand-edit)
```

Commands (workspace root):
```bash
python3 .wiki/seed.py && python3 .wiki/build.py
python3 validate.py
```
