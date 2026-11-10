# Decision: Q6 — Profile Provisioning: Dynamic vs Static Skill Lists

## Question

Should profile skill lists (in `.agent/profiles/*.md` frontmatter) be static (explicitly enumerated) or dynamic (computed from categorization tags at provision time)?

## Chosen Value

**Static skill lists in profile frontmatter, with a dynamic fallback for development.** Profiles declare their skills explicitly in frontmatter (`skills: [brainstorming, writing-plans, ...]`). The provisioning script (`.harness/sync_active.py`) reads this list and copies those skills from `.agent/skills/` to `.harness/skills/`. A `--dynamic` flag exists for development that auto-selects skills by category tags, but the committed profile frontmatter is the source of truth.

## Approver

conceptualizer (human-facing orchestrator), taskmaster (subagent-facing orchestrator) — 2026-11-10

## Evidence

- Current profiles: 9 profiles, each with 4–21 skills listed in frontmatter
- Master library: 3,520 skills in `.agent/skills/`
- Active set: 4 skills in `.harness/skills/` (conceptualizer profile)
- Provisioning script: `sync_active.py` reads frontmatter `skills:` array
- Skill index: `gen_skills_index.py` reads `.harness/skills/` contents
- Categorization CSV: 3,520 rows with task_type, task_subtype, level, os

## Rationale

Industry patterns for capability provisioning:

| Approach | Examples | Trade-off |
|----------|----------|-----------|
| **Static manifest** | Cargo.toml, package.json, go.mod, Python requirements.txt | Explicit, auditable, reproducible, reviewable |
| **Dynamic query** | npm workspaces, Bazel labels, Nix flakes | Flexible, but opaque; "what skills does this profile have?" requires running code |
| **Hybrid** | Poetry groups, Cargo features | Best of both: static manifest with optional dynamic composition |

**Static manifests win for auditability and reproducibility.** A human (or CI) can read `.agent/profiles/conceptualizer.md` and know exactly which skills are provisioned without executing code. This is critical for:
- Security review: "Does this profile have the `shell` skill?"
- Reproducibility: Same commit → same active skill set
- Debugging: "Why does this profile have skill X?" → check frontmatter, not query logic

The dynamic fallback (`--dynamic`) supports development exploration (e.g., "give me all `task_type=planning` skills") but does not replace the committed manifest.

## Constraint on Future Specs

- **Forbidden**: Removing static `skills:` frontmatter from profiles
- **Forbidden**: Making dynamic selection the default for committed profiles
- **Required**: `sync_active.py` must validate that every skill in frontmatter exists in `.agent/skills/`
- **Required**: `sync_active.py` must fail (not warn) on missing skills in static mode
- **Required**: Dynamic mode (`--dynamic`) must be opt-in and logged as non-authoritative

## Links

- Spec: `docs/specs/profile-provisioning-spec.md` (planned)
- Tracking: `open-questions.md` (Q6)
- Implementation: `.agent/profiles/*.md`, `.harness/sync_active.py`, `skills/index.json`

---

*Decision recorded 2026-11-10. Static frontmatter is source of truth; dynamic is dev-only exploration.*
