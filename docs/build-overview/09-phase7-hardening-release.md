> **ChatWorkspace Build Task Overview** — Part 9 of 12
> Index: [`CONTEXT.md` §2.D](../../CONTEXT.md) · Prev: [`08-phase6-switch-polish.md`](08-phase6-switch-polish.md) · Next: [`10-dependencies-parallelization.md`](10-dependencies-parallelization.md)

## 10. Phase 7 — Hardening & Release (Weeks 11–12)

Goal: internal-track build passes A1–A20, no donor checklist open.

| ID | Task | WS | Depends | Acceptance |
|---|---|---|---|---|
| T-110 | Cross-chat sandbox escape tests (`../other-chat/repo`) | WS-H | T-017, T-039 | A16 passes |
| T-111 | Secret redaction audit across logs and crash reporter | WS-H | T-043 | A10 passes; no secrets in 24h log capture |
| T-112 | Audit chain tamper test on fresh install | WS-H | T-076 | Chain verification passes after scripted 24h use |
| T-113 | Donor checklist audit — every item in supplement §4 | WS-P | all WS-P tasks | A13 passes |
| T-114 | Adapter contract tests in CI for all 4 adapters | WS-H | T-073, T-039, T-050, T-017 | A14 passes |
| T-115 | No-Android-imports check in CI for `:core-engine` | WS-H | T-011 | A15 passes |
| T-116 | Cross-chat escape and branch-guard end-to-end tests | WS-H | T-075, T-110 | A16, A17 pass |
| T-117 | No references to donor broken members | WS-H | T-113 | A19 passes |
| T-118 | Stream vs non-stream parity test in CI | WS-H | T-050 | A20 passes |
| T-119 | Crash/ANR sweep; StrictMode clean | WS-H | all | No StrictMode violations in 24h use |
| T-120 | Baseline profile generation | WS-H | all | Profile committed |
| T-121 | Device matrix: API 26, 30, 34+ | WS-H | T-119 | All pass smoke suite |
| T-122 | Release build: signing, R8, size audit | WS-H | T-121 | Signed AAB produced |
| T-123 | Play listing assets + internal track upload | WS-H | T-122 | Internal track receives build |
| T-124 | Final acceptance walkthrough A1–A20 | WS-H | T-123 | All 20 criteria demonstrated |

### Phase 7 exit gate — M7

- A1–A20 all pass.
- No donor checklist item open.
- Internal-track build available.

---
