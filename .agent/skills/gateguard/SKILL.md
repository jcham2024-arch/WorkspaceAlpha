---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 80ece0a63d954b06c54168e96bd7f97e73361d1aa57dd32e79d71c8d0301820d
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
description: PreToolUse fact-forcing gate that denies the first Edit/Write/Bash (including MultiEdit and NotebookEdit) attempt until the agent presents concrete facts (importers, data schemas, verbatim user instruction), then allows retry; A/B-tested at +2.25 quality points. Use when enabling or configuring the GateGuard hook, exempting paths via env vars, or handling first-touch denials.
name: gateguard
origin: community
---
# GateGuard — Fact-Forcing Pre-Action Gate
Scope: first-touch gate on Edit/Write/Bash that forces investigation
before editing. Body is the workflow; detail lives in references/.
## When to Activate
- Codebase edits affect multiple modules
- Projects with data files with specific schemas/formats
- AI-generated code must match existing patterns
- The agent tends to guess instead of investigating
## Core Concept
LLM self-evaluation fails ("are you sure?" → always "yes").
Asking "list every file that imports this module" forces Grep/Read,
and the investigation itself creates context. Three-stage gate:
```
1. DENY  — block the first Edit/Write/Bash attempt
2. FORCE — tell the model exactly which facts to gather
3. ALLOW — permit retry after facts are presented
```
## Evidence
Two independent A/B tests, identical agents, same task:
| Task | Gated | Ungated | Gap |
| --- | --- | --- | --- |
| Analytics module | 8.0/10 | 6.5/10 | +1.5 |
| Webhook validator | 10.0/10 | 7.0/10 | +3.0 |
| **Average** | **9.0** | **6.75** | **+2.25** |
## Gate Types
### Edit / MultiEdit Gate (first edit per file)
MultiEdit is handled identically (each file gated individually);
NotebookEdit is gated as an Edit. For **code** targets:
```
Before editing {file_path}, present these facts:
1. List ALL files that import/require this file (search the tree — Glob/Grep)
2. List the public functions/classes affected by this change
3. If this file reads/writes data files, show field names, structure, and date format
   (use redacted or synthetic values, not raw production data)
4. Quote the user's current instruction verbatim
```
Full questions when the change cannot be read with confidence; otherwise
call-sites + data question dropped when no data is handled. Detail:
[questions-fit-the-change](references/questions-by-target-class.md).
### Write Gate (first new file creation)
Same four questions, reworded: 1. Who calls this file? 2. No existing
file serves the purpose? 3. Data schema? 4. Quote instruction.
Item 3 dropped when no data.
### Questions by target class
instruction / test / prose / config / code classes, matched on the
project-relative path; every class ends with "Quote the user's
current instruction verbatim". Full rules:
[questions-by-target-class](references/questions-by-target-class.md).
### Destructive Bash Gate (every destructive command)
Triggers on `rm -rf`, `git reset --hard`, `git push --force`,
`drop table`, etc.:
```
1. List all files/data this command will modify or delete
2. Write a one-line rollback procedure
3. Quote the user's current instruction verbatim
```
### Routine Bash Gate (once per session)
```
1. The current user request in one sentence
2. What this specific command verifies or produces
```
Read-only commands pass and are counted until the first command
fires the gate. Anything else (redirection, substitution, unknown
command, writes) makes it ordinary.
## Parallel Batches and Partial Application
First-touch evaluates each call independently. When several edits to
an untouched file ship in one parallel batch, the first is denied and
the denial marks the file checked — siblings are applied. Nothing is
rolled back. Rule: **dependent edits to an untouched file ship
sequentially, never inside a parallel batch.** After a denial,
present facts, retry, and re-read the file before building on
anything else from the batch.
## What Counts as Already Done
Denials are softened when the investigation already happened this
turn (prior-search credit), the edit is comment/whitespace-only, or a
sibling collapse applies. Full order of checks, sensitive and
hard-linked targets, prior-search credit rules, trivial-edit rules,
and sibling-collapse details:
[already-done](references/already-done.md).
## Quick Start
- **Option A (ECC hook, zero install):** the hook
  `scripts/hooks/gateguard-fact-force.js` is in this plugin; enable
  via hooks.json. To disable for setup sessions:
  `ECC_GATEGUARD=off`. In long sessions, full denials embed only
  the first `GATEGUARD_FACT_FORCE_FULL_DENIALS` (default 3); later
  denials condense.
- **Option B:** full package adds `.gateguard.yml` for per-project
  configuration (custom messages, ignore paths, gate toggles).
Graduated controls, decision metrics, glob semantics, and turning it
off completely: [env-vars](references/env-vars.md) and
[metrics](references/metrics.md).
## Anti-Patterns
- **Don't use self-evaluation instead.** "Are you sure?" always
  gets "yes" — experimentally verified.
- **Don't skip the data schema check.** A/B agents assumed ISO-8601
  when real data used `%Y/%m/%d %H:%M`. Checking data structure
  prevents this class of bugs.
- **Don't gate every Bash command.** Routine gates once per session;
  destructive gates every time. The balance avoids slowdown while
  catching real risks.
## Best Practices
- Let the gate fire naturally. Don't pre-answer the gate questions —
  real investigation before editing is what improves quality, and it
  is credited (see [already-done](references/already-done.md)).
- Customize gate messages for your domain.
- Use `.gateguard.yml` to ignore paths like `.venv/`, `node_modules/`, `.git/`.
## Related Skills
- `safety-guard` — Runtime safety checks (complementary, not overlapping)
## Platform variants
OS-specific companions for this skill:
- [Linux](platforms/linux.md)