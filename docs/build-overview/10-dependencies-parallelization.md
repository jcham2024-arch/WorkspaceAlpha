> **ChatWorkspace Build Task Overview** — Part 10 of 12
> Index: [`CONTEXT.md` §2.D](../../CONTEXT.md) · Prev: [`09-phase7-hardening-release.md`](09-phase7-hardening-release.md) · Next: [`11-status-tracking-gates.md`](11-status-tracking-gates.md)

## 11. Dependency graph (critical path)

```
T-001 → T-002 → T-003 → T-004 → T-005 → T-006 → T-007  (WS-R)
                                    ↘
T-010 → T-011 → T-012 ────────────→ T-020 → T-021 → T-024 → T-025/26/27 → T-029
                 ↓                   T-022
T-013 → T-014 → T-016               T-023 → T-036 → T-037 → T-040 → T-041
         ↓                           ↓
       T-042                       T-039 → T-100 → T-101 → T-107
                                  
T-018 → T-033 → T-034 → T-035
              → T-031 → T-030 → T-037

T-050 → T-051 → T-052 → T-054 → T-056 → T-078 → T-079
                              ↓
                            T-059 → T-061

T-070 → T-071 → T-077
T-073 → T-074 → T-075
T-090 → T-091 → T-092 → T-094 → T-095 → T-096/97

T-110 … T-124 (serialized hardening)
```

Critical path: **T-010 → T-013 → T-014 → T-031 → T-033 → T-037 → T-040 → T-050 → T-051 → T-052 → T-054 → T-056 → T-073 → T-075 → T-077 → T-090 → T-095 → T-124**. Any slip on this path moves M7 by the same amount.

---

## 12. Parallelization guide

Two-engineer split (recommended, ~8-week fast path):

- **Engineer A (donor + core):** WS-R, WS-P, and the `:core-engine` / `:security` work in WS-I. Owns T-001–T-007, T-020–T-022, T-028, T-039, T-044, T-050, T-073–T-076, T-113.
- **Engineer B (feature + UI):** WS-S, WS-N, and the chat UI portion of WS-I. Owns T-010–T-018, T-023–T-027, T-030–T-038, T-040–T-042, T-052–T-060, T-070–T-072, T-077–T-079, T-090–T-094, T-100–T-108.
- **Shared:** WS-H testing tasks split by domain; review both directions.

Three-engineer split (~6-week fast path): add a third engineer for WS-H from Week 5, plus a UI specialist for T-056–T-057, T-078–T-079, T-102–T-105.

One-engineer split (~12-week baseline, per scope): serialize WS-R and WS-S in Week 1; accept that Wave 3 of the repair (T-005) may slip to Week 2 and delay T-020 by a few days.

---
