# Specs Directory — Readiness Table

This directory contains technical specifications for the Baselayer workspace. Each spec follows the governance model in `BOOTSTRAPPER.md` §3 (pipeline: docs → graph → manifest + wiki).

## Readiness Status

| Spec | Status | Last Updated | Linked Decisions | Implementation |
|------|--------|--------------|------------------|----------------|
| `audit-persistence-spec.md` | **Draft** | 2026-11-09 | [Q2-sqlite-sync.md](../contracts/decisions/Q2-sqlite-sync.md) | `knowledge.py` (partial) |
| `prompt-stack-spec.md` | **Draft** | 2026-11-11 | — | `envelope/`, `assembly/`, `adapters/`, `provenance/`, `schemas/` |
| `skill-lifecycle-spec.md` | Planned | — | [Q1-rpo-rto.md](../contracts/decisions/Q1-rpo-rto.md) | — |
| `mcp-protocol-spec.md` | Planned | — | [Q3-key-rotation.md](../contracts/decisions/Q3-key-rotation.md) | `.agent/tools/mcp/server.py` |
| `wiki-render-spec.md` | Planned | — | — | `.wiki/seed.py`, `.wiki/build.py` |
| `profile-provisioning-spec.md` | Planned | — | — | `.harness/sync_active.py` |

## Status Definitions

| Status | Meaning |
|--------|---------|
| **Draft** | Written, under review, not yet implemented |
| **Approved** | Human-approved, ready for implementation |
| **Implemented** | Code exists, tests pass, documented |
| **Deprecated** | Superseded by newer spec |
| **Planned** | Placeholder for future work |

## Governance

1. **New specs**: Create in `docs/specs/`, add row here, link decisions
2. **Status changes**: Update this table + `open-questions.md` + decision notes
3. **Implementation**: Track in `open-questions.md` Q-status column
4. **Validation**: `python3 validate.py` checks spec↔code consistency

## Cross-References

- **Open questions**: `open-questions.md` (root)
- **Decisions**: `docs/contracts/decisions/`
- **Build pipeline**: `BOOTSTRAPPER.md` §3
- **Agent profiles**: `.agent/profiles/*.md`

---

*Edit this file, then rebuild: `python3 .wiki/seed.py && python3 .wiki/build.py`*
