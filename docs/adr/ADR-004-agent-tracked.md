# ADR-004: Why .agent/ Is Tracked in Git (Model A)

## Status

Accepted

## Context

The `.agent/` directory holds the master skill library (3,520 skills), agent profiles, tools, MCP server, and machine registry. Two deployment models were considered:

**Model A (tracked):** `.agent/` is source-controlled. Only `.agent/.env` (secrets) and `.agent/.harness/` (provisioned snapshot) are gitignored.

**Model B (untracked):** `.agent/` is provisioned by bootstrap on each clone. Only `.agent/README.md` and `.agent/.env.example` are tracked via negation rules.

## Decision

**Model A (tracked)**. The full master skill library is committed to git. Rationale:

- **Source of truth**: `.agent/skills/` is the canonical library; tracking it enables history, review, and reproducible provisioning
- **Auditability**: Skill curation (add/edit/quarantine) is auditable via `git log`
- **Reproducibility**: Same commit → same active skill set
- **Already committed**: 12,000+ files already in the repository; switching to Model B would lose history

Model B would be better for very large libraries (>50K skills) or when skills are fetched from external registries, but neither applies here.

## Consequences

**Positive:**
- Git history for all skill changes
- Reproducible skill provisioning from any commit
- Pre-commit validation on skill changes
- Easy to review skill additions/modifications

**Negative:**
- Large repo size (12,000+ skill files)
- `.agent/.env` must be carefully gitignored to prevent secret leaks
- Clone/download time is larger than Model B

## Links

- .gitignore: root `.gitignore`
- BOOTSTRAPPER.md: §2 Directory contract, §7 Build-from-scratch checklist
- Agent runtime: `.agent/agent.md`
- Skill lifecycle: `docs/operations/skill-lifecycle.md`
