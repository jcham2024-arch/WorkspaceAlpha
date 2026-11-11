# Decision metrics

Scope: metrics.jsonl schema + privacy rules + summarizer.
Load when: measuring gate behaviour or wiring metrics.

## Contents

- Field schema (v, session, tool, class, decision, reason, questions, sensitive, profile)
- Privacy rules
- Summarizer behaviour

## Checklist

- [ ] Metrics enabled only when decisions are being measured
- [ ] No paths, commands, file content, or session ids in lines
- [ ] File rotated past 1 MiB (`metrics.jsonl.1` replaces old)

## Commands

| Task | Command |
|---|---|
| Read/decisions | `metrics.jsonl` in state dir (`~/.gateguard`) |
| Summary | built-in summarizer reads `.1` then `metrics.jsonl`, skips malformed lines |

## Notes

- Fields: `v=1`; `session` = first 12 hex of sha256(session key); `tool` = Edit|Write|MultiEdit|NotebookEdit|Bash|PowerShell; `class` = target class or null; `decision` ∈ deny|credit|sibling|cap|trivial|pass-checked|pass-exempt|pass-subagent|routine-deny|routine-readonly|destructive-deny|pass; `reason` = short code; `questions` = question ids on denial; `sensitive`; `profile` when computed.
- Privacy: every text field short lowercase code or null; never contains paths/commands/content/session id. Errors ignored.
- Summarizer prints per-session and total: decisions by type, denials by class/reason, near-miss share, rates of denial/credit/sibling/cap/trivial among first touches, routine read-only passes, most-asked question ids.
