---
tier: quarantine
last_reviewed: 2026-11-10
content_hash: 64e02d0197c027560e8cb6dbb9230d79a4815dc5b573bb361856917b1a1b070a
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
author: Matt Pocock
category: productivity
date_added: 2026-06-19
description: A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
license: MIT
license_source: ""https://github.com/mattpocock/skills/blob/main/LICENSE""
name: grill-with-docs
risk: safe
source: community
source_repo: mattpocock/skills
source_type: community
---disable-model-invocation: true
  - productivity
  - workflow
  - coding-agents
  - claude-code
  - codex-cli
  - cursor
---
## When to Use
Use when this workflow matches the user request: A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
_Source: [mattpocock/skills](https://github.com/mattpocock/skills) (MIT)._
Use the installed `grilling` procedure to ask one meaningful question at a time. Inspect existing ADR/glossary conventions first. Record only confirmed answers in authorized project docs, mark open proposals as Proposed, preserve conflicting alternatives and review the resulting diff. Use `domain-modeling` only if installed and relevant; do not invent a slash-command dependency.
## Example
**User request:**
> Use @grill-with-docs for this task: A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
## Limitations
- Requires the upstream tool, account, API key, or local setup when the workflow names one.
- Does not authorize destructive, production, paid, or external-message actions without explicit user approval.
- Validate generated artifacts or recommendations against the user's real sources before treating them as final.