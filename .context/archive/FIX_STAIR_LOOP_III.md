> **Superseded by .context/FIX_STAIR_LOOP.md** (2026-11-12). Archived for history; do not execute.

# FIX DIRECTIVE III: Execute the Loop Fix That Was Specified But Not Applied

**Audience:** Implementation agent (human or model)
**Prerequisites:** Read `.context/FIX_STAIR_LOOP_II.md` — this directive is its execution, not its replacement. That document explains *why* each change matters. This document explains *exactly what to change and how to verify it landed*.
**Scope:** Apply the single-prediction contract, the wall-clock cap, the enforcement gate, the regression tests, and the adapter timeout to the current code state. Fix the stale test that is silently blocking the test suite. Do not attempt the structural split — that is a later phase.
**Not in scope:** Feature work, refactoring of other files, the `stair_validate.py` / `stair_toc.py` split, the assembler split, the GPM work, the handoff protocol. All of those are blocked on this fix landing first.

---

## 0. WHY THIS DIRECTIVE EXISTS

`FIX_STAIR_LOOP_II.md` was written. It was not executed. The current code state is identical to the state that prompted that directive:

- `navigate()` still calls `dispatcher.dispatch()` inline (line 74)
- `_dispatch_llm()` is still defined but never called (lines 42–55)
- The keyword fallback is still present (lines 84–85)
- No wall-clock timeout exists anywhere
- `validate.py` still has only manifest integrity checks (24 lines)
- The regression tests do not exist
- The existing `test_stair_navigator.py` asserts `isinstance(result, dict)` against a function that returns `LeafPrediction` — **it is already failing, and either pytest is not being run or its output is being ignored**

The fact that the previous directive did not land is itself the most important diagnostic signal in this project. It means one of three things is true, and each requires a different response:

1. **The directive was not seen.** It was written in conversation but never saved to disk, so a fresh session had no way to find it. → Save this directive to `.context/FIX_STAIR_LOOP_III.md` before executing it.
2. **The directive was seen but deprioritized.** The loop stopped long enough that urgency faded and feature work resumed. → The priority ordering below addresses this by front-loading the smallest possible self-contained commit.
3. **The directive was attempted but the agent looped on it.** The most likely failure is that the agent tried to do all phases in one session and blew context. → This directive is split into smaller phases, each independently committable and verifiable.

**Before doing anything else:** save this directive to disk as `.context/FIX_STAIR_LOOP_III.md`. If the project has an `AGENTS.md` or `BOOTSTRAPPER.md`, add a one-line pointer to it. The next session must be able to find this document without being told.

---

## 1. INVARIANTS

1. **Small commits.** Each phase below is one commit. Do not merge phases. If any phase balloons past 30 minutes of work, stop and commit what you have — even a partial phase — rather than risk the session dying mid-change.
2. **Failing test before fix.** Phase 2 (failing tests) comes before Phase 3 (fix). The regression test must fail against the current code. If it passes, the test is wrong.
3. **Enforcement before feature.** Phase 4 (the `validate.py` gate) is not optional. Without it, the next session reintroduces the bug because there is no machine memory of the contract.
4. **Do not modify the working paths.** Manifest validation (`if predicted_id not in manifest_nodes`) and byte-mode hydration are correct. Do not touch them. The fix is narrow: remove the fallback, remove the inline dispatch, add the timeout, add the gate.
5. **Preserve the graph-loading path.** `_load_graph()` is correct. Do not touch it.
6. **The failing test is a deliverable, not a chore.** The commit that adds the failing test is the evidence that the fix fixes the right thing. Do not skip it.
7. **Do not attempt the structural split.** The `stair_validate.py` / `stair_toc.py` split is deferred. Doing it now obscures whether the single-prediction fix actually worked.

---

## 2. PHASE 0 — PRESERVE AND LOCATE

```bash
# 1. Save this directive to disk before executing it
# (Copy the contents of this doc to .context/FIX_STAIR_LOOP_III.md)

# 2. Add a pointer in AGENTS.md if it exists
# Append: "Active fix: see .context/FIX_STAIR_LOOP_III.md"

# 3. Backup
cp -r . /tmp/wa_fix3_backup_$(date +%Y%m%d_%H%M%S)

# 4. Stash any uncommitted work to verify baseline
git status
git stash push -u -m "pre-fix3 $(date +%Y%m%d_%H%M%S)"

# 5. Verify baseline
python -m pytest -x -q 2>&1 | tail -10
python .wiki/validate.py 2>&1 | tail -5
```

**If pytest fails at baseline:** stop and record the failure. That failure is *part of the problem this directive exists to fix*. The most likely failing test is `test_navigate_returns_result` in `tests/test_stair_navigator.py` (the stale `isinstance(result, dict)` assertion). Confirm which test fails:

```bash
python -m pytest tests/test_stair_navigator.py -v 2>&1 | tail -30
```

Record the exact failure. **Do not fix it yet.** Phase 1 fixes it as part of the sequence.

**If pytest passes at baseline:** the stale test is not being executed. Check:

```bash
# Is the test file being collected?
python -m pytest --collect-only tests/ 2>&1 | grep test_stair_navigator

# Is there a conftest.py that skips it?
grep -rn "skip\|xfail" tests/test_stair_navigator.py tests/conftest.py 2>/dev/null

# Is there a pytest.ini that excludes it?
cat pytest.ini setup.cfg pyproject.toml 2>/dev/null | grep -A5 "\[tool.pytest"
```

If the test is being skipped, that's a second bug — record it in `memory/ERRORS.md`. The fix will address it in Phase 1.

---

## 3. PHASE 1 — FIX THE STALE TEST (UNBLOCK)

The existing test asserts a `dict` from a function that returns `LeafPrediction`. This test is either failing (and being ignored) or skipped (and not running). Either way, it blocks the regression tests from being meaningful. Fix it first.

**Read the current test:**

```bash
cat tests/test_stair_navigator.py
```

**Expected current content (approximately):**

```python
def test_navigate_returns_result():
    result = navigate("test query")
    assert isinstance(result, dict)      # WRONG
    assert "node_id" in result           # WRONG

def test_navigate_empty_query():
    result = navigate("")
    ...
```

**Fix:**

```python
"""Tests for stair_navigator basic contract."""
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


def test_navigate_empty_query_returns_none_or_valid():
    """Empty query either returns None-node prediction or a valid one.
    It must NOT hang or loop."""
    import time
    start = time.monotonic()
    result = navigate("")
    elapsed = time.monotonic() - start
    assert elapsed < 30, "navigate('') exceeded 30s — timeout not working"
    assert isinstance(result, LeafPrediction)
```

**Verify:**

```bash
python -m pytest tests/test_stair_navigator.py -x -q
```

Both tests must pass. If `test_navigate_empty_query_returns_none_or_valid` fails because `navigate("")` hangs for more than 30 seconds, that confirms the missing timeout — Phase 3 will fix it. Record the observed hang duration.

**Commit 1:**

```bash
git add tests/test_stair_navigator.py
git commit -m "test(stair): fix stale test — navigate() returns LeafPrediction, not dict

The prior test asserted isinstance(result, dict) against a function that
returns LeafPrediction. Either the test was failing silently or was skipped.
This commit corrects the assertion and adds a wall-clock bound so a future
hang is caught by the test itself.

Baseline before this commit: [record pass/fail state]
Observed navigate('') duration: [record]s"
```

---

## 4. PHASE 2 — WRITE THE FAILING REGRESSION TESTS

These tests encode the single-prediction contract. They **must fail** against the current code. If they pass, the tests are not exercising the loop and the fix is unprovable.

**Append to `tests/test_stair_navigator.py`:**

```python
import pytest
from unittest.mock import patch


class TestSinglePredictionContract:
    """navigate() must dispatch exactly once per call. See FIX_STAIR_LOOP_III.md §1."""

    def test_dispatch_called_exactly_once(self, mocker):
        """A single navigate() call results in exactly one dispatch call.

        This test is expected to FAIL against the pre-fix code because the
        keyword fallback in navigate() can result in a second prediction
        attempt when the primary dispatch returns no usable node_id.
        """
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
            f"navigate() must be single-prediction — no keyword fallback, no retry. "
            f"See FIX_STAIR_LOOP_III.md §4."
        )

    def test_manifest_drift_returns_none_no_retry(self, mocker):
        """Predicted node not in manifest → None, no fallback, no second dispatch."""
        dispatch_spy = mocker.patch(
            ".agent.tools.stair_navigator._dispatch_llm",
            return_value={"node_id": "ghost-node", "confidence": 0.9}
        )
        mocker.patch(
            ".agent.tools.stair_navigator._load_manifest",
            return_value={"nodes": [{"id": "real-node"}]}  # ghost not present
        )
        mocker.patch(
            ".agent.tools.stair_navigator._load_graph",
            return_value=([{"id": "ghost-node"}], None)
        )

        result = navigate("test query")

        assert result.node_id is None, (
            "Manifest drift should return node_id=None, not a fallback match"
        )
        assert dispatch_spy.call_count == 1, (
            f"Drift must not trigger a second dispatch, got {dispatch_spy.call_count}"
        )

    def test_empty_graph_returns_none_no_dispatch(self, mocker):
        """Empty graph returns None without dispatching at all."""
        dispatch_spy = mocker.patch(".agent.tools.stair_navigator._dispatch_llm")
        mocker.patch(
            ".agent.tools.stair_navigator._load_graph",
            return_value=([], None)
        )

        result = navigate("test query")

        assert result.node_id is None
        assert dispatch_spy.call_count == 0, "Empty graph must not dispatch"


class TestNoLoopConstructs:
    """Static checks — the navigator file must not contain loop constructs."""

    def test_no_while_in_navigate(self):
        import ast, pathlib
        src = pathlib.Path(".agent/tools/stair_navigator.py").read_text()
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "navigate":
                for inner in ast.walk(node):
                    assert not isinstance(inner, ast.While), (
                        "navigate() contains a while loop — prediction must be single-shot. "
                        "See FIX_STAIR_LOOP_III.md §1."
                    )

    def test_inline_dispatch_removed(self):
        import pathlib
        src = pathlib.Path(".agent/tools/stair_navigator.py").read_text()
        assert "dispatcher.dispatch" not in src, (
            "Inline dispatcher.dispatch() present — must route through _dispatch_llm() only. "
            "See FIX_STAIR_LOOP_III.md §4."
        )

    def test_keyword_fallback_removed(self):
        import pathlib
        src = pathlib.Path(".agent/tools/stair_navigator.py").read_text()
        # The keyword fallback used 'query_lower' or 'query.lower()' in a loop.
        # Its presence is verifiable by checking for the specific pattern.
        has_keyword_scan = "query_lower" in src or (
            "query.lower()" in src and "for node in nodes" in src
        )
        assert not has_keyword_scan, (
            "Keyword fallback still present — second prediction attempt. "
            "See FIX_STAIR_LOOP_III.md §4."
        )
```

**Run the new tests and confirm they fail:**

```bash
python -m pytest tests/test_stair_navigator.py::TestSinglePredictionContract -x -q 2>&1 | tail -30
python -m pytest tests/test_stair_navigator.py::TestNoLoopConstructs -x -q 2>&1 | tail -30
```

**Expected failures:**

- `test_dispatch_called_exactly_once` — should fail because either `dispatcher.dispatch` is being mocked incorrectly or the keyword fallback runs an extra attempt
- `test_inline_dispatch_removed` — should fail because `dispatcher.dispatch` is present in the source
- `test_keyword_fallback_removed` — should fail because `query_lower` or the keyword scan pattern is present

If **any** of these pass against the current code, **stop and investigate**. The most likely cause is that the mocks aren't hitting the real dispatch path. Fix the mocks so the tests exercise the actual code — the fix is not provable if the tests can't fail.

**Record the failures in the commit message** — this is the evidence trail.

**Commit 2:**

```bash
git add tests/test_stair_navigator.py
git commit -m "test(stair): add failing regression tests for single-prediction contract

These tests encode the invariants from FIX_STAIR_LOOP_III.md §1.

Against current code:
- test_dispatch_called_exactly_once: FAIL (keyword fallback runs)
- test_manifest_drift_returns_none_no_retry: [pass or fail]
- test_empty_graph_returns_none_no_dispatch: [pass or fail]
- test_no_while_in_navigate: [pass or fail]
- test_inline_dispatch_removed: FAIL (dispatcher.dispatch present)
- test_keyword_fallback_removed: FAIL (query_lower present)

The fix commit makes these pass. Without this failing-test commit, the
fix is unprovable."
```

---

## 5. PHASE 3 — APPLY THE FIX

### 5.1 Read the current file

```bash
cat .agent/tools/stair_navigator.py
```

Confirm the state matches §0. If it doesn't, **stop**. The diagnosis is wrong and the fix needs re-diagnosis before proceeding.

Specifically confirm:

- `_dispatch_llm` is defined but not called
- `navigate()` calls `dispatcher.dispatch()` (or similar) inline
- A keyword scan exists with `query_lower` or `query.lower()` pattern
- No `signal.alarm`, no `_with_timeout`, no `NavigatorTimeout` class

### 5.2 Rewrite `navigate()` and add the timeout infrastructure

The new `navigate()` does exactly: one dispatch, one validation, one hydration, one return. Nothing else.

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

    Contract: exactly one dispatch call per invocation. If the prediction is
    unusable for any reason (dispatch error, timeout, manifest drift, low
    confidence), returns LeafPrediction(node_id=None). The caller (router)
    handles fallback.

    No keyword scan, no retry, no second dispatch. If you are tempted to add
    one, that is the bug this contract exists to prevent.

    See FIX_STAIR_LOOP_III.md §1 and §5.
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

- The inline `dispatcher.dispatch()` call (the entire try/except block that wraps it)
- The keyword scan (`for node in nodes: if query_lower in ...`)
- Any `while` loop (should not be present, but confirm)
- Any `except Exception:` or bare `except:` around the dispatch call
- Any import left unused by the removals (`dispatcher` if it's now unused)

**Keep unchanged:**

- `_load_graph()`, `_build_toc()`, `_load_manifest()`, `_build_prompt()`, `_hydrate()`
- The manifest validation logic (moved verbatim into the new `navigate()`)
- The `LeafPrediction` return type
- The byte-mode read in `_hydrate()`

### 5.3 Verify the tests now pass

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

Makes the regression tests from the previous commit pass.

See FIX_STAIR_LOOP_III.md §5."
```

---

## 6. PHASE 4 — ENFORCEMENT GATE IN validate.py

The fix is provable. The gate makes it **permanent**.

### 6.1 Read the current validate.py

```bash
cat .wiki/validate.py
```

Confirm it is ~24 lines and only checks manifest integrity. The gate below adds four new checks.

### 6.2 Add the checks

**Add to `validate.py` (as new top-level functions):**

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
                        f"see FIX_STAIR_LOOP_III.md §1"
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
            f"route through _dispatch_llm() only, see FIX_STAIR_LOOP_III.md §5"
        )
    has_keyword_scan = "query_lower" in src or (
        "query.lower()" in src and "for node in nodes" in src
    )
    if has_keyword_scan:
        violations.append(
            f"{nav_path}: keyword fallback present — second prediction attempt, "
            f"see FIX_STAIR_LOOP_III.md §5"
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
        return [f"missing graph.json or manifest.json"]
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

**Wire into `validate.py`'s main function:**

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

### 6.3 Verify the gate catches violations

```bash
# Test the loop check by introducing a temporary violation
python -c "
import ast
src = '''
def navigate(q):
    while True:
        pass
'''
tree = ast.parse(src)
found = False
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef) and node.name == 'navigate':
        for inner in ast.walk(node):
            if isinstance(inner, ast.While):
                found = True
print('AST check working:', found)
assert found
"
```

Then verify against the real file:

```bash
python .wiki/validate.py
# Should PASS with the current fixed code
```

**Commit 4:**

```bash
git add .wiki/validate.py
git commit -m "feat(validate): enforce navigator single-prediction contract at build time

Adds four checks that fail the build if violated:
- no while loops in navigate()
- no inline dispatcher.dispatch() (route through _dispatch_llm only)
- no keyword fallback
- line-count limits for assembly/ and .agent/tools/
- graph/manifest coherence

These make the fix from the previous commit permanent. Without this gate,
the next session that touches stair_navigator.py can reintroduce the bug
without anyone noticing until it loops again.

See FIX_STAIR_LOOP_III.md §6."
```

---

## 7. PHASE 5 — ADAPTER TIMEOUT

Defense in depth. The navigator already caps dispatch at 15 seconds. The adapter should also cap its own call so a hung adapter fails locally with a clear error rather than being interrupted by the navigator's alarm.

```bash
cat adapters/dispatch.py
```

**If the adapter is synchronous:** the navigator's `signal.alarm` already wraps it. The adapter timeout is optional. Skip this phase if the adapter is sync and the navigator's timeout is verified working.

**If the adapter is asynchronous:** wrap the underlying model call in `asyncio.wait_for`.

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

**Commit 5 (if adapter changed):**

```bash
git add adapters/dispatch.py
git commit -m "fix(adapter): add dispatch timeout — defense in depth for navigator cap

The navigator wraps dispatch in a 15s signal.alarm. The adapter also caps
its own call at 10s so a hung underlying call fails locally with a specific
error rather than being interrupted by the navigator's alarm.

See FIX_STAIR_LOOP_III.md §7."
```

---

## 8. PHASE 6 — END-TO-END VERIFICATION

Run the full pipeline. This is the *proof* the fix works in reality, not just in tests.

```bash
# 1. Full test suite
python -m pytest -x -q

# 2. Validation gate
python .wiki/validate.py

# 3. Real navigate() call in bounded time
python -c "
import time
from .agent.tools.stair_navigator import navigate
start = time.monotonic()
result = navigate('According to ADR-004, what was the decision?')
elapsed = time.monotonic() - start
print(f'navigate completed in {elapsed:.2f}s, node_id={result.node_id}')
assert elapsed < 20, f'navigate exceeded 20s ({elapsed:.2f}s) — timeout not working'
print('PASS: navigate bounded and returned')
"

# 4. Confirm single-dispatch via instrumentation
# Add a temporary counter if not already present, or check the adapter logs
grep -n "dispatch" provenance/turns.jsonl | tail -5
# Should show one entry per navigate() call, not two
```

---

## 9. ACCEPTANCE CRITERIA

- [ ] `.context/FIX_STAIR_LOOP_III.md` exists on disk.
- [ ] `tests/test_stair_navigator.py::TestSinglePredictionContract::test_dispatch_called_exactly_once` passes.
- [ ] `tests/test_stair_navigator.py::TestSinglePredictionContract::test_manifest_drift_returns_none_no_retry` passes.
- [ ] `tests/test_stair_navigator.py::TestSinglePredictionContract::test_empty_graph_returns_none_no_dispatch` passes.
- [ ] `tests/test_stair_navigator.py::TestNoLoopConstructs::test_no_while_in_navigate` passes.
- [ ] `tests/test_stair_navigator.py::TestNoLoopConstructs::test_inline_dispatch_removed` passes.
- [ ] `tests/test_stair_navigator.py::TestNoLoopConstructs::test_keyword_fallback_removed` passes.
- [ ] `grep -n "dispatcher.dispatch" .agent/tools/stair_navigator.py` returns empty.
- [ ] `grep -n "query_lower\|keyword.*fallback" .agent/tools/stair_navigator.py` returns empty.
- [ ] `grep -n "_with_timeout\|signal.alarm\|NavigatorTimeout" .agent/tools/stair_navigator.py` shows the timeout infrastructure.
- [ ] `validate.py` fails on a synthetic `while` in `navigate()` (verified by AST unit test or manual mutation).
- [ ] `validate.py` fails on a synthetic `dispatcher.dispatch` in the navigator.
- [ ] `validate.py` passes against the current code.
- [ ] A real `navigate()` call completes in under 20 seconds.
- [ ] `git log` shows the sequence: (1) fix stale test, (2) add failing regression tests, (3) apply fix, (4) add gate. The failing-test commit precedes the fix commit.

---

## 10. WHAT NOT TO DO

- ❌ Do not merge Phase 2 (failing tests) and Phase 3 (fix) into one commit. The failing test must be a separate commit so `git log` proves the fix fixed the right thing.
- ❌ Do not add retry logic to `navigate()` "to handle flaky dispatch." If the dispatch is flaky, fix the adapter. The navigator's contract is single-shot.
- ❌ Do not widen the 15-second timeout. If predictions time out, the cause is a slow adapter, an oversized ToC, or a wrong-tier dispatch. Fix the cause.
- ❌ Do not add a keyword fallback "as a safety net." The keyword fallback **is** the bug. The caller (router) falls back to VECTOR on `node_id=None`.
- ❌ Do not catch `Exception` around the dispatch. Catch `NavigatorTimeout` and `NavigatorDispatchError` specifically.
- ❌ Do not attempt the structural split (`stair_validate.py`, `stair_toc.py`) in this session. The split can land after the fix is committed and verified. Splitting first obscures whether the fix worked.
- ❌ Do not attempt the assembler split. Same reason.
- ❌ Do not "improve" the working paths while in the file. Manifest validation and byte-mode hydration are correct.
- ❌ Do not skip the `validate.py` gate. Without it, the next session reintroduces the bug because there is no machine memory of the contract.
- ❌ Do not skip the "save to disk" step in Phase 0. The previous directive didn't land, and the most likely reason is that it wasn't saved where a fresh session could find it.

---

## 11. COMMIT SEQUENCE

```
1. test(stair): fix stale test — navigate() returns LeafPrediction, not dict
2. test(stair): add failing regression tests for single-prediction contract
3. fix(stair): enforce single-prediction contract + 15s wall-clock cap
4. feat(validate): enforce navigator single-prediction contract at build time
5. fix(adapter): add dispatch timeout — defense in depth (if applicable)
```

Each commit independently verifiable. Each commit message records the verification state at that step. The `git log` is the evidence trail. If you cannot demonstrate from `git log` that the failing test landed before the fix, the fix is unprovable.

---

## 12. IF THE LOOP RETURNS ANYWAY

Even with the single-prediction fix and the wall-clock cap, a loop could theoretically re-emerge through:

- A caller that retries `navigate()` when it returns `None` (the router should not do this, but check)
- An adapter that hangs beyond 15 seconds in a way that `signal.alarm` cannot interrupt (e.g., blocking I/O in a non-main thread)
- A manifest so large that `_build_toc()` itself takes minutes (unlikely at current scale, but possible)

If a loop is observed after the fix:

1. **Check whether `navigate()` is being called more than once per session.** The router in `assembly/` should call it once and fall back to VECTOR on `None`. If it's retrying, that's a router bug, not a navigator bug.
2. **Check `provenance/turns.jsonl`** for the dispatch pattern. If there are N dispatch entries for one session, `navigate()` is being called N times.
3. **Check the wall-clock cap actually fires.** Add a deliberate `time.sleep(60)` to `_dispatch_llm` temporarily, run `navigate()`, confirm it raises `NavigatorTimeout` within 15 seconds, then remove the sleep.

If all three checks pass and the loop still occurs, the cause is somewhere else in the system. Do not keep patching the navigator. Do not add more timeouts. The fix directive is not the right tool for a loop that is not in `stair_navigator.py`. Diagnose the actual loop location using the earlier `FIX_STAIR_LOOP.md` five-hypothesis framework, applied to whatever component is actually looping.

---

## 13. AFTER THIS LANDS

Once all commits are in and verified:

1. **Structural split** (`CLEANUP_DIRECTIVE.md` Phase 3) — safe now, because the loop is provably gone and the split can proceed on a stable base.
2. **Assembler split** (`CLEANUP_DIRECTIVE.md` Phase 1) — the `plan.py` / `optimize.py` / `execute.py` / `feedback.py` decomposition.
3. **Loop detection protocol** (`IMPLEMENTATION_SCOPING_PROTOCOLS.md` Addendum II §2) — add `material_progress` to worker checkpoints and the four loop detectors.
4. **Handoff protocol** (`IMPLEMENTATION_HANDOFF_PROTOCOLS.md` Addendum I) — so future loops terminate with a resumable session rather than a hung worker.
5. **GPM** (main directive §4.2) — the transformation store that makes scoping cheaper over time.

None of those can land usefully until this fix is provably done and the gate is in place. This directive is the prerequisite for everything else.

---

**End of directive. The single most important rules: (1) save this to disk before executing; (2) write the failing test before the fix; (3) do not merge the failing test and the fix into one commit; (4) add the `validate.py` gate even though it feels like extra work — it's the only thing that prevents the next session from reintroducing the bug. The project has been stuck at this boundary before. The way to not get stuck again is to follow the sequence exactly and leave the evidence trail in `git log` so the next session inherits both the fix and the proof it was fixed.**