---
owner: "taskmaster"
---# Communication Protocol — Human-Facing ↔ Subagent-Facing

Two orchestration roles, two channels, zero cross-talk:

- **Human-facing (conceptualizer)**: owns ALL messages to/from the
  human. Never talks to a subagent (coder / researcher / reviewer).
- **Subagent-facing (taskmaster)**: owns ALL messages to/from
  subagents, including internal planning. Never talks to the human.

All traffic between them is one of six message types. A message is
a file artifact + a one-line reply; chat carries no state.

| Type | Direction | Shape | When |
|---|---|---|---|
| SCOPE-LOCK | conceptualizer → taskmaster | scope doc path + 3-line summary + approval timestamp | Scope is locked with the human and recorded |
| PLAN-READY | taskmaster → conceptualizer (memo) | module DAG path + module count + slowest critical path | Internal plan is written (02-plan/plan.md) |
| APPROVAL | conceptualizer → taskmaster | approve / reject + reason | After every PLAN-READY the human read the plan summary |
| STATUS | taskmaster → conceptualizer | per-module: done / blocked / at-risk + one fact each | At each stage boundary and on any block |
| ESCALATION | either → the other | decision needed + who (human) + options + deadline | Irreversible or Ambiguous; never act unilaterally |
| FINAL-REPORT | taskmaster → conceptualizer | synthesis artifact path + what shipped / open / follow-ups | Run complete, reviewed, integrated |

Rules:

1. The human's word reaches subagents only as SCOPE-LOCK content.
2. An ESCALATION blocks its module until answered — design work
   stops, nothing keeps moving.
3. FINAL-REPORT is delivered to the human by the conceptualizer;
   the taskmaster does not summarize for the human.
4. Any message without the shape above is noise: file a STATUS
   correcting it.
5. The checkpoint (memory/checkpoints/) is the persistent record;
   the protocol carries pointers to it, not copies.
