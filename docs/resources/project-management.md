# Project Management — Skills Shortlist

Skills relevant to project management specialization, from the
curated .harness/skills/ set and catalog/project-management.md
(dump is larger but unrated; install candidates one at a time).

## Planning and execution

- writing-plans: multi-step planning before touching code.
- executing-plans: running a plan inline as the implementer.
- brainstorming: requirements and design discovery before building.
- verification-before-completion: acceptance check before claiming done.
- dispatching-parallel-agents: independent workstreams.
- subagent-driven-development: plan execution with subagents.
- finishing-a-development-branch: integrate when implementation is complete.

## Quality gates in the delivery path

- test-driven-development: red-green before implementation code.
- systematic-debugging: root-cause-first diagnosis for failures.
- requesting-code-review + receiving-code-review: review loop.
- diagnosing-superpowers + using-superpowers: superpowers session health.
- using-git-worktrees: isolated feature work.

## Relation to the baselayer

These skills manage the delivery workflow around the baselayer;
the baselayer itself indexes documentation (docs/) into a DAG
(graph.json → manifest.json + wiki). For project management
specialization of the DAG itself (task states, owners, dates,
dependency semantics, critical-path queries), see the earlier
research thread — none of the 57 local skills provide CPM/PERT or
schedule modeling; the closest analogues are planning + git-worktree
isolation + Google Tasks-style dependency notes in OVERLAPS.md.
