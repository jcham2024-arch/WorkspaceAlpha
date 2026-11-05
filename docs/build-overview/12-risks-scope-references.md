> **ChatWorkspace Build Task Overview** — Part 12 of 12
> Index: [`CONTEXT.md` §2.D](../../CONTEXT.md) · Prev: [`11-status-tracking-gates.md`](11-status-tracking-gates.md)

## 15. Risk-to-task mapping

Supplement §7 risks map to tasks as follows. When a risk materializes, the corresponding task is the mitigation point.

| Risk (supplement §7) | Mitigation task(s) |
|---|---|
| Donor carries hidden Apex assumptions | T-113 (checklist audit), T-117 (no broken-member refs) |
| Donor repository referenced by ported code | T-117 |
| Donor Room schema used destructive migration | T-015 (own schema from scratch), T-023, T-036 |
| Donor path guard assumes global root | T-017, T-110 |
| Donor interlock has no branch concept | T-075, T-116 |
| Donor engine has no streaming port | T-050, T-118 |
| Donor Compose uses non-existent M3 roles | T-057, T-109 |
| Donor provider manager assumes single active | T-039, T-107 |
| Donor audit store global | T-076, T-112 |
| JGit performance on large repos | T-018 (spike), T-033 (shallow clone) |
| MCP SDK maturity on Android | T-018 (spike), T-070/T-071 (fallback to REST behind same interface) |
| Prompt bloat from root docs | T-091 (line count test), T-095 (token counts) |
| Secret leakage in logs | T-043, T-111 |
| Branch divergence local vs remote | T-035, T-041 |
| Runaway tool loops | T-052 (loop cap), T-080 (timeout), T-106 (budget surfacing) |

---

## 16. Out of scope for this build

Per scope §18 and supplement §6, none of the following are tasks in this build:

- Non-OpenAI-compatible provider adapters (Anthropic native, Gemini native).
- Merge/PR creation UI.
- Multi-file atomic commits via Git Data API helper.
- Chat search, export, share.
- Background/scheduled agent runs.
- Workspace editing UI (agent-only writes).
- Multiple repositories per chat.
- Firebase, WorkManager, OfflineSyncManager.
- Replacing `fallbackToDestructiveMigration()` in the Harness branch (deferred to extraction, tracked in repair report §Remaining known defects).

---

## 17. References

| Document | Purpose |
|---|---|
| `ChatWorkspace — Project Scope & Build Plan` | Product requirements, architecture, acceptance criteria A1–A12 |
| `ChatWorkspace — Supplement A: Clean Build with Donor Parts` | Donor inventory D1–D11, adapter contracts, checklists, additional acceptance A13–A20 |
| Harness repair kit (prompt + `AGENTS.md` + 3 `context/for-agent/*.md`) | WS-R execution instructions |
| `docs/build-progress.md` (this file's companion) | Live task status |
| `docs/repair-report.md` (produced by WS-R) | Handoff from repair to port; §Remaining known defects feeds Phase 0 decisions |
| `docs/build-decisions.md` (created when fallback triggered) | Records WS-R slip and fallback activation |

---

**End of document.**
