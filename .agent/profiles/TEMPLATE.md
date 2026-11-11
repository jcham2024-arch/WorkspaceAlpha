---
name: <slug>
role: <one-line task description>
stage: 03-execute
model-tier: <smallest viable: e.g. low-context/no-thinking implementer | large-context/low-thinking manager | large-context/high-thinking specialist>
skills:
  - <from .agent/skills master, chosen per task by skill-picker>
tools:
  - .agent/tools/context.py section
reads:
  - .context/manifest.json (byte ranges only)
verify: "<how a reviewer proves this step is done>"
owner: "taskmaster"
---

# <Name> (fill from TEMPLATE; delete this line)

Model tier ladder (pick the smallest that can pass verification):

| Tier | Model class | Context size | When |
|---|---|---|---|
| 1 | smallest/fastest/cheapest | minimal (step package only) | Bounded, verifiable steps (write X, build Y, format Z) |
| 2 | mid | moderate (files + module context) | Steps needing style or cross-file coherence |
| 3 | largest | full project context | Open-ended design, judgment calls, final synthesis |

Default to Tier 1; escalate only on evidence (failed done check).

Parallelization checks:

- Any step with no shared inputs with another step runs parallel.
- Steps sharing a file serialize (one writer per file).
- Order dependents by the plan DAG, not by optimism.

Minimal context package per step:

1. Objective (one line).
2. Files (explicit list, never whole-repo).
3. Invariants it must not break.
4. Done condition (command + observed output).

Manager loop (manager tier): decompose → package → dispatch (batched,
independent) → check each result against done condition → package
whole task → return to taskmaster. No project conversation reaches
implementers.
