---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 7220ea07bad36152cf3ec8aab936a942e848566a43637924cd960e40734813b5
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
description: Operate and extend NanoClaw, ECC's zero-dependency session-aware REPL, with persistent markdown-backed sessions and slash commands for model switching, skill loading, session branching, cross-session search, history compaction, and export. Use when running or extending scripts/claw.js, or when resuming, branching, compacting, searching, or exporting a NanoClaw session.
name: nanoclaw-repl
origin: ECC
---
# NanoClaw REPL
Use this skill when running or extending `scripts/claw.js`.
## Capabilities
- persistent markdown-backed sessions
- model switching with `/model`
- dynamic skill loading with `/load`
- session branching with `/branch`
- cross-session search with `/search`
- history compaction with `/compact`
- export to md/json/txt with `/export`
- session metrics with `/metrics`
## Operating Guidance
1. Keep sessions task-focused.
2. Branch before high-risk changes.
3. Compact after major milestones.
4. Export before sharing or archival.
## Extension Rules
- keep zero external runtime dependencies
- preserve markdown-as-database compatibility
- keep command handlers deterministic and local