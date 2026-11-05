> **ChatWorkspace Build Task Overview** — Part 8 of 12
> Index: [`CONTEXT.md` §2.D](../../CONTEXT.md) · Prev: [`07-phase5-prompt-docs.md`](07-phase5-prompt-docs.md) · Next: [`09-phase7-hardening-release.md`](09-phase7-hardening-release.md)

## 9. Phase 6 — Provider Switching & Polish (Week 10)

Goal: mid-chat switch works, all UI states covered, workspace inspector.

| ID | Task | WS | Depends | Acceptance |
|---|---|---|---|---|
| T-100 | Chat top-bar provider/model dropdown | WS-N | T-056, T-039 | Selecting updates session; next turn uses new provider |
| T-101 | System-note append on switch | WS-I | T-100, T-054 | A5 passes (history preserved, note appended) |
| T-102 [P] | Workspace Inspector screen (read-only, guarded) | WS-N | T-017, T-039 | Read via `PerChatPathGuard`; no write path |
| T-103 [P] | Error banners, cancel, retry, loop cap surfacing | WS-N | T-058, T-060 | All error paths have UI |
| T-104 | Accessibility pass (labels, contrast, touch targets) | WS-H | all UI | TalkBack walkthrough passes |
| T-105 | Dark theme + empty/loading states | WS-N | all UI | All four screens themed |
| T-106 | Iteration cap (8) config + budget surfacing | WS-I | T-073 | Cap error surfaced clearly |
| T-107 | Per-chat provider resolution test on switch | WS-H | T-100, T-039 | A18 passes |
| T-108 | Delete/rename/archive chat actions | WS-N | T-042 | Long-press menu works; delete cascades |
| T-109 | Polish pass: spacing, transitions, icons imports | WS-N | all UI | Lint clean; no missing import warnings |

### Phase 6 exit gate — M6

- A5 (mid-chat switch preserves history) passes.
- A18 (switch affects only that chat) passes.
- All UI states covered.

---
