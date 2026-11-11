---
tier: experimental
last_reviewed: 2026-11-10
content_hash: ee7ce4e398461b9041e3c79560193adfa476a151b3eb9e7c09ef2f6f707b115a
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
description: Engineering operating model for teams where AI agents generate a large share of implementation output. Use when setting team process, review gates, or ownership rules for a codebase largely written by agents.
name: ai-first-engineering
origin: ECC
---
# AI-First Engineering
Use this skill when designing process, reviews, and architecture for teams shipping with AI-assisted code generation.
## Process Shifts
1. Planning quality matters more than typing speed.
2. Eval coverage matters more than anecdotal confidence.
3. Review focus shifts from syntax to system behavior.
## Architecture Requirements
Prefer architectures that are agent-friendly:
- explicit boundaries
- stable contracts
- typed interfaces
- deterministic tests
Avoid implicit behavior spread across hidden conventions.
## Code Review in AI-First Teams
Review for:
- behavior regressions
- security assumptions
- data integrity
- failure handling
- rollout safety
Minimize time spent on style issues already covered by automation.
## Hiring and Evaluation Signals
Strong AI-first engineers:
- decompose ambiguous work cleanly
- define measurable acceptance criteria
- produce high-signal prompts and evals
- enforce risk controls under delivery pressure
## Testing Standard
Raise testing bar for generated code:
- required regression coverage for touched domains
- explicit edge-case assertions
- integration checks for interface boundaries