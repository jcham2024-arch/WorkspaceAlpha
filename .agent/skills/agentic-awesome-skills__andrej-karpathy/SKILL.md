---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 3af96edc70a839b6ca8c0f56b2f1f159f107d1ed84c529a97d5786c2f147c31b
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
author: renat
date_added: 2026-03-06
description: Behavioral guidelines to reduce common LLM coding mistakes. Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical changes, surface assumptions, and define verifiable success criteria.
license: MIT
license_source: ""https://github.com/multica-ai/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md""
name: andrej-karpathy
risk: safe
source: community
source_repo: multica-ai/andrej-karpathy-skills
source_type: community
  - coding-guidelines
  - code-review
  - llm-coding
  - simplicity
  - claude-code
  - antigravity
  - cursor
  - gemini-cli
  - codex-cli
------
# Karpathy Guidelines
Behavioral guidelines to reduce common LLM coding mistakes, derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls.
**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.
## When to Use This Skill
- Use when writing, reviewing, or refactoring code with an LLM.
- Use when a change needs to stay surgical and avoid speculative abstractions.
- Use when assumptions, tradeoffs, and verification criteria should be made explicit.
- Use when code has become overcomplicated and needs to be simplified.
## 1. Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**
Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.
## 2. Simplicity First
**Minimum code that solves the problem. Nothing speculative.**
- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.
Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.
## 3. Surgical Changes
**Touch only what you must. Clean up only your own mess.**
When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.
When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.
The test: Every changed line should trace directly to the user's request.
## 4. Goal-Driven Execution
**Define success criteria. Loop until verified.**
Transform tasks into verifiable goals:
- "Add validation" -> "Write tests for invalid inputs, then make them pass"
- "Fix the bug" -> "Write a test that reproduces it, then make it pass"
- "Refactor X" -> "Ensure tests pass before and after"
For multi-step tasks, state a brief plan:
```text
1. [Step] -> verify: [check]
2. [Step] -> verify: [check]
3. [Step] -> verify: [check]
```
Strong success criteria let you loop independently. Weak criteria such as "make it work" require constant clarification.
## Examples
```text
User request: "Add validation to this form."
Better response:
1. Assumption: validation should run before submit and show inline errors.
2. Plan: add a small validator, add tests for invalid inputs, then verify existing submit behavior.
3. Scope: only touch the form component and its test file.
```
```text
User request: "Refactor this service."
Better response:
1. Ask what behavior must remain unchanged.
2. Identify a concrete smell, such as duplicated parsing logic.
3. Make the smallest refactor and run the existing service tests.
```
## Limitations
- These guidelines are behavioral guardrails, not a replacement for project-specific architecture or style rules.
- For emergency fixes, prioritize the smallest verified correction over extensive planning.
- For exploratory prototypes, some caution can be relaxed, but assumptions and verification should still be explicit.