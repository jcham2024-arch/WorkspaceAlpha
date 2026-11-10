# Audit Persistence Specification

## Overview

This document specifies the persistence layer for audit logging in the Baselayer workspace. It defines how audit records are stored, queried, and retained across sessions.

## Requirements

### Functional Requirements

1. **Immutable Audit Trail**: Once written, audit records cannot be modified or deleted
2. **Queryable**: Support filtering by timestamp, agent, task, outcome, and tags
3. **Partitioned**: Store by date (YYYY-MM-DD) for efficient time-range queries
4. **Compressed**: Use efficient binary format for long-term storage
5. **Replicable**: Support export/import for backup and migration

### Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Write latency (p99) | < 10ms |
| Read latency (p99) | < 50ms for 10k records |
| Storage overhead | < 20% vs raw JSONL |
| Retention | Configurable, default 90 days |
| Durability | fsync on each write |

## Data Model

```json
{
  "version": 1,
  "timestamp": "2026-11-09T19:11:43.681771+00:00",
  "agent": "taskmaster",
  "task": "dispatch module X",
  "tier": "high-thinking",
  "outcome": "ok",
  "duration_ms": 1250,
  "tags": ["dispatch", "parallel"],
  "context_ref": "memory/checkpoints/abc123.json",
  "metadata": {
    "model": "claude-3.5-sonnet",
    "tokens_in": 4500,
    "tokens_out": 1200
  }
}
```

## Storage Format

### Primary: SQLite with FTS5

- Table: `audit_log` with columns matching data model
- FTS5 virtual table for full-text search on `task`, `tags`, `context_ref`
- Indexes on `timestamp`, `agent`, `outcome`
- WAL mode for concurrent reads during writes

### Secondary: Daily JSONL (export)

- Path: `memory/runs/YYYY-MM-DD.jsonl`
- One record per line
- Compressed with zstd after 7 days

## Governance

### Write Path

1. Agent emits record via `knowledge.py add --kind work`
2. `knowledge.py sync` writes to SQLite + JSONL atomically
3. Background job compresses JSONL older than 7 days
4. Retention job deletes partitions older than configured TTL

### Read Path

1. `knowledge.py search <query>` → FTS5 query
2. `knowledge.py last --kind work -n 5` → indexed timestamp query
3. Export: `knowledge.py export --since YYYY-MM-DD --format jsonl`

### Access Control

- Only the active agent session may write
- Read access via knowledge tool (no direct DB access)
- Export requires explicit human approval (ESCALATION protocol)

## Configuration

```yaml
audit:
  retention_days: 90
  compression_after_days: 7
  sqlite_path: ".context/audit.db"
  jsonl_dir: "memory/runs"
  wal_mode: true
  sync_on_write: true
```

## Migration Strategy

- Version field in each record enables schema evolution
- `knowledge.py migrate --to-version N` handles upgrades
- Backward compatibility: readers handle missing fields gracefully
- No downgrade support (immutable trail)

## Testing

- Property-based tests: write N records, verify all readable
- Chaos tests: kill process mid-write, verify no corruption
- Performance benchmarks: CI gate on latency targets
- Retention integration test: verify TTL cleanup

---

*This spec is part of the Baselayer documentation system. Edit source in `docs/specs/`, then rebuild with `python3 .wiki/seed.py && python3 .wiki/build.py`.*
