# Decision: Q5 — Wiki Render Pipeline: Incremental vs Full Rebuild

## Question

Should the wiki render pipeline (`.wiki/seed.py` → `.wiki/build.py`) support incremental rebuilds (only changed files) or always perform full rebuilds? What are the performance and correctness trade-offs?

## Chosen Value

**Full rebuild by default; incremental as an opt-in optimization behind a flag.** The canonical pipeline runs full rebuilds (`seed.py` scans all `docs/`, `build.py` regenerates entire `manifest.json` and `wiki/index.html`). An incremental mode (`--incremental`) may be added later for development speed, gated by content-hash comparison.

## Approver

wiki-producer (HTML production), taskmaster (orchestration) — 2026-11-10

## Evidence

- Current `seed.py`: walks `docs/`, parses every `.md`, extracts sections, writes `graph.json` (83 nodes, ~15KB)
- Current `build.py`: reads `graph.json`, generates `manifest.json` + `wiki/index.html` (~88KB)
- Full rebuild time: ~0.7s total (seed: 0.3s, build: 0.4s) on Android 17 device
- `docs/` size: ~15 files, ~15KB total markdown
- No external dependencies; pure Python 3.14 stdlib
- `validate.py` validates entire graph/manifest/wiki consistency

## Rationale

Industry baselines for static site generators and documentation pipelines:

| Approach | Examples | Trade-off |
|----------|----------|-----------|
| **Full rebuild** | Sphinx, MkDocs (default), Hugo, Jekyll | Simple, correct, fast enough for small corpora |
| **Incremental** | VitePress, Next.js, Astro | Complex cache invalidation, risk of stale output |
| **Hybrid** | MkDocs `--dirtyreload`, Sphinx `-j auto` | Opt-in, development only |

For our corpus (15 files, <1s rebuild), **full rebuild is correct by default**. The complexity of incremental (file watching, hash tracking, partial graph merge, partial HTML rewrite) is not justified. Incremental can be added later as `--incremental` flag using SHA-256 content hashes already stored in `graph.json` nodes.

Key principle: **Correctness over speed for the canonical pipeline**. The build is fast enough that incremental optimization is premature.

## Constraint on Future Specs

- **Forbidden**: Making incremental the default or only mode
- **Required**: Full rebuild must always produce bit-for-bit identical output given same input
- **Required**: If incremental mode added, it must pass `validate.py` with identical results to full rebuild
- **Required**: `validate.py` remains the source of truth for correctness; no incremental-only validation path

## Links

- Spec: `docs/specs/wiki-render-spec.md` (planned)
- Tracking: `open-questions.md` (Q5)
- Implementation: `.wiki/seed.py`, `.wiki/build.py`, `validate.py`

---

*Decision recorded 2026-11-10. Current rebuild: ~700ms. Incremental flag may be added when corpus exceeds 100 files or rebuild exceeds 5s.*
