> **ChatWorkspace Build Task Overview** — Part 11 of 12
> Index: [`CONTEXT.md` §2.D](../../CONTEXT.md) · Prev: [`10-dependencies-parallelization.md`](10-dependencies-parallelization.md) · Next: [`12-risks-scope-references.md`](12-risks-scope-references.md)

## 13. Status tracking template

Maintain `docs/build-progress.md` as a companion file. Each row:

```
| ID | Task | WS | Status | Owner | Started | Done | Notes |
|----|------|----|--------|-------|---------|------|-------|
| T-001 | Commit repair kit MDs | WS-R | done | A | 2026-01-05 | 2026-01-05 | 4 files |
| T-002 | Baseline build | WS-R | in-progress | A | 2026-01-06 | — | 286 confirmed |
| ... |
```

Status values: `not-started`, `in-progress`, `blocked`, `review`, `done`. Update on every state change. Milestone gates (§14) cannot pass with any task in that phase below `done`.

---

## 14. Milestone gates and sign-off

| Gate | Week | Sign-off by | Blocking criteria |
|---|---|---|---|
| M0 Foundation | 1 | Build lead | T-010–T-018 done; WS-R green OR fallback recorded |
| M1 Providers | 2 | Build lead | A1, A12 pass; D6–D8 checklists complete |
| M2 Git | 4 | Build lead + Eng A | A2, A3, A10 (Git) pass; failure paths recoverable |
| M3 Chat Core | 6 | Build lead | A9, A20 pass; D9 checklist complete |
| M4 MCP | 8 | Build lead + Eng A | A4, A6, A17 pass; D1–D3 checklists complete |
| M5 Prompt | 9 | Build lead | A7, A8 pass; regression suite green |
| M6 Switch | 10 | Build lead + QA | A5, A18 pass; all UI states covered |
| M7 Release | 12 | Release manager | A1–A20 pass; no checklist open; internal build uploaded |

No milestone may pass with an open donor checklist item in its scope, even if the acceptance criteria pass.

---
