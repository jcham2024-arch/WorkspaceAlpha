# FIX DIRECTIVE: stair_navigator.py Loop — Diagnostic Framework & Definitive Fix

**Audience:** Implementation agent (human or model)
**Status:** This document supersedes the earlier `FIX_STAIR_LOOP.md`, `FIX_STAIR_LOOP_II.md`, and `FIX_STAIR_LOOP_III.md`. Read this one; do not chase the earlier versions. If any earlier version exists on disk, move it to `.context/archive/` and add a pointer at the top of each archived file saying "Superseded by FIX_STAIR_LOOP.md."
**Prerequisites:** None. This document is self-contained. It contains both the diagnostic framework (Part I) for any *future* loop in `stair_navigator.py` and the specific confirmed diagnosis and fix (Parts II–VI) for the *current* loop.

**Save this to disk as `.context/FIX_STAIR_LOOP.md` before executing anything.** The previous fix directives were written in conversation but evidently never made it to disk in a form a fresh session could find — which is the most likely reason the fix was never applied. Do not repeat that failure.

---

## 0. THE PROBLEM, STATED PRECISELY

`stair_navigator.py` is looping during execution. The file is 110 lines (under the 200-line limit) so the loop is not a file-size problem. The loop is caused by three compounding defects that coexist in the current code:

1. **Dual dispatch paths.** `_dispatch_llm()` is defined at lines 42–55 but is never called. `navigate()` calls `dispatcher.dispatch()` directly at line 74. The dead helper means a future maintainer may reconnect it, producing a different bug.
2. **Keyword-scan fallback.** After the dispatch, if no usable `node_id` is extracted, `navigate()` runs a linear keyword scan over all manifest nodes (lines 84–85). This is a **second prediction attempt** — the failure mode the single-prediction contract exists to prevent.
3. **No wall-clock cap.** If `dispatcher.dispatch()` hangs — adapter timeout unset, model in a bad state, network stalled — `navigate()` runs unbounded. The session dies at the context limit before the hang returns.

What is already correct and must be preserved:

- Predicted node is validated against `manifest_nodes` before hydration (~lines 76–80). If not found, `node_id=None` is returned. This is correct.
- Hydration uses `read_bytes()` and byte slicing, not character slicing (~lines 95–100). This is correct.
- `_load_graph()` and `_build_toc()` are correct.

The fix is narrow: eliminate the dead helper, remove the keyword fallback, add a wall-clock cap, add the enforcement gate, add the regression tests.

---

## 1. INVARIANTS

1. **One prediction per call.** `navigate()` makes exactly one dispatch call. If the result is unusable, it returns `LeafPrediction(node_id=None, ...)`. The caller (router) handles fallback. No keyword scan, no second attempt, no retry.
2. **Single dispatch path.** `_dispatch_llm()` is the only function that calls the adapter. `navigate()` calls `_dispatch_llm()`. The inline `dispatcher.dispatch()` call is removed.
3. **Wall-clock cap.** The dispatch call has a hard 15-second timeout. Exceeding it raises `NavigatorTimeout`. No retry.
4. **Enforcement is machine-checked.** `validate.py` fails the build if `stair_navigator.py` contains a `while` loop inside `navigate()`, defines an inline `dispatcher.dispatch` call, contains a keyword fallback, or grows past 200 lines.
5. **Regression tests lock the contract.** Tests exist that would have caught the original loop. Without them, the fix is unprovable.
6. **Failing test before fix.** The regression test commit precedes the fix commit. If the test passes against the pre-fix code, the test does not exercise the loop and the fix is unprovable.
7. **Preserve working paths.** Do not change manifest validation behavior, hydration, or graph loading. Remove the fallback, delete the dead path, add the timeout. Nothing else.

---

## PART I — DIAGNOSTIC FRAMEWORK FOR FUTURE LOOPS

This part is preserved from the original directive. If a loop returns after this fix and the confirmed diagnosis in Part II does not apply, run these five checks in order. The first check that fires is your hypothesis.

### Hypothesis 1 — Confidence retry loop

**Check:** `grep -n "while\|recurs\|_try_predict\|_retry\|_attempt\|confidence" .agent/tools/stair_navigator.py`

**Signal:** Any `while` loop, any recursive call, or any function whose name suggests retry inside the prediction path.

**Why it loops:** The LLM dispatch is deterministic under a fixed prompt/temperature/seed. If `while confidence < threshold: predict_again()` exists, the confidence never changes and the loop is unbounded. Unit tests don't catch this because they mock the LLM to return a fixed confidence and never exercise the retry path past one iteration.

**Diagnostic confirmation:**

```bash
python -c "
from unittest.mock import patch
from .agent.tools import stair_navigator as sn

call_count = [0]
def fake_dispatch(*a, **kw):
    call_count[0] += 1
    return {'node_id': 'some-node', 'confidence': 0.3}  # below threshold

with patch.object(sn, '_dispatch_llm', fake_dispatch):
    try:
        sn.navigate('test query')
    except Exception as e:
        print('raised:', type(e).__name__, e)
    print('dispatch calls:', call_count[0])
"
```

If `dispatch calls > 1` for a low-confidence response, that's the loop.

### Hypothesis 2 — Graph/manifest drift

**Check:**

```bash
python -c "
import json
g = json.load(open('.context/graph.json'))
m = json.load(open('.context/manifest.json'))
g_nodes = set(n['id'] for n in (g.get('nodes') or []))
m_nodes = set(n['id'] for n in (m.get('nodes') or []))
print('graph nodes:', len(g_nodes))
print('manifest nodes:', len(m_nodes))
print('in graph not in manifest:', len(g_nodes - m_nodes))
print('in manifest not in graph:', len(m_nodes - g_nodes))
"
```

**Signal:** Non-zero drift in either direction.

**Why it loops:** The navigator builds its ToC from `graph.json` and validates predictions against `manifest.json`. If a predicted node exists in the graph but not in the manifest, every prediction fails validation. If there's retry logic (Hypothesis 1 also present), the navigator retries with the same starting data and gets the same answer. This is a build-pipeline bug, not a navigator bug. The fix is to regenerate `manifest.json` from `graph.json` in the same build step and add the coherence check to `validate.py`.

### Hypothesis 3 — Byte-vs-character slicing

**Check:** `grep -n "content_ref\|byte_range\|open(\|\[.*:.*\]\|encode\|decode" .agent/tools/stair_navigator.py`

**Signal:** Any occurrence of `open(path).read()[start:end]` (character slice) or `open(path, 'r').read()[start:end]` when the byte ranges in the manifest were computed on bytes.

**Why it loops:** Multi-byte UTF-8 characters before the byte range shift the character slice. Hydration returns wrong content, fails validation, retries.

**Note:** The current code already uses `read_bytes()` and byte slicing correctly. This hypothesis is included for completeness; it does not apply to the current state unless the fix regressed it.

### Hypothesis 4 — Wrong adapter tier or adapter instability

**Check:** `grep -n "_dispatch_llm\|adapter\|tier\|manager\|orchestrator\|worker\|timeout" .agent/tools/stair_navigator.py`

**Signal:** Any of:
- `_dispatch_llm` defined inline (not imported from `adapters/`)
- Adapter calls to worker-tier or orchestrator-tier models (STAIR is manager-tier work)
- Any `timeout=` parameter without a corresponding `except TimeoutError:` that raises rather than retries
- Broad `except Exception:` clauses around adapter calls

**Why it loops:** Timeout caught by broad `except` that retries — the retry can time out again. Wrong tier (orchestrator for fast prediction) makes timeouts likely.

### Hypothesis 5 — Circular import with broad except

**Check:** `grep -n "except Exception\|except:\|except ImportError\|except AttributeError" .agent/tools/stair_navigator.py`

**Signal:** A bare `except:` or `except Exception:` around a call to a module whose import may be deferred, combined with any circular import structure.

**Why it loops:** Python's deferred import execution can succeed at module load but fail at call time with `AttributeError` or `ImportError` on a partially-initialized module. If that's caught and retried, the retry hits the same partially-initialized state.

---

## PART II — THE CURRENT CONFIRMED DIAGNOSIS

The current loop is **not any of the five hypotheses in their pure form**. It is a compound failure that shares features with Hypothesis 1 (retry loop) but the retry comes from the fallback rather than from a `while` loop.

**The actual mechanism:**

1. `navigate()` calls `dispatcher.dispatch()` inline (line 74).
2. If the adapter returns a result with no usable `node_id` — because the prompt was malformed, the model returned an unexpected shape, or the manifest check fails — the code falls through to the keyword scan (lines 84–85).
3. The keyword scan iterates over `nodes` linearly. If the query is short, or the graph is large, this can produce a `node_id` that *looks* valid but is not in the manifest.
4. The caller (router) receives `node_id=None` or a drift-failing `node_id`, and (because there is no wall-clock cap) retries `navigate()`. Each retry repeats steps 1–3.
5. Without a timeout, no individual retry is bounded. Without a single-prediction contract, each `navigate()` call contains its own internal retry via the fallback. The loop is multiplicative.

**What's added by the dead `_dispatch_llm`:** It signals that a prior refactoring attempt was started and not finished. Anyone reading the file sees two dispatch paths and doesn't know which is canonical. A future "cleanup" that routes `navigate()` through `_dispatch_llm` would produce a *different* bug (different error handling, different model params) — still a loop, just a different one.

**The fix that addresses this diagnosis is not "one of the five hypotheses" — it's the single-prediction contract plus the wall-clock cap, which together eliminate the retry surface and bound whatever retry mechanism remains.**

---

## PART III — THE FIX PROCEDURE

### Phase 0 — Preserve and locate

```bash
# 1. Save this directive to disk
# Copy contents to .context/FIX_STAIR_LOOP.md

# 2. Archive the earlier directives (if present)
mkdir -p .context/archive
for f in FIX_STAIR_LOOP_II.md FIX_STAIR_LOOP_III.md; do
    if [ -f ".context/$f" ]; then
        echo "Superseded by .context/FIX_STAIR_LOOP.md" | \
            cat - .context/$f > .context/archive/$f
        rm .context/$f
    fi
done

# 3. Add pointer in AGENTS.md if present
# Append: "Active fix: see .context/FIX_STAIR_LOOP.md"

# 4. Backup
cp -r . /tmp/wa_fix_backup_$(date +%Y%m%d_%H%M%S)

# 5. Stash to verify baseline
git stash push -u -m "pre-fix $(date +%Y%m%d_%H%M%S)"

# 6. Verify baseline
python -m pytest -x -q 2>&1 | tail -10
python .wiki/validate.py 2>&1 | tail -5
```

**If pytest fails at baseline:** record the failure. The most likely failure is `test_navigate_returns_result` in `tests/test_stair_navigator.py` (the stale `isinstance(result, dict)` assertion). Phase 1 fixes it.

**If pytest passes at baseline:** the stale test is being skipped or not collected. Check `pytest --collect-only tests/ | grep stair`, `grep -rn "skip\|xfail" tests/`, and `cat pytest.ini`. Record in `memory/ERRORS.md` — it's a second bug.

### Phase 1 — Fix the stale test (unblock)

Read the current test:

```bash
cat tests/test_stair_navigator.py
```

Replace its contents with:

```python
"""Tests for stair_navigator basic contract."""
import time
from .agent.tools.stair_navigator import navigate, LeafPrediction


def test_navigate_returns_leaf_prediction():
    """navigate() returns a LeafPrediction, not a dict."""
    result = navigate("test query")
    assert isinstance(result, LeafPrediction), (
        f"navigate() returned {type(result).__name__}, expected LeafPrediction. "
        f"If this fails, check whether navigate() was reverted to returning dicts."
    )
    assert hasattr(result, "node_id")
    assert hasattr(result, "confidence")


def test_navigate_empty_query_bounded():
    """Empty query either returns None-node or a valid one. Must not hang."""
    start = time.monotonic()
    result = navigate("")
    elapsed = time.monotonic() - start
    assert elapsed < 30, f"navigate('') exceeded 30s ({elapsed:.1f}s) — timeout not working"
    assert isinstance(result, LeafPrediction)
```

Verify:

```bash
python -m pytest tests/test_stair_navigator.py -x -q
```

Both must pass. If `test_navigate_empty_query_bounded` fails on wall-clock, that confirms the missing timeout — Phase 3 fixes it. Record the observed duration.

**Commit 1:**

```bash
git add tests/test_stair_navigator.py
git commit -m "test(stair): fix stale test — navigate() returns LeafPrediction, not dict

Prior test asserted isinstance(result, dict) against a function returning
LeafPrediction. Either failing silently or skipped. Adds wall-clock bound
to catch future hangs.

Baseline: [record pass/fail]
navigate('') duration: [record]s"
```

### Phase 2 — Write the failing regression tests

Append to `tests/test_stair_navigator.py`:

```python
import pytest
from unittest.mock import patch


class TestSinglePredictionContract:
    """navigate() must dispatch exactly once per call. See FIX_STAIR_LOOP.md §1."""

    def test_dispatch_called_exactly_once(self, mocker):
        dispatch_spy = mocker.patch(
            ".agent.tools.stair_navigator._dispatch_llm",
            return_value={"node_id": "some-node", "confidence": 0.9}
        )
        mocker.patch(
            ".agent.tools.stair_navigator._load_manifest",
            return_value={"nodes": [{"id": "some-node", "content_ref": "/tmp/x.md",
                                     "byte_range": [0, 10]}]}
        )
        mocker.patch(
            ".agent.tools.stair_navigator._load_graph",
            return_value=([{"id": "some-node"}], None)
        )

        navigate("test query")

        assert dispatch_spy.call_count == 1, (
            f"Expected exactly 1 dispatch call, got {dispatch_spy.call_count}. "
            f"navigate() must be single-prediction — no keyword fallback, no retry."
        )

    def test_manifest_drift_returns_none_no_retry(self, mocker):
        dispatch_spy = mocker.patch(
            ".agent.tools.stair_navigator._dispatch_llm",
            return_value={"node_id": "ghost-node", "confidence": 0.9}
        )
        mocker.patch(
            ".agent.tools.stair_navigator._load_manifest",
            return_value={"nodes": [{"id": "real-node"}]}
        )
        mocker.patch(
            ".agent.tools.stair_navigator._load_graph",
            return_value=([{"id": "ghost-node"}], None)
        )

        result = navigate("test query")

        assert result.node_id is None
        assert dispatch_spy.call_count == 1

    def test_empty_graph_returns_none_no_dispatch(self, mocker):
        dispatch_spy = mocker.patch(".agent.tools.stair_navigator._dispatch_llm")
        mocker.patch(
            ".agent.tools.stair_navigator._load_graph",
            return_value=([], None)
        )

        result = navigate("test query")

        assert result.node_id is None
        assert dispatch_spy.call_count == 0


class TestNoLoopConstructs:
    """Static checks — the navigator must not contain loop constructs."""

    def test_no_while_in_navigate(self):
        import ast, pathlib
        src = pathlib.Path(".agent/tools/stair_navigator.py").read_text()
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "navigate":
                for inner in ast.walk(node):
                    assert not isinstance(inner, ast.While), (
                        "navigate() contains a while loop — prediction must be single-shot"
                    )

    def test_inline_dispatch_removed(self):
        import pathlib
        src = pathlib.Path(".agent/tools/stair_navigator.py").read_text()
        assert "dispatcher.dispatch" not in src, (
            "Inline dispatcher.dispatch() present — route through _dispatch_llm() only"
        )

    def test_keyword_fallback_removed(self):
        import pathlib
        src = pathlib.Path(".agent/tools/stair_navigator.py").read_text()
        has_keyword_scan = "query_lower" in src or (
            "query.lower()" in src and "for node in nodes" in src
        )
        assert not has_keyword_scan, (
            "Keyword fallback present — second prediction attempt"
        )
```

Run them and confirm they fail against the current code:

```bash
python -m pytest tests/test_stair_navigator.py::TestSinglePredictionContract -x -q
python -m pytest tests/test_stair_navigator.py::TestNoLoopConstructs -x -q
```

**If any of these pass against the current code, stop.** The mocks are not hitting the real dispatch path; fix the mocks so the test exercises the actual code. The fix is not provable if the tests cannot fail.

**Commit 2:**

```bash
git add tests/test_stair_navigator.py
git commit -m "test(stair): add failing regression tests for single-prediction contract

Against current code:
- test_dispatch_called_exactly_once: FAIL (keyword fallback runs)
- test_manifest_drift_returns_none_no_retry: [record state]
- test_empty_graph_returns_none_no_dispatch: [record state]
- test_no_while_in_navigate: [record state]
- test_inline_dispatch_removed: FAIL (dispatcher.dispatch present)
- test_keyword_fallback_removed: FAIL (query_lower present)

Fix commit makes these pass."
```

### Phase 3 — Apply the fix

Read the current file first:

```bash
cat .agent/tools/stair_navigator.py
```

Confirm the state matches Part II. If it doesn't, stop and re-diagnose using Part I.

**Add at the top of the file (after existing imports):**

```python
import signal


class NavigatorTimeout(Exception):
    """Raised when a dispatch call exceeds the wall-clock cap."""
    pass


class NavigatorDispatchError(Exception):
    """Raised when the dispatch adapter fails for a non-timeout reason."""
    pass


_WALL_CLOCK_TIMEOUT_SECONDS = 15


def _with_timeout(fn, *args, timeout=_WALL_CLOCK_TIMEOUT_SECONDS, **kwargs):
    """Run fn with a hard wall-clock cap. Raises NavigatorTimeout on expiry."""
    def _handler(signum, frame):
        raise NavigatorTimeout(f"operation exceeded {timeout}s")

    previous = signal.signal(signal.SIGALRM, _handler)
    signal.alarm(timeout)
    try:
        return fn(*args, **kwargs)
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)
```

**Replace `navigate()` with:**

```python
def navigate(query: str, *, model: str = "nemotron-3.5", tier: str = "manager") -> LeafPrediction:
    """Single-shot leaf prediction.

    Contract: exactly one dispatch call per invocation. If the prediction
    is unusable for any reason (dispatch error, timeout, manifest drift,
    low confidence), returns LeafPrediction(node_id=None). The caller
    (router) handles fallback.

    No keyword scan, no retry, no second dispatch. If you are tempted to
    add one, that is the bug this contract exists to prevent.
    """
    nodes, _ = _load_graph()
    if not nodes:
        return LeafPrediction(node_id=None, path=[], confidence=0.0)

    toc = _build_toc(nodes)
    manifest_nodes = {n["id"] for n in _load_manifest().get("nodes", [])}

    prompt = _build_prompt(query, toc)

    try:
        result = _with_timeout(_dispatch_llm, model=model, tier=tier, prompt=prompt)
    except NavigatorTimeout:
        return LeafPrediction(node_id=None, path=[], confidence=0.0)
    except NavigatorDispatchError:
        return LeafPrediction(node_id=None, path=[], confidence=0.0)

    if not result or not result.get("node_id"):
        return LeafPrediction(node_id=None, path=[], confidence=0.0)

    predicted_id = result["node_id"]
    if predicted_id not in manifest_nodes:
        # Structural drift — graph and manifest disagree. Return None;
        # the router decides whether to fall back to VECTOR. The drift
        # itself is a build bug caught by validate.py's coherence check.
        return LeafPrediction(node_id=None, path=[], confidence=0.0)

    return _hydrate(predicted_id, nodes, confidence=result.get("confidence", 0.5))
```

**Delete from the file:**

- The inline `dispatcher.dispatch()` call (entire try/except block)
- The keyword scan (`for node in nodes: if query_lower in ...`)
- Any `while` loop
- Any `except Exception:` or bare `except:` around the dispatch
- Any import left unused by the removals

**Keep unchanged:** `_load_graph()`, `_build_toc()`, `_load_manifest()`, `_build_prompt()`, `_hydrate()`. Manifest validation logic moved verbatim into the new `navigate()`. Byte-mode read in `_hydrate()`.

**Verify:**

```bash
python -m pytest tests/test_stair_navigator.py -x -q
```

All tests must pass. If any fail, the fix is incomplete — do not commit.

**Commit 3:**

```bash
git add .agent/tools/stair_navigator.py
git commit -m "fix(stair): enforce single-prediction contract + 15s wall-clock cap

- Remove inline dispatcher.dispatch() call; route through _dispatch_llm() only
- Remove keyword-scan fallback (was a second prediction attempt)
- Add _with_timeout() wrapper using signal.alarm
- Add NavigatorTimeout and NavigatorDispatchError exception classes
- navigate() now makes exactly one dispatch call per invocation

Makes regression tests from previous commit pass."
```

### Phase 4 — Add the enforcement gate to validate.py

Read the current `validate.py`:

```bash
cat .wiki/validate.py
```

**Add these functions:**

```python
import ast
import json
import pathlib


def check_navigator_loop_constructs(ROOT) -> list[str]:
    """Fail if stair_navigator.py has a while loop inside navigate()."""
    violations = []
    nav_path = ROOT / ".agent/tools/stair_navigator.py"
    if not nav_path.exists():
        return []
    tree = ast.parse(nav_path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "navigate":
            for inner in ast.walk(node):
                if isinstance(inner, ast.While):
                    violations.append(
                        f"{nav_path}: while loop in navigate() — "
                        f"see FIX_STAIR_LOOP.md §1"
                    )
    return violations


def check_navigator_dispatch_path(ROOT) -> list[str]:
    """Fail if the inline dispatch call or keyword fallback is reintroduced."""
    violations = []
    nav_path = ROOT / ".agent/tools/stair_navigator.py"
    if not nav_path.exists():
        return []
    src = nav_path.read_text()
    if "dispatcher.dispatch" in src:
        violations.append(
            f"{nav_path}: inline dispatcher.dispatch() present — "
            f"route through _dispatch_llm() only"
        )
    has_keyword_scan = "query_lower" in src or (
        "query.lower()" in src and "for node in nodes" in src
    )
    if has_keyword_scan:
        violations.append(
            f"{nav_path}: keyword fallback present — second prediction attempt"
        )
    return violations


LINE_COUNT_LIMITS = {
    "assembly/*.py": 200,
    ".agent/tools/*.py": 200,
    ".agent/tools/mcp/*.py": 200,
}


def check_line_counts(ROOT) -> list[str]:
    """Fail if any tooling file exceeds its limit without a waiver."""
    violations = []
    for pattern, limit in LINE_COUNT_LIMITS.items():
        for path in ROOT.glob(pattern):
            text = path.read_text()
            if "wa:allow-long-file" in text[:200]:
                continue
            lines = len(text.splitlines())
            if lines > limit:
                violations.append(
                    f"{path}: {lines} lines exceeds {limit}-line limit. "
                    f"Split per CLEANUP_DIRECTIVE.md."
                )
    return violations


def check_graph_manifest_coherence(ROOT) -> list[str]:
    """Fail if graph.json and manifest.json disagree on node IDs."""
    violations = []
    graph_path = ROOT / ".context/graph.json"
    manifest_path = ROOT / ".context/manifest.json"
    if not graph_path.exists() or not manifest_path.exists():
        return ["missing graph.json or manifest.json"]
    g = json.loads(graph_path.read_text())
    m = json.loads(manifest_path.read_text())
    g_nodes = {n["id"] for n in (g.get("nodes") or [])}
    m_nodes = {n["id"] for n in (m.get("nodes") or [])}
    for missing in g_nodes - m_nodes:
        violations.append(f"node {missing} in graph.json but not manifest.json — run build.py")
    for stale in m_nodes - g_nodes:
        violations.append(f"node {stale} in manifest.json but not graph.json — regenerate")
    return violations
```

**Wire into `validate.py`'s main:**

```python
def main():
    violations = []
    violations.extend(check_manifest_integrity())  # existing check
    violations.extend(check_navigator_loop_constructs(ROOT))
    violations.extend(check_navigator_dispatch_path(ROOT))
    violations.extend(check_line_counts(ROOT))
    violations.extend(check_graph_manifest_coherence(ROOT))

    if violations:
        for v in violations:
            print(f"FAIL: {v}")
        sys.exit(1)
    print("PASS: validate.py — 0 violations")
```

**Verify the gate catches violations:**

```bash
# Test the AST check works in isolation
python -c "
import ast
src = 'def navigate(q):\n    while True:\n        pass\n'
tree = ast.parse(src)
found = False
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef) and node.name == 'navigate':
        for inner in ast.walk(node):
            if isinstance(inner, ast.While):
                found = True
assert found, 'AST check broken'
print('AST check working:', found)
"

# Verify current code passes
python .wiki/validate.py
```

**Commit 4:**

```bash
git add .wiki/validate.py
git commit -m "feat(validate): enforce navigator single-prediction contract at build time

Adds four checks:
- no while loops in navigate()
- no inline dispatcher.dispatch() (route through _dispatch_llm only)
- no keyword fallback
- line-count limits for assembly/ and .agent/tools/
- graph/manifest coherence

These make the fix permanent. Without them, the next session can
reintroduce the bug without anyone noticing until it loops again."
```

### Phase 5 — Adapter timeout (defense in depth)

```bash
cat adapters/dispatch.py
```

**If synchronous:** the navigator's `signal.alarm` already wraps it. Skip this phase.

**If asynchronous:** wrap the underlying model call in `asyncio.wait_for`:

```python
import asyncio


class AdapterTimeout(Exception):
    pass


async def dispatch(self, model, tier, prompt, *, timeout=10.0):
    try:
        return await asyncio.wait_for(
            self._do_dispatch(model, tier, prompt),
            timeout=timeout,
        )
    except asyncio.TimeoutError:
        raise AdapterTimeout(f"adapter dispatch exceeded {timeout}s")
```

**Commit 5 (if changed):**

```bash
git add adapters/dispatch.py
git commit -m "fix(adapter): add dispatch timeout — defense in depth for navigator cap"
```

### Phase 6 — End-to-end verification

```bash
# 1. Full test suite
python -m pytest -x -q

# 2. Validation gate
python .wiki/validate.py

# 3. Real navigate() in bounded time
python -c "
import time
from .agent.tools.stair_navigator import navigate
start = time.monotonic()
result = navigate('According to ADR-004, what was the decision?')
elapsed = time.monotonic() - start
print(f'navigate completed in {elapsed:.2f}s, node_id={result.node_id}')
assert elapsed < 20, f'exceeded 20s — timeout not working'
print('PASS')
"

# 4. Confirm single-dispatch in provenance
grep -n "dispatch" provenance/turns.jsonl | tail -5
```

---

## PART IV — ACCEPTANCE CRITERIA

- [ ] `.context/FIX_STAIR_LOOP.md` exists on disk.
- [ ] Archived earlier directives are in `.context/archive/` with supersession notes.
- [ ] `test_navigate_returns_leaf_prediction` passes.
- [ ] `test_navigate_empty_query_bounded` passes.
- [ ] `test_dispatch_called_exactly_once` passes.
- [ ] `test_manifest_drift_returns_none_no_retry` passes.
- [ ] `test_empty_graph_returns_none_no_dispatch` passes.
- [ ] `test_no_while_in_navigate` passes.
- [ ] `test_inline_dispatch_removed` passes.
- [ ] `test_keyword_fallback_removed` passes.
- [ ] `grep -n "dispatcher.dispatch" .agent/tools/stair_navigator.py` returns empty.
- [ ] `grep -n "query_lower\|keyword.*fallback" .agent/tools/stair_navigator.py` returns empty.
- [ ] `grep -n "_with_timeout\|signal.alarm\|NavigatorTimeout" .agent/tools/stair_navigator.py` shows the timeout infrastructure.
- [ ] `validate.py` fails on a synthetic `while` in `navigate()`.
- [ ] `validate.py` fails on a synthetic `dispatcher.dispatch` in the navigator.
- [ ] `validate.py` passes against the current code.
- [ ] A real `navigate()` call completes in under 20 seconds.
- [ ] `git log` shows: failing-test commit before fix commit, fix commit before gate commit.

---

## PART V — WHAT NOT TO DO

- ❌ Do not merge Phase 2 (failing tests) and Phase 3 (fix) into one commit. The failing test must precede the fix in `git log` so the fix is provable.
- ❌ Do not add retry logic to `navigate()` "to handle flaky dispatch." A flaky dispatch is a dispatch problem. The navigator returns `None`; the router decides. Fix the adapter — don't paper over it.
- ❌ Do not widen the 15-second timeout. If predictions time out, fix the cause (slow adapter, oversized ToC, wrong-tier dispatch).
- ❌ Do not add a keyword fallback "as a safety net." The keyword fallback **is** the bug.
- ❌ Do not catch `Exception` around the dispatch. Catch `NavigatorTimeout` and `NavigatorDispatchError` specifically.
- ❌ Do not attempt the structural split (`stair_validate.py`, `stair_toc.py`) in this session. That's `CLEANUP_DIRECTIVE.md` Phase 3 and can land after the fix.
- ❌ Do not attempt the assembler split. Same reason.
- ❌ Do not "improve" working paths while in the file. Manifest validation and byte-mode hydration are correct.
- ❌ Do not skip the `validate.py` gate. It's the only thing preventing the next session from reintroducing the bug.
- ❌ Do not skip the "save to disk" step in Phase 0. The previous directives were not saved — the most likely reason the fix never landed.

---

## PART VI — COMMIT SEQUENCE

```
1. test(stair): fix stale test — navigate() returns LeafPrediction, not dict
2. test(stair): add failing regression tests for single-prediction contract
3. fix(stair): enforce single-prediction contract + 15s wall-clock cap
4. feat(validate): enforce navigator single-prediction contract at build time
5. fix(adapter): add dispatch timeout — defense in depth (if applicable)
```

Each commit independently verifiable. Each commit message records the verification state at that step. The `git log` is the evidence trail. If you cannot demonstrate from `git log` that the failing test landed before the fix, the fix is unprovable.

---

## PART VII — IF THE LOOP RETURNS ANYWAY

Even with the single-prediction fix and the wall-clock cap, a loop could re-emerge through:

- A caller that retries `navigate()` on `None` (check the router in `assembly/`)
- An adapter that hangs beyond 15s in a way `signal.alarm` cannot interrupt (blocking I/O on a non-main thread)
- A manifest so large that `_build_toc()` itself takes minutes

If a loop is observed after the fix:

1. **Check whether `navigate()` is called more than once per session.** The router should call once and fall back to VECTOR on `None`. If it retries, that's a router bug.
2. **Check `provenance/turns.jsonl`** for the dispatch pattern. N dispatch entries for one session means N calls.
3. **Verify the wall-clock cap fires.** Add a deliberate `time.sleep(60)` to `_dispatch_llm`, run `navigate()`, confirm `NavigatorTimeout` raises within 15s, remove the sleep.

If all three pass and the loop still occurs, **return to Part I** and run the five diagnostic hypotheses against the actual looping component. The loop is not in `stair_navigator.py` — do not keep patching this file. Diagnose the actual location.

---

## PART VIII — AFTER THIS LANDS

Once all commits are in and verified:

1. **Structural split** (`CLEANUP_DIRECTIVE.md` Phase 3) — safe now, on a stable base.
2. **Assembler split** (`CLEANUP_DIRECTIVE.md` Phase 1) — the `plan.py` / `optimize.py` / `execute.py` / `feedback.py` decomposition.
3. **Loop detection protocol** (`IMPLEMENTATION_SCOPING_PROTOCOLS.md` Addendum II §2) — `material_progress` on worker checkpoints, four loop detectors.
4. **Handoff protocol** (`IMPLEMENTATION_HANDOFF_PROTOCOLS.md` Addendum I) — so future loops terminate with resumable sessions rather than hung workers.
5. **GPM** (main directive §4.2) — the transformation store that makes scoping cheaper over time.

None of those can land usefully until this fix is provably done and the gate is in place. This directive is the prerequisite for everything else.

---

**End of directive. The single most important rules: (1) save this to disk before executing; (2) write the failing test before the fix; (3) do not merge the failing test and the fix into one commit; (4) add the `validate.py` gate even though it feels like extra work — it's the only thing that prevents the next session from reintroducing the bug. The project has been stuck at this boundary before. The way to not get stuck again is to follow the sequence exactly and leave the evidence trail in `git log` so the next session inherits both the fix and the proof it was fixed.**