# Lock Skip Locked

Scope: lock-skip-locked (supabase-postgres-best-practices).
Load when: you need the lock-skip-locked (supabase-postgres-best-practices) detail described in SKILL.md.

## Contents

- Lock Skip Locked

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
---
title: Use SKIP LOCKED for Non-Blocking Queue Processing
impact: MEDIUM-HIGH
impactDescription: 10x throughput for worker queues
tags: skip-locked, queue, workers, concurrency
---

## Use SKIP LOCKED for Non-Blocking Queue Processing

When multiple workers process a queue, SKIP LOCKED allows workers to process different rows without waiting.

**Incorrect (workers block each other):**

```sql
-- Worker 1 and Worker 2 both try to get next job
begin;
select * from jobs where status = 'pending' order by created_at limit 1 for update;
-- Worker 2 waits for Worker 1's lock to release!
```

**Correct (SKIP LOCKED for parallel processing):**

```sql
-- Each worker skips locked rows and gets the next available
begin;
select * from jobs
where status = 'pending'
order by created_at
limit 1
for update skip locked;

-- Worker 1 gets job 1, Worker 2 gets job 2 (no waiting)

update jobs set status = 'processing' where id = $1;
commit;
```

Complete queue pattern:

```sql
-- Atomic claim-and-update in one statement
update jobs
set status = 'processing', worker_id = $1, started_at = now()
where id = (
  select id from jobs
  where status = 'pending'
  order by created_at
  limit 1
  for update skip locked
)
returning *;
```

Reference: [SELECT FOR UPDATE SKIP LOCKED](https://www.postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE)
