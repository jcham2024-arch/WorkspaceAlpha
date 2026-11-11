# AGENTS.md Effectiveness Test

No rigorous evidence yet that AGENTS.md improves task success (arXiv
2602.11988). Run this quarterly A/B on a small task set:

For each of 5 recurring tasks (e.g. seed+build after doc edit;
debug a failing test; add a skill to the master library):
- Run A: agent with AGENTS.md loaded.
- Run B: same agent, AGENTS.md withheld.
- Score: task success (validated by reviewer), token estimate,
  deviations from invariants.

Keep clauses that move the needle; delete or rewrite the rest. If a
clause never changes behavior, it is costing tokens without benefit.
Log each run as one line in memory/learnings.md.
