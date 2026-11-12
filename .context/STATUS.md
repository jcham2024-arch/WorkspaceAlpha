# STATUS — current state of the workspace

**Single pointer for agents and humans.** Read this first. Everything that
was previously spread across four fix directives is consolidated here.

Last updated: 2026-11-12

---

## 1. What this workspace is

An offline, DAG-routed documentation workspace. One canonical graph
(`.context/graph.json`) compiles into two surfaces:

| Surface | Audience | Form |
| :--- | :--- | :--- |
| **Wiki** | Humans | `.wiki/index.html` — offline, anchor-addressable |
| **Router** | Agents | `AGENTS.md` + `.context/manifest.json` |

Plus a 3,530-skill master library (`.agent/skills/`) with per-profile
provisioning, and a small MCP/adapter/provenance layer on top.

## 2. Build path (verified working)

```bash
python3 .wiki/seed.py     # docs/ -> .context/graph.json   (cached; skips unchanged)
python3 .wiki/build.py    # graph.json -> manifest.json + .wiki/index.html
python3 validate.py       # gate: PASS/FAIL
```

Current: **3,654 nodes**, wiki ~4.15 MB, `validate.py` PASS.

## 3. Test suite

```bash
python -m unittest discover -s tests -t .
```

Current: **111 tests, 0 failures, 5 skipped.** No pytest in this environment;
everything is stdlib `unittest`. The 5 skips are `tests/test_provision.py`,
which needs the harness-owned `.harness/sync_active.py` bridge that is not
checked into the repo.

Prompt graph is validated separately (it is not part of `.context/graph.json`):

```bash
python3 tools/validate_prompt_graph.py   # JSON graph + YAML mirror coherence
python3 tools/sync_prompt_graph.py       # regenerate YAML from JSON after edits
```

## 4. Completed work

### 4.1 STAIR navigator repair — DONE

The loop fix has landed. Do **not** re-diagnose it.

| Commit | What |
| :--- | :--- |
| `aa1a44ab` | Regression suite for single-prediction, drift, multibyte, timeout, wall-clock |
| `517d90f0` | Single-prediction navigator; dispatch extracted to `adapters/navigator.py`; split into `stair_toc.py` / `stair_validate.py` |
| `e35948ef` | First `validate.py` hardening gate |
| `3edb36cd` | 11 contract tests + 10 gate tests, verified failing against pre-fix `8cdd6298` |
| `94894fdc` | Gate refactored into importable, fixture-testable functions |
| `fb5b9063` | Stale test contract corrected; gate tightened to precise patterns |
| `d9ebdb39` | `FIX_STAIR_LOOP.md` persisted; superseded directive archived |
| `405dc225` | `EXECUTION_PROTOCOL.md` persisted with ledger complete |

Final state of the navigator:

```text
.agent/tools/stair_navigator.py    98 lines   orchestration only
.agent/tools/stair_validate.py     96 lines   validation + byte-exact hydration
.agent/tools/stair_toc.py          65 lines   graph loading + ToC
adapters/navigator.py              68 lines   manager-tier dispatch, 15s cap
```

Contract, enforced by both tests and `validate.py`:

- `navigate()` makes **exactly one** dispatch call per invocation.
- No keyword fallback, no retry, no second prediction attempt.
- No `while` loop anywhere in the module.
- Wall-clock cap: `signal.setitimer`, 15 s, raises `NavigatorTimeout`.
- Low confidence or failed validation returns `node_id=None`; the **router**
  decides fallback, not the navigator.
- Manifest drift raises `ManifestDriftError` (hard error, never silent fallback).
- Hydration reads bytes with seek+read and decodes explicitly
  (`HydrationError` on misaligned UTF-8).

### 4.2 Baseline test repairs — DONE

Five failures predating the navigator work were fixed on 2026-11-12:

| Test | Defect | Fix |
| :--- | :--- | :--- |
| `test_redaction` | Missing `import unittest`; class collected but never run | Import added |
| `test_redaction` | Passed literal `"[redacted]"` as a secret — matches no pattern, so asserted a block the redactor correctly never raised | Synthetic `ghp_…` token fixture |
| `test_redaction` | `TestConvenienceFunctions` subclassed nothing, so unittest discovery skipped it entirely | Now subclasses `unittest.TestCase` |
| `test_seed::test_one_node_per_heading` | Counted raw headings (3,972) against deduplicated nodes (3,654) | Asserts the deduplicated `file::slug` set instead |
| `test_provision` (×5) | Hard-required `.harness/sync_active.py`, absent outside the harness runtime | `skipIf` with an explanatory reason |

## 5. Directives and history

Superseded fix directives live in `.context/archive/`. They are kept for
history and must not be executed:

- `.context/archive/FIX_STAIR_LOOP_III.md` — superseded by `FIX_STAIR_LOOP.md`
- `.context/FIX_STAIR_LOOP.md` — the canonical fix specification (Part I is
  still the diagnostic framework for any *future* navigator loop)
- `.context/EXECUTION_PROTOCOL.md` — the multi-phase execution meta-protocol,
  with its ledger recorded as complete

Read `FIX_STAIR_LOOP.md` Part I only if the navigator loops again after this
repair. Its Parts II–VI describe a code state that no longer exists.

## 6. Known gaps — not bugs, but not done

| Gap | Where | Blocks |
| :--- | :--- | :--- |
| Assembler does not *execute* the protocol | `assembly/assembler.py` binds the `proto-*` node into the prompt but does not call the tool in `metadata.tool` | Retrieval results never enter the context |
| Navigator writes no provenance | `provenance/turns.jsonl` has no dispatch records | Audit trail for retrieval |
| No vector index | `tools/build_vectors.py` exists, `.context/vector-index.db` does not | `Protocol::VECTOR` returns nothing |
| `.harness/` provisioning bridge | Not in repo (harness-owned) | 5 skipped tests |
| `assembly/assembler.py` is 514 lines | Over the 200-line limit `validate.py` enforces with a waiver | Assembler split |

### 6.1 Retrieval protocol layer — wired 2026-11-12

The router-to-graph seam is now connected:

- `prompt-graph.json` declares **5 `RetrievalProtocol` nodes**
  (`proto-direct`, `proto-stair`, `proto-vector`, `proto-graph`, `proto-pattern`),
  each with `metadata.protocol`, `metadata.tool` and an agent `tier`.
- Every protocol node has an inbound `routes_to` edge from both envelopes, so
  the router can actually select it.
- `assembler.py` calls `route()` before Plan, binds **only the selected**
  protocol node (the other four are alternatives, not additions), and applies
  a tier ceiling: `thinking` → manager, `low_thinking`/`non_thinking` → worker.
  A worker asking for PATTERN or GRAPH is downgraded to VECTOR with
  `downgraded_from`, `required_tier` and `tier_ceiling` recorded in provenance.
- `tools/validate_prompt_graph.py` now validates the **JSON** (the file the
  runtime reads) instead of the YAML, checks schema/validator enum agreement,
  rejects duplicate node ids, duplicate edges, self-loops, and any protocol
  node with no inbound `routes_to`, and fails if the YAML mirror has drifted.
- `tools/sync_prompt_graph.py` regenerates the YAML from the JSON and refuses
  to write unless the result round-trips to an identical graph.

**Defect found and fixed while doing this:** `.context/prompt-graph.yaml`
contained a duplicate `edges:` key. A conformant YAML loader keeps the last
occurrence, so 18 of the 21 edges were silently discarded while
`validate_prompt_graph.py` reported PASS — the gate was validating the stale
copy. The validator now targets the JSON and a test asserts the YAML exposes
more than 10 edges.

Remaining: the assembler binds the protocol node but does not yet invoke the
tool named in `metadata.tool`. Binding without executing is why retrieval
results still do not reach the prompt.

## 7. Conventions for the next session

1. **Read this file first.** It replaces four documents.
2. **Build before you change anything:** `seed.py && build.py && validate.py`,
   then `tools/validate_prompt_graph.py`.
3. **Baseline the suite** with `python -m unittest discover -s tests -t .` and
   expect 111 tests, 0 failures, 5 skipped.
4. **Never edit `.context/manifest.json` or `.wiki/index.html`** — both are
   generated. Regenerate via `.wiki/seed.py` and `.wiki/build.py`.
5. **Byte ranges are byte ranges.** Hydrate with `open(path, 'rb')` + seek, never
   a character slice of text-mode read.
6. **`AGENTS.md` is golden-file coupled.** Editing it requires regenerating
   `tests/fixtures/golden/AGENTS.md` (the tripwire is intentional).
7. **Multi-phase work:** one phase per commit, ledger updated before each. See
   `EXECUTION_PROTOCOL.md` §1.
8. **No pytest.** Use `unittest`. `mocker.patch` becomes `unittest.mock.patch`.

---

**End of STATUS. If you are about to fix the stair navigator loop: it is
already fixed. Check §4.1 and `git log`. If you are about to build: §2. If you
are about to change a generated file: §7.4.**
