# CONTEXT — WorkspaceAlpha

Index of the documents in this repository. Update it whenever a file is added, moved, or renamed.

## 1. What this repository is

This repository holds the ChatWorkspace build documentation: the Harness branch repair kit and the
master build task index. It does not hold the Apex application source, which lives in the separate
repository `jcham2024-arch/Google-Ai-repo`, branch `Harness`.

## 2. File index

### 2.A — Repository root

| File | Purpose |
| :--- | :--- |
| `README.md` | Repository title. |
| `AGENTS.md` | Agent instructions for the Harness branch repair. |
| `CONTEXT.md` | This index. |

### 2.B — `context/for-agents/`

| File | Purpose |
| :--- | :--- |
| `preservation-rules.md` | Donor components that must not be broken by the repair. |
| `known-issues.md` | The 286 baseline errors grouped by root cause, with per-cause fix guidance. |
| `build-repair.md` | Repair waves, exit criteria, and the report template. |

### 2.C — `docs/`

No standalone files yet. See §2.D.

### 2.D — `docs/build-overview/` — ChatWorkspace Build Task Overview (chunked)

The master task index is split into parts of at most 200 lines each. Start at `01-overview.md`;
every part carries `Prev`/`Next` pointers.

| Part | File | Contents |
| :--- | :--- | :--- |
| 1 | `docs/build-overview/01-overview.md` | Document header, §0 How to use, §1 Workstreams, §2 Phase map |
| 2 | `docs/build-overview/02-phase0-foundation.md` | §3 Phase 0 — Foundation |
| 3 | `docs/build-overview/03-phase1-providers.md` | §4 Phase 1 — Providers |
| 4 | `docs/build-overview/04-phase2-chat-creation-git.md` | §5 Phase 2 — Chat Creation & Git |
| 5 | `docs/build-overview/05-phase3-chat-core.md` | §6 Phase 3 — Chat Core |
| 6 | `docs/build-overview/06-phase4-mcp-tools.md` | §7 Phase 4 — MCP & Tools |
| 7 | `docs/build-overview/07-phase5-prompt-docs.md` | §8 Phase 5 — System Prompt & Workspace Docs |
| 8 | `docs/build-overview/08-phase6-switch-polish.md` | §9 Phase 6 — Provider Switching & Polish |
| 9 | `docs/build-overview/09-phase7-hardening-release.md` | §10 Phase 7 — Hardening & Release |
| 10 | `docs/build-overview/10-dependencies-parallelization.md` | §11 Dependency graph, §12 Parallelization guide |
| 11 | `docs/build-overview/11-status-tracking-gates.md` | §13 Status tracking template, §14 Milestone gates |
| 12 | `docs/build-overview/12-risks-scope-references.md` | §15 Risk-to-task mapping, §16 Out of scope, §17 References |
