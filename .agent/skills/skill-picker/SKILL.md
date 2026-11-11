---
name: skill-picker
description: >-
  Use whenever the user has a task and wants to know which installed skill
  applies, or says "which skill", "what skill should I use", "pick a skill",
  "route this", or hands you a task without naming a skill. The picker reads
  the task, matches it against the 60 installed skills (including optimization,
  code simplification, and project debloat skills), and returns the single best
  skill plus a one-line why, the exact invocation, and any overlap or gap.
  Trigger this before starting any task whose domain matches an installed
  skill — do not default to doing the work yourself when a dedicated skill
  exists.
---

# Skill Picker

Pick the best installed skill for the user's task, then hand off to it.

## When to use

Use this skill at the start of any task where the user hasn't already named a
skill, whenever:

- The user asks "which skill should I use", "pick a skill", "route this", or
  hands you a task without naming a skill.
- The task clearly matches one of the installed skill domains (coding, debugging,
  testing, planning, browser automation, QA, reviewing, etc.).

Do not default to implementing the work yourself when a dedicated skill exists.
The picker's job is to identify and invoke the right skill, not to do the task
inline.

## The picking method

Follow these steps in order. Stop at the first step that produces a clear
winner.

### Step 1 — Check for an explicit skill request

If the user names a skill (e.g. "/ponytail", "use systematic-debugging",
"run a code review"), use that skill directly. Verify it exists in the
installed catalog below. If it doesn't exist, tell the user it's not installed
and offer the closest match from the catalog.

### Step 2 — Match the task to a domain

Read the task and map it to one domain:

| If the task is about… | Domain | Best skill |
|---|---|---|
| Writing, fixing, refactoring code — smallest change | Coding / lean dev | `ponytail` |
| Writing a failing test first, then code | TDD | `test-driven-development` |
| Finding root cause before fixing a bug | Debugging | `systematic-debugging` |
| Writing an implementation plan before coding | Planning | `writing-plans` |
| Executing a plan yourself (no subagents) | Execution | `executing-plans` |
| Executing a plan with parallel subagents | Execution | `subagent-driven-development` |
| Running 2+ independent tasks in parallel | Parallel agents | `dispatching-parallel-agents` |
| Reviewing a change for correctness/safety/load | Code review | `ponytail-review` |
| Auditing a whole repo (bloat, security, tests) | Repo audit | `ponytail-audit` |
| Listing deferred `shortcut:` comments | Tech debt | `ponytail-debt` |
| Showing ponytail measured savings | Benchmark | `ponytail-gain` |
| Ponytail levels/commands quick reference | Reference | `ponytail-help` |
| Claiming work is complete before committing | Verification | `verification-before-completion` |
| Receiving code review feedback | Code review (inbound) | `receiving-code-review` |
| Requesting a code review before merging | Code review (outbound) | `requesting-code-review` |
| Finishing a dev branch / integration | Branch finish | `finishing-a-development-branch` |
| Isolated feature work / git worktree | Workspace | `using-git-worktrees` |
| Finding and using skills at conversation start | Setup | `using-superpowers` |
| Creating/editing/verifying a skill | Skill authoring | `writing-skills` |
| Brainstorming before creating anything new | Ideation | `brainstorming` |
| Diagnosing why a superpowers session went wrong | Diagnosis | `diagnosing-superpowers` |
| Browser automation, scraping, CDP, cloud browser | Browser | `browser-use` |
| QA score a website/app (1-5) with evidence | QA | `qa` |
| Browser Use Cloud API/SDK docs | Cloud browser | `cloud` |
| browser-use open-source library Python code | Open-source browser | `open-source` |
| Isolated cloud browser from a sandbox | Remote browser | `remote-browser` |
| x402 / USDC pay-per-request browser payments | Payments | `x402` |
| Optimize code for speed/size/cost | Optimization | `performance-optimization`, `code-simplification`, `minimalist` |
| Agent context quality degrading | Optimization | `context-engineering` |
| LLM token/cost too high | Optimization | `llm-cost-optimizer` |
| Simplify overly complex code | Optimization | `code-simplification`, `caveman`, `minimalist` |
| Set quality bar / stop quality drift | Optimization | `constraint-driven-development` |
| Verify APIs exist, no hallucinations | Optimization | `strict-api`, `zero-hallucination-coder` |
| Identify bottleneck constraint | Optimization | `thinking-theory-of-constraints` |
| Buffer sizing under uncertainty | Optimization | `thinking-margin-of-safety` |
| Stop analysis at good-enough | Optimization | `thinking-bounded-rationality` |
| Resource allocation tradeoffs | Optimization | `thinking-opportunity-cost` |
| Rebuild from first principles | Optimization | `thinking-first-principles` |
| Production visibility / observability | Optimization | `observability-and-instrumentation` |
| Ground implementation in official docs | Optimization | `source-driven-development` |
| Tech stack selection / TCO | Optimization | `tech-stack-evaluator` |
| Simplify code for clarity | Code Simplify | `code-simplification`, `code-simplifier`, `clean-code` |
| Remove junk files, dead code | Project Debloat | `codebase-audit-pre-push`, `repo-maintainer` |
| Strip scaffolding, prune unused deps | Project Debloat | `lovable-cleanup`, `codebase-cleanup-refactor-clean` |
| Clean Code / SOLID / DRY / KISS / YAGNI | Code Simplify | `clean-code`, `clean-code-guard` |
| Reduce context window bloat | Optimization | `filesystem-context` |
| Non-semantic code cleanup | Code Simplify | `code-polish` |
| Avoid overcomplication | Code Simplify | `andrej-karpathy` |

### Step 3 — Resolve overlaps

If two skills could apply, prefer the more specific one:

- Debugging + code: `systematic-debugging` finds root cause; `ponytail` then
  applies the smallest fix. Use debugging first, then ponytail for the fix.
- TDD + bug fix: `test-driven-development` governs the write-test-first cycle;
  `systematic-debugging` governs finding the root cause. Use systematic-debugging
  first to find the cause, then TDD to implement the fix.
- Planning + executing: `writing-plans` writes the plan; `executing-plans` or
  `subagent-driven-development` carries it out. One task, two skills in sequence.
- Review + audit: `ponytail-review` reviews a change/diff; `ponytail-audit`
  audits the whole repo. Pick by scope.
- Browser + QA: `qa` scores a site with evidence; `browser-use` drives the
  browser. Use `qa` when the user wants a score/report; `browser-use` when they
  want automation or scraping.
- Performance + Debugging: `performance-optimization` finds bottlenecks;
  `systematic-debugging` finds root cause. Use debugging first if the cause is
  unknown, then performance-optimization to fix it.
- Code simplification + Ponytail: `code-simplification` reduces complexity;
  `ponytail` applies the smallest change. Use ponytail first for general lean
  dev, code-simplification for refactoring existing complex code.
- Minimalist + Ponytail: Both favor lean code. `ponytail` is the default for
  coding tasks; `minimalist` is for when over-engineering is the specific
  problem.
- Theory of constraints + Systematic debugging: `thinking-theory-of-constraints`
  finds the binding bottleneck; `systematic-debugging` finds root cause. Use
  constraints for throughput/latency pipeline issues, debugging for bugs.
- Code Simplify: `code-simplification` simplifies existing complex code;
  `code-simplifier` refines code for clarity/consistency; `clean-code` applies
  Clean Code principles; `clean-code-guard` reviews against SOLID/DRY/KISS/YAGNI.
  Use `code-simplification` for refactoring, `clean-code-guard` for review gates,
  `code-simplifier` for general cleanup.
- Project Debloat: `codebase-audit-pre-push` removes junk/dead code before push;
  `repo-maintainer` audits repository hygiene; `lovable-cleanup` strips project
  scaffolding and unused deps. Use `codebase-audit-pre-push` for pre-push cleanup,
  `repo-maintainer` for ongoing maintenance, `lovable-cleanup` for Lovable/Vite projects.
- Minimalist + Ponytail: Both favor lean code. `ponytail` is the default for
  coding tasks; `minimalist` is for when over-engineering is the specific
  problem.
- `caveman` has a broken SKILL.md (404) — use `minimalist` or `code-simplification`
  instead for minimalist coding guidance.

### Step 4 — Check for a gap

If no installed skill matches, say so plainly: "No installed skill covers
<domain>. The closest is <skill>." Offer to create a custom skill with
`writing-skills` if the user wants one.

## Output format

Return exactly this, nothing extra:

```
Recommended skill: <skill name>
Why: <one sentence matching the task to the skill's purpose>
Invoke with: skill_view(name="<skill-name>") — then follow that skill's instructions
Alternatives: <other skills that partially fit, or "none">
Overlap note: <why this beats the runner-up, or "none">
Gap check: <covered / no exact match — closest is <skill>>
```

If the user already named a skill, skip the catalog and confirm it exists:

```
Recommended skill: <user-named skill>
Why: You requested it directly.
Invoke with: skill_view(name="<skill-name>")
Alternatives: none
Overlap note: none
Gap check: covered
```

## Examples

**Example 1:** User says "my login form submits empty emails, fix it"

```
Recommended skill: systematic-debugging
Why: The task is an unexpected behavior (empty email accepted) that needs a root
cause before any fix.
Invoke with: skill_view(name="systematic-debugging") — four-phase root cause
investigation, then implement the smallest fix.
Alternatives: ponytail (apply the smallest fix after root cause is found)
Overlap note: systematic-debugging beats ponytail here because the root cause
is unknown; ponytail's "smallest fix" presumes you already know what to fix.
Gap check: covered
```

**Example 2:** User says "write a failing test first, then implement checkout"

```
Recommended skill: test-driven-development
Why: The user explicitly wants the write-test-first cycle.
Invoke with: skill_view(name="test-driven-development") — RED-GREEN-REFACTOR
with the iron law "no production code without a failing test first."
Alternatives: none
Overlap note: none
Gap check: covered
```

**Example 3:** User says "audit this whole codebase for bloat and security"

```
Recommended skill: ponytail-audit
Why: Whole-repo audit ranked by importance (correct, safe, holds under load,
tested, fast, lean).
Invoke with: skill_view(name="ponytail-audit") — one-shot report, changes
nothing.
Alternatives: ponytail-review (reviews a change/diff, not the whole repo)
Overlap note: ponytail-audit beats ponytail-review because the scope is the
whole repo, not a single change.
Gap check: covered
```

**Example 4:** User says "I need a custom skill for my workflow"

```
Recommended skill: writing-skills
Why: The task is to create a new skill, not to apply an existing one.
Invoke with: skill_view(name="writing-skills") — draft SKILL.md, test cases,
eval loop.
Alternatives: none
Overlap note: none
Gap check: covered
```

## How to hand off

After printing the recommendation, read the chosen skill with
`skill_view(name="<chosen-skill>")` and follow its instructions. Do not
re-implement the chosen skill's logic here — the picker routes, it does not
substitute.

If you are unsure between two candidates, state both, explain the tie-breaker,
and ask the user to confirm before proceeding.
