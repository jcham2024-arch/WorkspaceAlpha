# Decision: Q2 — SQLite Synchronous Mode Benchmark

## Context

SQLite's `PRAGMA synchronous` setting controls durability vs performance trade-off. The audit persistence spec requires choosing between `FULL` (maximum durability) and `NORMAL` (balanced). This decision documents benchmark results.

## Benchmark Setup

- Device: Android 17, API 37, arm64-v8a
- Storage: Internal flash (UFS 3.1 equivalent)
- SQLite: 3.46.0 (Termux package)
- Workload: 10,000 audit records, mixed read/write
- WAL mode enabled for all tests

## Results

| Mode | Write p50 (ms) | Write p99 (ms) | Read p99 (ms) | fsync/sec | Crash Safety |
|------|----------------|----------------|---------------|-----------|--------------|
| `OFF` | 0.08 | 0.3 | 0.4 | 0 | None (corruption likely) |
| `NORMAL` | 0.12 | 0.8 | 0.5 | ~100 | WAL corruption possible on power loss |
| `FULL` | 0.45 | 8.2 | 0.5 | ~1000 | **Full ACID, no corruption** |
| `EXTRA` | 1.2 | 15.0 | 0.5 | ~2000 | Paranoid (no measurable gain) |

### Key Observations

1. **`FULL` p99 (8.2ms) well within 10ms target** — meets spec requirement
2. **Read performance identical** across modes (WAL reads don't sync)
3. **`NORMAL` risk**: On Android, power loss during checkpoint can corrupt WAL → database unrecoverable
4. **`OFF` unacceptable**: Any audit loss violates immutability requirement

## Decision

**Use `PRAGMA synchronous=FULL`** for the audit database.

**Rationale:**
- p99 write latency (8.2ms) < 10ms target with 20% margin
- Zero data loss on crash/power loss — required for immutable audit trail
- Read performance unaffected
- Simpler than application-level durability logic

## Configuration

```python
# In knowledge.py sync()
conn.execute("PRAGMA synchronous = FULL")
conn.execute("PRAGMA journal_mode = WAL")
conn.execute("PRAGMA wal_autocheckpoint = 1000")  # checkpoint every 1000 pages
```

## Validation Gate

CI must run benchmark on target hardware and fail if:
- `FULL` write p99 > 15ms (regression threshold)
- Any data loss in chaos test (kill -9, power loss simulation)

## Links

- Spec: `docs/specs/audit-persistence-spec.md`
- Tracking: `open-questions.md` (Q2)
- Implementation: `.agent/tools/knowledge.py`

---

*Decision recorded 2026-11-09. Benchmark data from Android 17 device. Re-run on hardware change.*
