> **ChatWorkspace Build Task Overview** — Part 2 of 12
> Index: [`CONTEXT.md` §2.D](../../CONTEXT.md) · Prev: [`01-overview.md`](01-overview.md) · Next: [`03-phase1-providers.md`](03-phase1-providers.md)

## 3. Phase 0 — Foundation (Week 1)

Goal: scaffold builds, donor parts compile, Harness branch is green (or the fallback path is taken).

### WS-R — Harness repair (parallel track)

| ID | Task | Depends | Acceptance |
|---|---|---|---|
| T-001 | Commit repair kit MD files to `Harness` (`AGENTS.md`, 3 `context/for-agent/*.md`) | — | Files present on branch, index readable |
| T-002 | Create `repair/compile` branch and run baseline build | T-001 | `docs/status.md` count matches actual (286) |
| T-003 | Wave 1: foundational DI (A1–A4) | T-002 | Error count ≤ 271 |
| T-004 | Wave 2: Compose UI (B1–B4) | T-003 | Error count ≤ 171 |
| T-005 | Wave 3: type and syntax (C1–C6) | T-004 | Error count = 0 |
| T-006 | Wave 4: donor tests green | T-005 | `testDebugUnitTest` exits 0 |
| T-007 | Write `docs/repair-report.md`; PR for human review | T-006 | Report follows template; diff shows repairs + quarantines only |

### WS-S — Scaffold

| ID | Task | Depends | Acceptance |
|---|---|---|---|
| T-010 | Create 8-module Gradle project with version catalog | — | `./gradlew projects` lists 8 modules |
| T-011 | Enforce module dependency rules via `api`/`implementation` | T-010 | `:core-engine` no-Android-imports check passes |
| T-012 [P] | Scaffold `:security`, `:workspace`, `:core-engine` module skeletons | T-010 | Modules build empty |
| T-013 [P] | Scaffold `:app`, `:data`, `:git`, `:mcp`, `:prompt` module skeletons | T-010 | Modules build empty |
| T-014 | Compose Navigation graph with 4 destinations (stubs) | T-013 | App runs, all 4 routes reachable |
| T-015 | Room `AppDatabase` with empty schema + explicit migration harness | T-013 | Migration test infrastructure present |
| T-016 | Manual DI container (match donor style — no Hilt/Koin) | T-015 | `AppContainer` provides database, repositories, managers |
| T-017 | `WorkspaceManager` scaffold with per-chat root and path sandboxing contract | T-012 | Unit test: `filesDir/chats/{id}/repo` created |
| T-018 | Dependency spike: JGit on Android, MCP Kotlin SDK on Android | — | Both compile in a test module; SPIKE.md written with findings |

### Phase 0 exit gate — M0

- **If WS-R green:** T-007 accepted, donor code confirmed extractable.
- **If WS-R not green by end of Week 1:** activate fallback — WS-P writes primitives from scratch using the supplement §3 adapter contracts as specification. Record decision in `docs/build-decisions.md`.
- T-010 … T-018 accepted.
- App runs with stub screens.

---
