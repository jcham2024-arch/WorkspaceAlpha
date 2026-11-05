# AGENTS.md — Harness Branch Repair

This repository is the Apex Agent app. The `Harness` branch has 286 Kotlin errors across 18 files per `docs/status.md`. The goal of this repair is to make it compile so four donor components can be extracted into a separate product (ChatWorkspace).

## Read order (mandatory)

1. `context/for-agent/preservation-rules.md` — what you must not break
2. `context/for-agent/known-issues.md` — the 286 errors, grouped by root cause, with per-root-cause fix guidance
3. `context/for-agent/build-repair.md` — repair waves, done criteria, reporting template

## Non-negotiable

- The build must pass: `sh gradlew assembleDebug`.
- Donor tests must pass: `sh gradlew testDebugUnitTest`.
- No features, no new dependencies, no rewrites.
- No deleting donor components.
- `docs/repair-report.md` must be written at the end.

## Status tracking

- Baseline error count: 286 (see `docs/status.md`).
- Update `docs/repair-progress.md` after every fix.

## Do not

- Do not read or edit `node_modules/`, `build/`, or `.gradle/`.
- Do not run `git push` or `git commit`.
- Do not commit or log secrets.