---
tier: quarantine
last_reviewed: 2026-11-10
content_hash: c2f603f2314f3b0b100968a0b4d5c792910950d2370fa9318bd7ccd58a3a8b82
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
author: Matt Pocock
category: productivity
date_added: 2026-06-19
description: A relentless interview to sharpen a plan or design.
license: MIT
license_source: ""https://github.com/mattpocock/skills/blob/main/LICENSE""
name: grill-me
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
Use when this workflow matches the user request: A relentless interview to sharpen a plan or design.
_Source: [mattpocock/skills](https://github.com/mattpocock/skills) (MIT)._
Use the locally available `grilling` skill to interview the user about the plan. If the host does not expose slash commands, follow its question-by-question procedure directly. Establish the intended outcome, challenge assumptions and dependencies, and stop when the user-defined decision criteria are resolved or the user ends the interview. Do not claim `/grilling` executed merely because it was printed.
## Example
**User request:**
> Use @grill-me for this task: A relentless interview to sharpen a plan or design.
## Limitations
- Requires the upstream tool, account, API key, or local setup when the workflow names one.
- Does not authorize destructive, production, paid, or external-message actions without explicit user approval.
- Validate generated artifacts or recommendations against the user's real sources before treating them as final.