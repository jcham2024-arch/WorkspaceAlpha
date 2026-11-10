# Open Architectural Questions

Tracking unresolved decisions that affect multiple components. Each question links to a decision note in `docs/contracts/decisions/` once resolved.

## Questions

| ID | Question | Status | Priority | Linked Spec | Decision Note | Owner |
|----|----------|--------|----------|-------------|---------------|-------|
| Q1 | What are the RPO/RTO targets for audit persistence? | **Open** | High | `audit-persistence-spec.md` | `Q1-rpo-rto.md` | taskmaster |
| Q2 | SQLite `synchronous=FULL` vs `NORMAL` benchmark results? | **Open** | High | `audit-persistence-spec.md` | `Q2-sqlite-sync.md` | taskmaster |
| Q3 | Key storage & rotation strategy for MCP secrets? | **Open** | Medium | `mcp-protocol-spec.md` | `Q3-key-rotation.md` | taskmaster |
| Q4 | Skill categorization schema stability guarantee? | **Decided** | Medium | `skill-lifecycle-spec.md` | `Q4-skill-categorization-stability.md` | conceptualizer |
| Q5 | Wiki render pipeline: incremental vs full rebuild? | **Decided** | Low | `wiki-render-spec.md` | `Q5-wiki-render-pipeline.md` | wiki-producer |
| Q6 | Profile provisioning: dynamic vs static skill lists? | **Decided** | Low | `profile-provisioning-spec.md` | `Q6-profile-provisioning.md` | conceptualizer |

## Status Definitions

| Status | Meaning |
|--------|---------|
| **Open** | Actively being investigated, no decision yet |
| **Decided** | Decision recorded in `docs/contracts/decisions/`, implementation pending |
| **Implemented** | Code matches decision, validated |
| **Deferred** | Not addressing in current scope |
| **Rejected** | Explicitly decided against with rationale |

## Resolution Process

1. **Investigate**: taskmaster dispatches researcher subagent
2. **Decide**: conceptualizer presents options to human, gets approval
3. **Record**: Write decision note in `docs/contracts/decisions/`
4. **Update**: Mark question **Decided** here, link decision note
5. **Implement**: taskmaster plans and executes implementation
6. **Verify**: validation passes, mark **Implemented**

## Escalation Triggers

- Question blocks ≥2 modules → ESCALATION to conceptualizer
- No progress in 3 sessions → ESCALATION with "stalled" flag
- Irreversible assumption needed → ESCALATION before acting

## History

| Date | Question | Resolution |
|------|----------|------------|
| 2026-11-07 | Master vs active skill folders? | Decided: `.agent/` master, `.harness/` active (see `DECISIONS.md`) |
| 2026-11-07 | Wiki location? | Decided: `.wiki/` subfolder, generated only |
| 2026-11-07 | Archive dump in git? | Rejected: 686M, gitignored, cleared after import |
| 2026-11-10 | Skill categorization schema stability? | Decided: Schema versioning, additive-only changes, v1.0.0 baseline |
| 2026-11-10 | Wiki render pipeline: incremental vs full? | Decided: Full rebuild default, incremental opt-in behind flag |
| 2026-11-10 | Profile provisioning: dynamic vs static? | Decided: Static frontmatter source of truth, dynamic dev-only fallback |

---

*Edit this file, then rebuild: `python3 .wiki/seed.py && python3 .wiki/build.py`*
