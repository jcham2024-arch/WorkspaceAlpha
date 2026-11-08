# Problems Registry

Errors found, root cause, fix, recurrence watch. Append-only.

## Entries

- 2026-11-07 | error: .agent/skills holds broken "404: Not Found" copies | tags: archive,quality
  Caveman / karpathy-coder / llm-cost-optimizer (plus 44 more dump
  sources, 47 total) shipped as 404 bodies. Fix: keep corruptored
  sources out of the live copy; quarantine + IMPORT_REPORT.
