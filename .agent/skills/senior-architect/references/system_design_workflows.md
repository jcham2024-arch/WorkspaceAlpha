# System Design Workflows

Scope: system_design_workflows (senior-architect).
Load when: you need the system_design_workflows (senior-architect) detail described in SKILL.md.

## Contents

- System Design Workflows

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# System design workflow

1. Capture the user problem, success metric, observed workload and hard constraints. Record assumptions and missing evidence.
2. Trace one real request/event from caller through authorization, state change and external effects; list data owners and failures.
3. Describe the current design and the smallest change, then compare an alternative on reliability, consistency, latency, cost and team ownership.
4. Specify interfaces, idempotency/ordering, timeout/cancel, tenant boundaries, secrets and rollback. Schema evolution must support mixed-version deploys where relevant.
5. Draft a migration with checkpoints, safe abort conditions and observable correctness, including data reconciliation and rollback limits.
6. Propose bounded validation against realistic isolated fixtures. Record actual results separately from forecasts; do not run production load or provision resources without authority.

Deliver: evidence-linked current diagram, proposed diagram, decision record, unresolved risks, validation and rollout plan. No bundled script automates these steps.
