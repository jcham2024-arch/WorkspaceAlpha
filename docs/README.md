# Baselayer Workspace — Project Documentation

This directory holds the project's specifications, standards, and instructional documents. The baselayer indexes these files; it does not rewrite them.

## Project Overview

**Baselayer** is an offline, DAG-routed documentation workspace for agentic coding. Two surfaces compile from one canonical graph (`.context/graph.json`):

| Surface | Purpose | Audience |
|---------|---------|----------|
| Agent router (`AGENTS.md` + `.context/manifest.json`) | Token-efficient routing for AI agents | Models |
| Human wiki (`.wiki/index.html`) | Offline HTML wiki with full prose | People |

## Architecture

```
<root>/
├── AGENTS.md              # Agent entry point (read first)
├── BOOTSTRAPPER.md        # Whole-system build spec
├── Baselayer.md           # Bootstrap spec (input only)
├── llms.txt               # Machine-readable tree map
├── .context/
│   ├── graph.json         # Canonical DAG (source of truth)
│   ├── manifest.json      # Generated router (agent)
│   ├── index.md           # Plain-file fallback index
│   └── knowledge.db       # SQLite FTS for memory
├── docs/                  # Source documentation (indexed)
│   ├── specs/             # Technical specifications
│   ├── contracts/         # Decision records, interfaces
│   └── resources/         # Reference materials
├── .wiki/                 # Render pipeline (generated)
│   ├── seed.py            # docs → graph.json
│   ├── build.py           # graph → manifest + wiki
│   └── index.html         # Human wiki (never hand-edit)
├── .agent/                # Agent runtime (master)
│   ├── skills/            # 3,520 skills (master library)
│   ├── profiles/          # 9 specialized agent profiles
│   ├── tools/             # Pipeline, audit, knowledge, MCP
│   └── .env               # Secrets (gitignored)
├── .harness/              # Active skill set (provisioned)
│   └── skills/            # Current profile's skills
├── skills/index.json      # Slim skill router
├── memory/                # Persistent learnings
│   ├── learnings.md       # Session bullets
│   ├── JOURNAL.md         # Work summaries
│   ├── DECISIONS.md       # ADR-lite decisions
│   ├── ERRORS.md          # Diagnosed failures
│   └── LESSONS.md         # Emergent principles
├── 01-navigate/ … 04-verify/  # ICM stage folders
├── validate.py            # Step-6 validator (pre-commit)
└── .archive/              # Cleared after import (gitignored)
```

## Conventions

### Documentation

- **Source of truth**: `docs/` (Markdown) + `.context/graph.json` (DAG)
- **Never edit generated**: `.context/manifest.json`, `.wiki/index.html`, `skills/index.json`
- **Build pipeline**: `python3 .wiki/seed.py && python3 .wiki/build.py`
- **Validation**: `python3 validate.py` (also pre-commit hook)

### Skills

- **Master library**: `.agent/skills/` (3,520 skills, categorized)
- **Active set**: `.harness/skills/` (provisioned per profile)
- **Router**: `skills/index.json` (name + description + path only)
- **New skills**: Create in `.agent/skills/<name>/SKILL.md` → categorize → provision

### Agent Profiles

| Profile | Role | Skills |
|---------|------|--------|
| `conceptualizer` | Human-facing orchestrator | brainstorming, writing-plans, thinking-first-principles, thinking-margin-of-safety |
| `taskmaster` | Subagent-facing orchestrator | dispatching-parallel-agents, subagent-driven-development, executing-plans, ... |
| `coder` | Implementation | (provisioned per task) |
| `researcher` | Investigation | (provisioned per task) |
| `reviewer` | Code review | (provisioned per task) |
| `coding-manager` | Task breakdown | (provisioned per task) |
| `research-manager` | Research coordination | (provisioned per task) |
| `review-manager` | Review coordination | (provisioned per task) |
| `wiki-producer` | HTML wiki generation | (provisioned per task) |

### Communication Protocol

Two orchestration roles, zero cross-talk:

- **Conceptualizer** ↔ Human (all human messages)
- **Taskmaster** ↔ Subagents (all subagent messages)
- **Bridge**: 6 message types via file artifacts (see `.agent/profiles/protocol.md`)

## Getting Started

### Prerequisites

- Python 3.14+ (verified at build time)
- Zero external dependencies at build time
- AndroidHarness app (runtime environment)

### Initial Build

```bash
# Full pipeline
python3 .wiki/seed.py        # docs/ → .context/graph.json
python3 .wiki/build.py       # graph.json → manifest.json + .wiki/index.html
python3 .agent/tools/gen_skills_index.py  # master skills → skills/index.json
python3 validate.py          # Step-6 validation
```

### Development Workflow

1. **Edit** `docs/` or `.context/graph.json`
2. **Rebuild** `python3 .wiki/seed.py && python3 .wiki/build.py`
3. **Validate** `python3 validate.py`
4. **Commit** (pre-commit hook runs validation)

### Adding a Skill

```bash
# 1. Create skill in master library
mkdir -p .agent/skills/my-skill
# Write .agent/skills/my-skill/SKILL.md with frontmatter

# 2. Categorize (task type/subtype/level/OS)
# Edit .agent/skills/CATEGORIZATION.csv

# 3. Provision to active profile
# Edit .agent/profiles/<profile>.md skills list
python3 .harness/sync_active.py --profile <profile>

# 4. Regenerate router
python3 .agent/tools/gen_skills_index.py
```

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
