# Build Repair — Sequencing, Done Criteria, Reporting

## Repair waves

Follow the waves in order. Do not start wave N+1 until wave N's exit criterion is met. Re-run the build after each file you touch.

### Wave 1 — Foundational DI (root cause A)

Files: `ChatRepositoryImpl.kt`, `AgentOrchestrator.kt`, `AgentTaskWorker.kt`, and the `ChatRepository` interface.

1. Add `ChatRepository.Companion.getInstance(context)` (A1).
2. Add `ChatRepository.getAgentOrchestrator()` only if the impl already constructs an orchestrator (A2).
3. Quarantine `AgentTaskWorker.kt` (A3).
4. Fix `ChatRepositoryImpl.executeTool` call site (A4).

Exit criterion: error count drops by at least 15 (to ≤271). No new errors introduced.

### Wave 2 — Compose UI (root cause B)

Fix in this order:
1. `AppNavigation.kt` (~22 errors; small, self-contained, unblocks navigation imports).
2. `ChatScreen.kt` (~79 errors; largest).
3. `WorkspaceScreen.kt` (~23 errors).
4. `ChatViewModel.kt` (~21 errors; likely cascading from ChatScreen).

Exit criterion: error count drops by at least 100 (to ≤171).

### Wave 3 — Type and syntax (root cause C)

Files: `FileGovernanceEngine.kt`, `SearchMemoryToolWorker.kt`, `AndroidApprovalPort.kt`, plus any cascade remaining from Wave 2.

Exit criterion: error count is 0.

### Wave 4 — Donor test pass

Run `sh gradlew testDebugUnitTest`. Fix test-compilation failures. Do not weaken or delete donor test assertions — if a donor test fails at runtime, the donor code is broken and the fix belongs in donor source, not in the test.

Exit criterion: `:core-engine`, `:security-interface`, and `:app` unit tests all green.

## Definition of done

1. `sh gradlew assembleDebug` exits 0.
2. `sh gradlew testDebugUnitTest` exits 0.
3. `docs/repair-report.md` exists and follows the template below.
4. `git diff main..HEAD --stat` shows only:
   - Source-file repairs
   - `quarantine/` moves
   - A `build.gradle.kts` sourceSets exclusion (if quarantine used)
   - `docs/repair-progress.md`, `docs/repair-report.md`, and an updated `docs/status.md`
   - No new feature files, no new dependencies (except as justified in the report).

## Verification commands

```bash
# Baseline — should print a number near 286
sh gradlew assembleDebug 2>&1 | grep -c "e: "

# After each wave
sh gradlew assembleDebug 2>&1 | tee /tmp/build.log
grep -c "e: " /tmp/build.log

# Final
sh gradlew assembleDebug testDebugUnitTest

# Diff check
git diff main..HEAD --stat
```

Use `sh gradlew`, not `./gradlew` — the wrapper is not exec-capable on shared storage in this environment.

## Reporting template — `docs/repair-report.md`

```markdown
# Harness Branch Repair Report

## Summary
- Baseline errors: 286
- Final errors: <N>
- Waves completed: <1, 2, 3, 4>
- Build: <pass|fail>
- Donor tests: <pass|fail>

## Root causes fixed
| ID | Root cause | Fix applied | Files touched |
|---|---|---|---|
| A1 | Missing ChatRepository factory | Added companion object | ChatRepository.kt |
| ... | ... | ... | ... |

## Quarantined
| File | Reason | Unresolved dependency |
|---|---|---|
| AgentTaskWorker.kt | Depends on OfflineSyncManager | OfflineSyncManager |

## Dependency additions (if any)
| Dependency | Version | Compiler error that required it |
|---|---|---|
| (none expected) | | |

## Donor components verified
- [ ] SecurityInterlock — tests passing, public API unchanged, fail-closed cases green
- [ ] WorkspacePathGuard — containment tests passing, rules unchanged
- [ ] AndroidKeyStoreManager — round-trip passing, cipher unchanged
- [ ] core-engine — unit tests passing, no Android imports

## Remaining known defects (out of scope, deferred to extraction)
- `fallbackToDestructiveMigration()` retained.
- `OfflineSyncManager` dependency unresolved; `AgentTaskWorker` quarantined.
- <any others discovered>

## Open questions
<anything the agent could not decide without human input>

## Diff summary
<output of `git diff main..HEAD --stat`>
```