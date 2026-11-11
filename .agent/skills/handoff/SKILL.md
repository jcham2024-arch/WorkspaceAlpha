---
tier: quarantine
last_reviewed: 2026-11-10
content_hash: c883d4d68868207190c560e60e55457165f49b03f8efbba430def6261d287972
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
author: Matt Pocock
category: productivity
date_added: 2026-06-19
description: Compact the current conversation into a handoff document for another agent to pick up.
license: MIT
license_source: ""https://github.com/mattpocock/skills/blob/main/LICENSE""
name: handoff
risk: safe
source: community
source_repo: mattpocock/skills
source_type: community
---argument-hint: "What will the next session be used for?"
disable-model-invocation: true
  - productivity
  - workflow
  - coding-agents
  - claude-code
  - codex-cli
  - cursor
---
## When to Use
Use when this workflow matches the user request: Compact the current conversation into a handoff document for another agent to pick up.
_Source: [mattpocock/skills](https://github.com/mattpocock/skills) (MIT)._
Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save in a fresh private temporary directory, with owner-only access where supported. Return its absolute path and note that temporary storage can be removed by the OS. Use an explicitly requested durable destination instead when the user supplies one.
Include verified state, uncompleted tasks, exact branch/commit and artifact paths, checks actually performed, authorization boundaries, known blockers and the next concrete action. Distinguish observed results from assumptions. A handoff does not authorize messaging another agent.
Include a "suggested skills" section in the document, which suggests skills that the agent should invoke.
Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.
Redact any sensitive information, such as API keys, passwords, or personally identifiable information.
If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
## Example
**User request:**
> Use @handoff for this task: Compact the current conversation into a handoff document for another agent to pick up.
## Limitations
- Requires the upstream tool, account, API key, or local setup when the workflow names one.
- Does not authorize destructive, production, paid, or external-message actions without explicit user approval.
- Validate generated artifacts or recommendations against the user's real sources before treating them as final.