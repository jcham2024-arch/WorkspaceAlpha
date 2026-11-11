---
owner: "taskmaster"
---# Profiles — Specialized Agent Definitions

One Markdown file per specialized agent (general form; sub-profiles
come later as additional files). Frontmatter is the machine routing
table (role, stage, skills, tools, reads, verify); the body is the
role prompt. A profile also **dictates provisioning**: its frontmatter
`skills:` list is exactly what gets synced from the master library
(.agent/skills/) into the currently-used set (.agent/harness/skills/) by
`python3 .agent/tools/provision.py --profile <name>`.

## The roster

Orchestration is two communication roles (human-facing conceptualizer
↔ protocol ↔ subagent-facing taskmaster), three execution specialists
(coder, researcher, reviewer), plus three **managers** that sit between
the taskmaster and implementers.

Model tiers: orchestrator = large context + high thinking;
manager = large context + low thinking (decompose, package, review);
implementer = low context + no thinking (execute steps only).

| Profile | Stage | Top-of-the-line ask | Skills (provisioned) |
|---|---|---|---|
| conceptualizer | 01-navigate (human-facing) | Talk to the human; question the idea; lock scope; collect approvals; present results. Never talks to subagents. | brainstorming, writing-plans, thinking-first-principles, thinking-margin-of-safety |
| taskmaster | 02-plan → 03-execute (subagent-facing) | Internalized planning, dispatch via domain managers, supervision, integration, synthesis. Ties out to the conceptualizer via protocol.md. Never talks to the human. | dispatching-parallel-agents, subagent-driven-development, executing-plans, skill-picker, context-engineering, filesystem-context, diagnosing-superpowers, using-git-worktrees, verification-before-completion, requesting-code-review, receiving-code-review, finishing-a-development-branch, thinking-theory-of-constraints, thinking-opportunity-cost |
| coder | 03-execute | Root cause over symptoms; smallest correct diff; test-first; no hallucinated APIs; measure perf | systematic-debugging, test-driven-development, clean-code-guard, clean-code, andrej-karpathy, strict-api, constraint-driven-development, minimalist, ponytail, code-simplification, performance-optimization, observability-and-instrumentation, source-driven-development, verification-before-completion, red-green-proof |
| researcher | 01-navigate | Evidence over intuition; primary sources; tradeoff matrices; security-first dependency triage | skill-picker, open-source, source-driven-development, tech-stack-evaluator, context-engineering, filesystem-context, thinking-first-principles, thinking-bounded-rationality, thinking-margin-of-safety, browser-use, remote-browser |
| reviewer | 04-verify | Diff-first adversarial audit with receipts; invariants, secrets, API truth, constraints | requesting-code-review, receiving-code-review, verification-before-completion, clean-code-guard, codebase-cleanup-refactor-clean, code-polish, ponytail-review, ponytail-audit, repo-maintainer, thinking-theory-of-constraints, strict-api |

Managers (taskmaster delegates to these, never to bare implementers):

| Profile | Task type | Decomposes into | Skills (provisioned) |
|---|---|---|---|
| research-manager | Research | independent search/extract steps, each with query + source + output shape | dispatching-parallel-agents, subagent-driven-development, skill-picker, open-source, source-driven-development, tech-stack-evaluator, context-engineering, filesystem-context, thinking-bounded-rationality |
| coding-manager | Build (task-agnostic) | Designs a per-task profile: smallest viable model tier, minimal-context steps, skill per step (skill-picker) | dispatching-parallel-agents, subagent-driven-development, systematic-debugging, test-driven-development, clean-code-guard, constraint-driven-development, verification-before-completion, red-green-proof |
| review-manager | Review | check steps (invariants, quality, secrets, API truth) | dispatching-parallel-agents, subagent-driven-development, requesting-code-review, receiving-code-review, verification-before-completion, clean-code-guard, ponytail-review, ponytail-audit, repo-maintainer, thinking-theory-of-constraints |

Run a provision to activate a role (conceptualizer is the default);
then refresh the index with `python3 .agent/tools/gen_skills_index.py`.
New task-specific profiles are generated per task from
`TEMPLATE.md` (model tier ladder, minimal context, parallel checks).
Sub-profiles (sprint-lead, frontend-coder, security-auditor, …)
live as extra files here and declare a superset/subset of the base
role's skills. The wiki-facing role is `wiki-producer.md` (human
HTML production; linked from `.wiki/agent.md`).
