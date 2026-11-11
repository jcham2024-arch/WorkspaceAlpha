# BOOTSTRAPPER.md — Whole-System Build Spec

> **Purpose.** Baselayer.md built the first layer. This file is the
> up-to-date spec for the system as it actually grew: DAG baselayer +
> master skill library + profile-routed provisioning + wiki renderer.
> Follow Sections 2–7 in order to replicate it from nothing.
>
> **For re-use.** New skills and profiles are loaded into this
> system under the rules in §6 (schemas) and §7 (timing/lint rules).

---

## 1. Principles (the conventions that shaped every decision)

1. **DAG baselayer**: only `docs/` is indexed; `.context/graph.json`
   is the master knowledge file; manifest + wiki are generated.
   Routers stay under ~15% of context (current: ~1,400 tokens).
2. **Progressive disclosure** (Anthropic): frontmatter (~50–100
   tokens/skill) always loaded; body on trigger (< 500 lines);
   references on demand (one level deep). This is what makes a
   3,518-skill library affordable.
3. **Master vs. active**: `.agent/skills/` is the complete master
   library. `.harness/skills/` is only the *currently-used* set,
   provisioned per active profile. Skills never load wholesale.
4. **Single-owner skills**: each skill belongs to exactly one
   provisioning role in practice; producer/consumer pairs are
   documented, not silent overlaps.
5. **Task-driven profiles**: the orchestrator solves scope → plan
   → dispatch; managers break into minimal-context steps
   (smallest fastest cheapest model); implementers execute.
6. **Platform routing**: skills are OS-agnostic by default
   (`cross`); OS-specific skills carry variants per OS
   (android/windows/linux/mac), never 4× duplication.
7. **Human wiki `.wiki/`**: the only surface expanded prose may
   live on (audience: people, not models).

---

## 2. Directory contract

```
<root>/
├── BOOTSTRAPPER.md        ← this file (whole-system spec)
├── Baselayer.md           ← historic input spec (retired)
├── AGENTS.md              ← agent router (≤150 lines)
├── CLAUDE.md              ← shim: @AGENTS.md
├── llms.txt               ← machine-readable tree map
├── README.md              ← human docs
├── validate.py            ← Step-6 validator + token report
├── .gitignore             ← __pycache__, .archive/, .agent/.env, .agent/.harness/
├── .githooks/pre-commit   ← runs validate.py (chmod +x)
├── .context/              ← graph.json (source), manifest.json,
│                             index.md (plain fallback)
├── docs/                  ← only tree seed indexes (provenance)
├── docs/specs/            # Technical specifications
├── docs/contracts/        # Decision records, interfaces
├── docs/operations/       # Operational docs (secrets, quarantine, deprecation, etc.)
├── docs/adr/              # Architecture Decision Records
├── docs/skills/           # Skill documentation index & duplicate report
├── .wiki/                 ← render pipeline (seed/build/index.html)
│                             + agent.md (wiki production guide)
├── wiki/                  # Generated prompt wiki views (Unified Prompt Stack)
│   ├── conversation.md    # Delegation chain transcript
│   ├── prompt-chunk.md    # Per-turn prompt composition
│   ├── conceptual-expansion.md — Node selection rationale & assumptions
│   ├── index.md           # View index
│   └── views/generator.py # Wiki view generator
├── skills/index.json      ← slim skills router
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
├── .harness/skills/       ← currently-used skills (untracked)
├── .agent/                ← ALL agent resources (tracked; only .env, .harness/ gitignored)
│   ├── agent.md           ← runtime root guide
│   ├── skills/            ← master library (3,518 skills)
│   ├── profiles/          ← roles, protocol, template, evals
│   └── tools/             ← context core, provisioner, MCP, helpers
│       └── mcp/           ← server.py, mcp.json, README
├── 01-navigate/ … 04-verify/  ← ICM stage folders + output contracts
├── memory/                ← learnings + checkpoints
└── .archive/              ← cleared (gitignored)
```

Notable migrations (intentional, known to be missing files):
`builder/operator/planner` → `coder/reviewer/taskmaster-manage`;
older `orchestrator/REVIEW` docs → `protocol.md` + `eval-agents.md`;
`build.py`/`seed.py` → `.wiki/`; `.agent/mcp/` → `.agent/tools/mcp/`;
`resources/` → folded into `tools/README.md`.

---

## 3. Baselayer pipeline

```
python3 .wiki/seed.py    # docs/ → .context/graph.json (idempotent)
python3 .wiki/build.py   # graph.json → manifest.json + .wiki/index.html
python3 validate.py      # PASS/FAIL + token budget
```

Then regenerate small artifacts:
```
python3 .harness/gen_skills_index.py    # skills/index.json
python3 .harness/sync_active.py --profile conceptualizer
```

Then build the Unified Prompt Stack (WA-UNIFIED-002):
```
# Decision notes are hand-written ADRs; they do not compile through seed/build.
# The prompt graph is assembled from hand-written nodes + manifest refs.
python3 assembly/assembler.py    # two-zone prompt assembly (if run standalone)
python3 provenance/recorder.py   # per-turn provenance recording (called per turn)
python3 wiki/views/generator.py  # wiki views (called per delegation session)
```

Graphs stay section-addressed (`byte_range`), hashed (`sha256`),
acyclic. Edges are human-authored; generation never rewrites docs/.

---

## 4. Skill library & platform routing

Master: `.agent/skills/<name>/SKILL.md` (3,518 skills; 47 broken
sources quarantined in `_quarantine/`). Provenance: `INDEX.md`/`CSV`.
Categorization (`.agent/skills/CATEGORIZATION.md`/`.csv`):
task type × subtype × level (manager/worker) × os
(android|windows|linux|mac|cross), regenerated by
`.agent/tools/categorize.py` + `classify_os.py`.

Platform variants live with the skill: either an inline `os:`
frontmatter note + OS section, or `platforms/<os>.md` companions
(see `.agent/skills/PLATFORMS.md`).

**Skill authoring schema (binding, per Anthropic best practices):**

- Frontmatter: `name` (≤64 chars, folder name must match after
  NFKC), `description` (third person, ≤60 words, what + when).
- Body (SKILL.md): < 500 lines; workflow + checklists + pointers.
- References: one level deep; TOC when > 100 lines; format =
  Title → Scope → Load when → Contents → Checklist → Commands → Notes
  (see `.agent/skills/REFERENCE_FORMAT.md`).
- Scripts execute (solve, don't punt); MCP names fully qualified;
  forward slashes; no time-sensitive content inline.
- Wording: assume the agent is smart; cut hedging, narration,
  repeated paragraphs. Default + escape hatch, never a menu.
- Freedom matches fragility (text / templates / exact scripts).
- Loading new skills: add → audit → categorize → wrap refs →
  provision → eval (see §6 timing rules).

---

## 5. Profiles & model tiers

| Tier | Model class | Roles |
|---|---|---|
| Orchestrator | large context, high thinking | conceptualizer (human-facing) ↔ protocol ↔ taskmaster (subagent-facing) |
| Manager | large context, low thinking | research-manager, coding-manager, review-manager — break into steps, review, package |
| Specialist | mid | coder, researcher, reviewer |
| Implementer | low context, no thinking | per-step agents dispatched by managers |

Each profile's frontmatter now includes a `tier:` field (`core`/`curated`/`experimental`/`quarantine`) matching the skill tier system in `.agent/skills/TIERS.md`.

Build order within a run: scope (01) → plan DAG (02) → dispatch
packages via managers (03) → verify incl. final branch review (04).
Every stage writes a file (`targets.md`, `plan.md`, `changes.md`,
`verification.md`) and a checkpoint (`memory/checkpoints/`).

`.wiki/agent.md` + `.agent/profiles/wiki-producer.md` map the
machine system into human context; the wiki is the only
human-expanded prose surface.

**Machine registry & releases.** `.agent/agents.json` (registry,
regenerated by `registry.py`) is the factory's source of truth for
agents. AgentCards (A2A-style exports) regenerate from it via
`agent_cards.py`. Releases: `python3 .agent/tools/release.py`
(validate → audit → regenerate → snapshot into
`.agent/releases/<version>/` → tag the version). The `version`
lives in `.agent/models.json`.

---

## 6. Knowledge & skill lifecycle

**Knowledge system (persistent memory).**

| Store | Write when | Sync |
|---|---|---|
| `memory/JOURNAL.md` | work done (stage 04) | `knowledge.py add --kind work` |
| `memory/ERRORS.md` | failure diagnosed | `--kind error` |
| `memory/LESSONS.md` | principle emerges | `--kind lesson` |
| `memory/DECISIONS.md` | trade-off settled | `--kind decision` |
| `.context/knowledge.db` + `memory/index.json` | generated | `knowledge.py sync` (or per-add) |

Query without a DB: `knowledge.py search <words>`;
`last --kind work -n 5`. Query before planning (stage 01).
Index content is generated; Markdown files are the truth.

For **loading a new skill** (from any source):

1. **Audit** — frontmatter present? name == folder? description
   ≤ 60 words (third person, what + when)? body ≤ 500 lines?
   (see `.agent/tools/audit.py` for the compliance counts; fixes needed for non-conformers).
2. **Conforms?** → wrap reference files in the standard header
   (content verbatim); trim bodies to the checklist/workflow-only
   shape; reset name mismatches to the folder name (suffixed
   duplicates stay distinct by design).
3. **Categorize** — re-run `categorize.py` + `classify_os.py`;
   confirm task type/subtype + os tag + manager/worker level.
4. **Provision** — add to the master library index (INDEX.md/CSV,
   SKILL_AUTHORING.md pointers); the owning profile lists it in
   frontmatter; run `provision.py --profile <role>`; regenerate
   `skills/index.json`.
5. **Revise against schemas** — every new or edited master skill
   must pass the §4 schema and be re-audited. Broken sources
   (frontmatter absent / "404: Not Found") go to
   `.agent/skills/_quarantine/` with an IMPORT_REPORT note, never
   into the live library.

Timing rule: master edits happen only in `.agent/skills/` and a
profile edit in `.agent/profiles/` — never in `.agent/harness/` directly
(it is the provisioned snapshot, regenerated). Re-run `validate.py`
after any material change.

## Why Model A (tracked .agent/)

**Model A** tracks the full master skill library (3,520 skills) in git. Only `.agent/.env` (secrets) and `.agent/.harness/` (provisioned snapshot) are gitignored. This was chosen because:
- The master library is the source of truth; tracking it enables history, review, and reproducible provisioning
- 12K files already committed; switching to Model B would lose history and require bootstrap on every clone
- Skill curation (add/edit/quarantine) is auditable via git log

Model B (untracked, bootstrap-provisioned) would be better for massive libraries (>50K skills) or when skills are fetched from external registries.

---

## 7. Build-from-scratch checklist

1. **Dirs**: create the §2 tree; `git init`; write `.gitignore`
   (`__pycache__/`, `.archive/`, `.agent/.env`, `.agent/.harness/`); `git config
   core.hooksPath .githooks` and make `pre-commit` executable.
2. **Baselayer**: copy `seed.py`/`build.py` (exact spec copies)
   into `.wiki/` with `ROOT` = parent. Re-run §3.
3. **Master library**: import sources (INDEX.csv rows with
   source_bucket/dump_path), dedupe by name (master wins,
   collisions suffixed), quarantine broken, then §6.
4. **Profiles**: create the role set in §5 (9 files) + protocol.
   Provision defaults (orchestrator → conceptualizer state).
5. **MCP**: `.agent/tools/mcp/server.py` (stdlib JSON-RPC stdio,
   contract in README); per-profile allowlists in `mcp.json`;
   keys in `.agent/.env` from `.env.example`.
6. **Wiki**: `.wiki/agent.md` + `wiki-producer.md`,
   `.wiki/seed.py && .wiki/build.py`, validate, commit.
7. **Prompt stack**: Create `envelope/` (schemas + templates),
   `assembly/` (manifest_reader, slicer, budgeter, assembler,
   prefix/), `adapters/` (deepseek_v32, nemotron_35, dispatch),
   `schemas/` (prompt-graph, provenance-record), `provenance/`
   (recorder.py), `wiki/views/` (generator.py).
   Write `.context/prompt-graph.json` manually (hand-authored
   nodes + edges referencing manifest IDs). Run `validate.py`.
8. **Memory/learning**: `memory/learnings.md` seeded; stage
   folders (01–04) + `llms.txt` (root) wired into AGENTS.md.
