---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 4459d01ab1798ec1b0e08c422bc7b2697d10f931a4950d54dc2970a1415ae827
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
description: Patterns for continuous autonomous agent loops with quality gates, evals, and recovery controls. Use when running an agent loop that must self-check, gate on evals, and recover from failures.
name: continuous-agent-loop
origin: ECC
---
# Continuous Agent Loop
This is the v1.8+ canonical loop skill name. It supersedes `autonomous-loops` while keeping compatibility for one release.
## Loop Selection Flow
```text
Start
  |
  +-- Need strict CI/PR control? -- yes --> continuous-pr
  |
  +-- Need RFC decomposition? -- yes --> rfc-dag
  |
  +-- Need exploratory parallel generation? -- yes --> infinite
  |
  +-- default --> sequential
```
## Combined Pattern
Recommended production stack:
1. RFC decomposition (`ralphinho-rfc-pipeline`)
2. quality gates (`plankton-code-quality` + `/quality-gate`)
3. eval loop (`eval-harness`)
4. session persistence (`nanoclaw-repl`)
## Failure Modes
- loop churn without measurable progress
- repeated retries with same root cause
- merge queue stalls
- cost drift from unbounded escalation
## Recovery
- freeze loop
- run `/harness-audit`
- reduce scope to failing unit
- replay with explicit acceptance criteria