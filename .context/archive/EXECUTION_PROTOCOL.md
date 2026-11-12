> **ARCHIVED 2026-11-12.** Superseded by `.context/STATUS.md`, which is the
> single current pointer for this workspace. Kept for history only — do not
> execute this document. The stair navigator repair it describes has landed;
> see STATUS.md §4.1 and `git log`.

---

# EXECUTION PROTOCOL: Land the Stair Navigator Fix in Slices

**Audience:** Implementation agent (human or model) executing the fix.
**Status:** COMPLETE. All six phases landed. This file is retained as the
execution record and as the meta-protocol for any future multi-phase fix.
**Relationship to other documents:** `.context/FIX_STAIR_LOOP.md` is the fix
specification. This document is the execution meta-protocol — *how* the fix
lands, not *what* the fix is.

---

## FIX PROGRESS

All phases verified against the current tree on 2026-11-12.

- [x] **Phase 1: Triage** — `stair_navigator.py` executable. `navigate('test query')`
      returns `LeafPrediction(node_id=None)` in 0.04s, no `NameError`.
- [x] **Phase 2: Target tests** — contract encoded; verified to fail against the
      pre-fix file (`8cdd6298`).
- [x] **Phase 3: Fix** — single-prediction contract + wall-clock cap applied.
- [x] **Phase 4: Gate** — `validate.py` checks added; gate catches a synthetic
      violation.
- [x] **Phase 5: Adapter timeout** — SKIPPED, deliberately. `adapters/dispatch.py`
      contains zero `async def` / `await` / `asyncio`. The navigator's
      `signal.setitimer` cap already bounds the sync call. Per §7 of this
      protocol: "If synchronous: the navigator's signal.alarm already caps it.
      Skip this phase."
- [x] **Phase 6: Verify end-to-end** — full suite, gate, real `navigate()` call.

Last updated: 2026-11-12.

### Notes and anomalies

1. **The premise of §0 was already stale when this protocol was executed.** §0
   describes a file with a `NameError` referencing `dispatcher`, `prompt`, and
   `max_tokens`. That file did not exist. The `NameError` was real but transient:
   it existed at commit `8cdd6298` and was removed by `517d90f0`, which also
   raised the file's syntax error (`SyntaxError` at line 123 — a `try` block
   with no matching `except`). Phase 1's goal was therefore already met before
   Phase 1 ran.

2. **Phase order differs from §11's expected sequence.** The protocol expects
   `triage → test → fix → gate → adapter → verify`. The actual order was
   `fix → test → gate → (docs) → test-hardening → verify`, because the fix
   landed before this protocol was written. The evidence-trail requirement is
   still satisfied: the regression tests were verified to fail against
   `8cdd6298` before being committed against fixed code.

3. **Phase 6 step 4 is not wired.** `grep -c "dispatch" provenance/turns.jsonl`
   returns 0. The navigator does not write to provenance, and no caller invokes
   `navigate()` from the assembled pipeline yet. Single-dispatch is instead
   proven by call-count assertions in
   `tests/stair/test_single_prediction_contract.py`. Wiring the navigator into
   `assembly/assembler.py` is outside this protocol's scope (it is the main
   retrieval directive's §2.5).

4. **`pytest` is unavailable in this environment** (`No module named pytest`).
   All tests are stdlib `unittest`. The protocol's `pytest` invocations were
   translated to `python -m unittest` equivalents; `mocker.patch` became
   `unittest.mock.patch`.

5. **`python .wiki/validate.py` does not exist.** The validator is `./validate.py`
   at the repo root. All references were translated.

6. **Golden-file coupling.** Adding §11 to `AGENTS.md` tripped
   `test_golden.py::test_agents_md_matches_golden`. The golden copy at
   `tests/fixtures/golden/AGENTS.md` was regenerated, since the edit was
   intentional. If that golden file is meant to be pinned externally rather than
   regenerated, revert both.

7. **Pre-existing failures unrelated to this work.** 7 tests fail on `main` and
   predate it: 5 in `test_provision`, 1 in `test_redaction` (missing
   `import unittest`), 1 in `test_seed` (`test_one_node_per_heading`, 3654 != 3972).
   None touch the navigator. Recorded here so a future session does not mistake
   them for regressions.

---

## §1 — THE LEDGER DISCIPLINE (retained for future fixes)

The ledger above is the mechanism that makes a multi-phase fix survivable. The
rules that made it work:

1. **One phase per session.** Do not attempt Phase 2 in the same session as
   Phase 1. Each phase is a commit. Stop after the commit.
2. **Time-box each phase to 20 minutes.** If a phase is exceeding the box, stop.
   Commit what you have — even an incomplete phase that leaves the repo valid.
   Do not loop.
3. **Never leave the repo broken at commit time.** Every commit must leave the
   code importable and the test suite no worse than before.
4. **Update the ledger before every commit.** If the commit is the last one
   before a session ends, the ledger is the handoff.
5. **No phase introduces functionality beyond its stated scope.** If a bug is
   found during a phase, note it in `Notes` and move on.
6. **Backup before Phase 1.**
7. **If you cannot explain what you are about to commit in one sentence, do not
   commit it.**

## §2 — PHASE CRITERIA (as executed)

| Phase | Goal | Verification |
| :--- | :--- | :--- |
| 1 Triage | `navigate()` returns `LeafPrediction`, no `NameError` | `isinstance(result, LeafPrediction)`, 0.04s |
| 2 Target tests | Contract encoded, fails pre-fix | 3 static tests confirmed failing against `8cdd6298` |
| 3 Fix | One dispatch, wall-clock cap | `dispatch_prediction(query` appears once; `setitimer` + `TIMEOUT_SECONDS = 15.0` |
| 4 Gate | `validate.py` enforces the contract | 5 check functions; fixture `tests/fixtures/bad_navigator.py` proves each fires |
| 5 Adapter | Defense in depth | Skipped — adapter is synchronous |
| 6 Verify | Whole system works | 33 stair+gate tests pass; `validate.py` passes; `navigate()` 0.09s |

## §3 — WHEN A PHASE FAILS

Stop the session. Do not attempt to fix it in the same session. Record in the
ledger: which phase failed, the exact error, the last working commit hash, and
any partial work. Then `git stash push -u -m "phase-N-blocked"` and end.

The pattern that broke four prior attempts: try to do too much in one session,
hit a snag, loop on it, run out of context, commit nothing. The pattern that
lands the fix: one phase per session, time-boxed, commit regardless of
perfection, hand off via the ledger.

## §4 — WHAT COMES AFTER

None of these are blocked by this protocol any more:

1. Structural split — already landed (`stair_validate.py`, `stair_toc.py`).
2. Assembler split — `assembly/assembler.py` is 458 lines, over the 200-line
   limit `validate.py` now enforces with a waiver.
3. Wire `navigate()` into `assembly/assembler.py` before the Plan step, and
   record the routing decision to provenance (retrieval directive §2.5).
4. Loop detection protocol — Addendum II §2 (`material_progress`).
5. Handoff protocol — Addendum I (`sessions/`).
6. GPM distillation — retrieval directive §4.2.

---

**End of protocol. The lesson that generalises: a fix specified four times and
never landed was not a specification problem. It was an execution-size problem.
Work smaller than feels necessary, commit each slice, and keep the ledger where
the next session will find it.**
