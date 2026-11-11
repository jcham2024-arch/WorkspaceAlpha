# Learnings

Persistent memory for this workspace. Append one line per session:
what was learned, in what context. Read this file at the start of
every session (see AGENTS.md §9).

## Entries

- 2026-11-07: Root BOOTSTRAPPER.md written (whole-system spec:
  directory contract, §3 pipeline, §4 skill authoring schema, §7
  build-from-scratch checklist). Skill lifecycle — new skills get
  audited, categorized, and provisioned via profiles.

- 2026-11-07: Baselayer bootstrapped; skills split into slim index
  (skills/index.json) because docs/skills catalog bloated manifest
  761 B → 148 KB. Layer-1 router must stay under ~15% of context.
- 2026-11-07: Three archive skills are broken at source (SKILL.md =
  "404: Not Found"): caveman, karpathy-coder, llm-cost-optimizer.
  Always verify disk state before trusting index counts.
- 2026-11-07: The .archive/ dump must never be git-added (686M).
  .agent/.env is gitignored; keys live there, not in chat or memory.

- 2026-11-10: Bootstrapped project content: audit-persistence-spec.md, open-questions.md with Q1-Q6, 3 decision notes (Q1: RPO=0 with synchronous=FULL; Q2: FULL p99=8.2ms on Android 17; Q3: .env v1, Keystore-wrapped DEK v2). Replaced placeholder docs/README.md. Full pipeline rebuild + validate.py passes. Pre-commit hook made executable.

- 2026-11-10: Closed Q4-Q6 with decision notes: Q4 (skill categorization schema stability — versioning, additive-only, v1.0.0), Q5 (wiki render pipeline — full rebuild default, incremental opt-in), Q6 (profile provisioning — static frontmatter source of truth, dynamic dev-only). open-questions.md updated with Decided status and history. Manifest 107 nodes, wiki 117KB, validate passes.

- 2026-11-10: Remediation plan executed (6 tasks): LICENSE (MIT) added + README.md updated; .gitignore reconciled (Model A tracked, .env+.harness ignored); tests/ added with 15 unittest tests (test_build.py, test_seed.py, test_provision.py); starter profile (12 skills) + docs/operations/starter-set.md created, README quickstart defaults to starter; docs/operations/secrets.md created + linked from agent.md/README.md; .agent/quarantine/registry.json (47 entries) + docs/operations/quarantine.md created, validate.py extended with quarantine check. validate.py passes (135 nodes, 10,363 router tokens).
