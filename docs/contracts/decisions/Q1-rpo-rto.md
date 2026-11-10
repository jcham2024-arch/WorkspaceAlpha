# Decision: Q1 — RPO/RTO Targets for Audit Persistence

## Context

The audit persistence spec requires configurable retention and durability guarantees. We need to define Recovery Point Objective (RPO) and Recovery Time Objective (RTO) targets that balance data safety with performance.

## Options Considered

| Option | RPO | RTO | Write Latency | Durability |
|--------|-----|-----|---------------|------------|
| A: Sync on every write (fsync) | 0 | < 1s | ~10-50ms | Maximum |
| B: Batch fsync every 100ms | ≤ 100ms | < 5s | ~1-5ms | High |
| C: Async with WAL checkpoint | ≤ 1s | < 30s | ~0.5ms | Standard |
| D: Application-level checkpoint | Configurable | Configurable | ~0.1ms | Tunable |

## Decision

**Option A (Sync on every write)** for the primary SQLite store.

**Rationale:**
- Audit trail is immutable by design — any loss is unacceptable
- Write volume is low (≈10-50 records/session), so latency cost is negligible
- WAL mode + `PRAGMA synchronous=FULL` provides crash consistency without application complexity
- JSONL secondary export provides additional durability layer

## Configuration

```yaml
audit:
  sqlite_synchronous: FULL
  wal_mode: true
  jsonl_flush_on_write: true
  checkpoint_interval_sec: 60  # WAL checkpoint, not data durability
```

## RPO/RTO Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| RPO (SQLite) | 0 records | `synchronous=FULL` + WAL |
| RPO (JSONL) | 0 records | Flush on each write |
| RTO (SQLite) | < 1 second | Single file, no recovery needed |
| RTO (JSONL) | < 5 seconds | Append-only, truncate on corruption |

## Validation

- Chaos test: kill -9 during write → verify 0 record loss on restart
- Benchmark: 1000 writes, measure p99 latency < 50ms
- Recovery test: corrupt WAL → verify clean restart

## Links

- Spec: `docs/specs/audit-persistence-spec.md`
- Tracking: `open-questions.md` (Q1)
- Implementation: `.agent/tools/knowledge.py`

---

*Decision recorded 2026-11-09. Update status in `open-questions.md` when implemented.*
