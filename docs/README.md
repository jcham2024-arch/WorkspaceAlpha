# Baselayer Workspace — Project Documentation

This directory holds the project's specifications, standards, and instructional documents. The baselayer indexes these files; it does not rewrite them.

## Project Overview

**Baselayer** is an offline, DAG-routed documentation workspace for agentic coding. Two surfaces compile from one canonical graph (`.context/graph.json`):

| Surface | Purpose | Audience |
|---------|---------|----------|
| Agent router (`AGENTS.md` + `.context/manifest.json`) | Token-efficient routing for AI agents | Models |
| Human wiki (`.wiki/index.html`) | Offline HTML wiki with full prose | People |

## Architecture

The workspace consists of the baselayer (docs → graph → manifest + wiki) plus the Unified Prompt Stack (prompt DAG, compiler, adapters, provenance, wiki views) layered on top.

```
<root>/
├── AGENTS.md              # Agent entry point (read first)
├── BOOTSTRAPPER.md        # Whole-system build spec
├── Baselayer.md           # Bootstrap spec (input only)
├── llms.txt               # Machine-readable tree map
├── README.md              # Project documentation (this file)
├── LICENSE                # MIT License
├── THIRD_PARTY_NOTICES.md # Third-party skill licenses
├── open-questions.md      # Architectural question tracker
├── .context/
│   ├── graph.json         # Canonical DAG (source of truth)
│   ├── manifest.json      # Generated router (agent)
│   ├── index.md           # Plain-file fallback index
│   ├── prompt-graph.json  # Prompt DAG (Unified Prompt Stack)
│   └── knowledge.db       # SQLite FTS for memory
├── docs/                  # Source documentation (indexed)
│   ├── specs/             # Technical specifications
│   ├── contracts/         # Decision records, interfaces
│   ├── operations/        | Operational docs (secrets, quarantine, deprecation, etc.)
│   ├── adr/               # Architecture Decision Records
│   ├── skills/            # Skill documentation index & duplicate report
│   └── architecture.md    # Architecture diagram (ASCII)
├── .wiki/                 # Render pipeline (generated)
│   ├── seed.py            # docs → graph.json
│   ├── build.py           # graph → manifest + wiki
│   └── index.html         # Human wiki (never hand-edit)
├── wiki/                  # Generated prompt wiki views (Unified Prompt Stack)
│   ├── conversation.md    # Delegation chain transcript
│   ├── prompt-chunk.md    # Per-turn prompt composition
│   ├── conceptual-expansion.md — Node selection rationale & assumptions
│   ├── index.md           # View index
│   └── views/generator.py # Wiki view generator
├── .agent/                # Agent runtime (master)
│   ├── skills/            # 3,520 skills (master library)
│   ├── profiles/          # 9 specialized agent profiles (with tier field)
│   ├── tools/             # Pipeline, audit, knowledge, MCP
│   └── .env               # Keys (gitignored)
├── .harness/skills/       # Currently-used set — provisioned per active profile
├── adapters/              # Model adapters (Unified Prompt Stack)
│   ├── deepseek_v32.py    # DeepSeek V3.2 (thinking mode, token floors)
│   ├── nemotron_35.py     # Nemotron 3.5 (reasoning_effort mapping)
│   └── dispatch.py        # Adapter selection by target_tier
├── assembly/              # DAG compiler (Unified Prompt Stack)
│   ├── manifest_reader.py # Manifest loading & scope resolution
│   ├── slicer.py          # Byte-range extraction with sha256 verification
│   ├── budgeter.py        # Per-tier token ceiling enforcement
│   └── assembler.py       # Plan→Bind→Optimize→Execute→Feedback pipeline
├── assembly/prefix/       # Frozen prompt prefixes (byte-identical, cache-keyed)
│   ├── orchestrator.md    # Conceptualizer prefix
│   ├── manager.md         # Taskmaster prefix
│   └── production.md      # Production worker prefix
├── envelope/              # Delegation envelopes (Unified Prompt Stack)
│   ├── handoff-envelope.schema.json   # JSON Schema for delegation envelope
│   ├── return-envelope.schema.json    # JSON Schema for return envelope
│   ├── mission-envelope.yaml          # MISSION delegation template
│   └── execution-envelope.yaml        # EXECUTION delegation template
├── schemas/               # JSON Schemas (Unified Prompt Stack)
│   ├── prompt-graph.schema.json   # Prompt DAG node/edge schema
│   └── provenance-record.schema.json  # Per-turn provenance record schema
├── provenance/            # Per-turn provenance records (Unified Prompt Stack)
│   ├── recorder.py        # Record & summarize turns
│   └── turns.jsonl        # JSONL log of all turns
├── skills/                # Skill documentation index
│   ├── SKILL_INDEX.md     # Searchable reference index (3,518 skills)
│   └── DUPLICATE_REPORT.md # 237 potential duplicate skill groups
├── tests/                 # Test suite (59 tests)
│   ├── test_build.py
│   ├── test_seed.py
│   ├── test_provision.py
│   ├── test_golden.py
│   ├── test_mcp.py
│   ├── test_envelope.py
│   ├── test_assembler.py
│   ├── test_adapter.py
│   └── test_cache.py
├── tools/                 # Development tools
│   ├── normalize_skills.py    # Promote body fields to frontmatter
│   ├── cleanup_skills.py      # Fix double separators, orphaned lists
│   ├── fix_double_separator.py
│   ├── fix_yaml_lists.py
│   ├── remove_empty_fields.py
│   ├── fix_quoting.py
│   ├── generate_skill_index.py # Generate SKILL_INDEX.md
│   ├── find_duplicate_skills.py # Find duplicate/overlapping skills
│   ├── backfill_tiers.py      # Backfill tier field
│   ├── backfill_last_reviewed.py # Backfill last_reviewed field
│   ├── dedup.py               # Find duplicate skills
│   ├── stale.py               # List unreviewed skills
│   ├── context_budget.py      # Context budget tracking
│   ├── scan_secrets.py        # Secret scanning
│   ├── context_budget.py      # Context budget
│   ├── lint_dag.py            # DAG linting
│   └── ...                    # Other utility scripts
├── .agent/                # Agent runtime (master)
│   ├── skills/            # 3,520 skills (master library)
│   ├── profiles/          # 9 specialized agent profiles (with tier field)
│   ├── tools/             # Pipeline, audit, knowledge, MCP
│   └── .env               # Keys (gitignored)
├── .harness/skills/       # Currently-used set — provisioned per active profile
├── .wiki/                 # Render pipeline (generated)
│   ├── seed.py            # docs → graph.json
│   ├── build.py           # graph → manifest + wiki
│   └── index.html         # Human wiki (never hand-edit)
├── .archive/              # Cleared after full import (gitignored)
├── 01-navigate/ … 04-verify/ | ICM stage folders (+ output contracts)
├── validate.py · .githooks/ | Step-6 check + pre-commit hook
└── memory/learnings.md    | Persistent learnings (append post-session)
```

## Conventions

- `docs/` is read-only to the build; `graph.json` is the only writable
  knowledge file — edit docs or graph, then rebuild.
- Skills are one folder per name, `SKILL.md` frontmatter authoritative;
  descriptions are load-bearing (progressive disclosure Layer 1).
- Secrets live only in `.agent/.env` (gitignored); `.env.example` is the
  committed template.
- The master library (3,520 skills) is categorized in
  `.agent/skills/CATEGORIZATION.md`; the 47 broken sources are
  quarantined in IMPORT_REPORT.md; bulk-installing is prohibited.
- Secrets: `docs/operations/secrets.md` — key storage, rotation, leak response.

## Key Files Reference

| File | Purpose | Edit? |
|------|---------|-------|
| `AGENTS.md` | Agent router (read first) | Yes (rarely) |
| `BOOTSTRAPPER.md` | Build spec, conventions, lifecycle | Yes |
| `Baselayer.md` | Bootstrap spec (input only) | No (historical) |
| `docs/specs/*.md` | Technical specifications | Yes |
| `docs/contracts/decisions/*.md` | Decision records | Yes (append-only) |
| `open-questions.md` | Architectural question tracker | Yes |
| `.agent/profiles/*.md` | Agent role definitions | Yes |
| `.agent/profiles/protocol.md` | Inter-role communication | Yes |
| `.harness/sync_active.py` | Skill provisioning script | Yes |
| `.wiki/seed.py`, `build.py` | Render pipeline | Yes (carefully) |
| `validate.py` | Step-6 validator | Yes |
| `.agent/tools/knowledge.py` | Memory system | Yes |
| `.agent/tools/mcp/server.py` | MCP JSON-RPC server | Yes |

## Validation Rules (validate.py)

1. **Graph integrity**: All node `byte_range` valid, `sha256` matches content
2. **Manifest consistency**: Every node in manifest exists in graph, edges valid
3. **Router budget**: `manifest.json` < 15% of context window (~1,400 tokens)
4. **Skill index**: `skills/index.json` matches `.harness/skills/` contents
5. **Wiki generation**: `.wiki/index.html` builds without error
6. **No generated files modified**: Manifest, wiki, index.json not hand-edited

## Memory System

Persistent knowledge (Markdown truth, generated indexes):

| File | Kind | Written |
|------|------|---------|
| `memory/JOURNAL.md` | Work summaries | Stage 04 |
| `memory/ERRORS.md` | Diagnosed failures | On failure |
| `memory/LESSONS.md` | Emergent principles | When discovered |
| `memory/DECISIONS.md` | Trade-off settlements | When decided |
| `memory/learnings.md` | Session bullets | Session end |

**Procedure**: `python3 .agent/tools/knowledge.py add --kind {work,error,lesson,decision} --title "..."`

## License

Proprietary — internal tooling for AndroidHarness.

---

*This documentation is indexed by the baselayer. Edit source files in `docs/`, then rebuild.*
