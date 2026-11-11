# WorkspaceAlpha Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           WORKSPACEALPHA                                 │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   HUMAN      │      │    AGENT     │      │   SUBCON     │
│  (reads      │      │  (reads      │      │   AGENT      │
│   .wiki/)    │      │   AGENTS.md  │      │  (tasks via  │
│              │      │              │      │  protocol)   │
└──────┬───────┘      └──────┬───────┘      └──────┬───────┘
       │                     │                     │
       ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  .wiki/      │      │  AGENTS.md   │      │  Protocol:   │
│  index.html  │      │  (≤150 lines)│      │  SCOPE-LOCK  │
│  (human wiki)│      │  (agent router)│     │  PLAN-READY  │
│              │      │              │      │  APPROVAL    │
└──────┬───────┘      └──────┬───────┘      │  STATUS      │
       │                     │             │  ESCALATION    │
       │                     │             │  FINAL-REPORT  │
       ▼                     ▼             └──────┬─────────┘
┌──────────────────────────────────────────────────────────────────────┐
│                    .context/graph.json  (canonical DAG)              │
│                     nodes, edges, byte ranges, SHA-256               │
└──────────────────────────────────────────────────────────────────────┘
                           ▲                   ▲
                           │                   │
                    seed.py             build.py
                    (docs/ →            (graph →
                     graph.json)        manifest +
                                       wiki)
                           │                   │
                           ▼                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                          docs/                                        │
│   (source documentation, read-only to build)                          │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                       .agent/  (master skill library)                │
│                                                                       │
│  skills/          profiles/       tools/                             │
│  3,520 skills   conceptualizer   seed/build/validate                 │
│  tiered (core/  taskmaster       context.py                           │
│   curated/     coder             mcp/server.py                       │
│   experimental  researcher       knowledge.py                        │
│   quarantine)   reviewer         sync_active.py                      │
│              *-manager           release.py                          │
└──────────────────────────────────────────────────────────────────────┘
                           ▲
                           │ provision
                           │ sync_active.py
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    .harness/skills/  (active set)                    │
│                     (provisioned per profile)                        │
└──────────────────────────────────────────────────────────────────────┘

Data flow:
  docs/ ──seed.py──> graph.json ──build.py──> manifest.json + wiki
  .agent/ ──sync──> .harness/skills/ ──agent uses──> tasks
  AGENTS.md ──────────────────────────────────────> routes to skills
```

## Unified Prompt Stack (WA-UNIFIED-002)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      UNIFIED PROMPT STACK                                │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  DELEGATION  │      │   DAG        │      │   MODEL      │
│  ENVELOPE    │      │  COMPILER    │      │  ADAPTER     │
│  (mission)   │      │  (Plan→Bind  │      │  (DeepSeek   │
│  → manager   │      │   →Optimize  │      │   3.2 /      │
│  → production│      │   →Execute   │      │   Nemotron   │
└──────┬───────┘      │   →Feedback  │      │   3.5)       │
       │               └──────┬───────┘      └──────┬───────┘
       │                     │                     │
       ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   FROZEN     │      │   VARIABLE   │      │   PROVENANCE │
│   PREFIX     │      │   SUFFIX     │      │   RECORDER   │
│  (SystemPrompt│      │  (task envelope│      │  (turn records│
│   node)      │      │   + context   │      │   + summaries)│
│  byte-identical│      │   slices)    │      │              │
│  cache-keyed   │      │              │      │              │
└──────┬───────┘      └──────┬───────┘      └──────┬───────┘
       │                     │                     │
       ▼                     ▼                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    .context/prompt-graph.json                          │
│              Six node types, five edge types                           │
│  SystemPrompt → Skill → Envelope → ContextSlice → Adapter →           │
│  OutputContract                                                    │
│  requires → triggers → routes_to → adapts → provenance_of            │
└──────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                          WIKI VIEWS                                     │
│  conversation.md  → Delegation chain transcript with evidence links   │
│  prompt-chunk.md   → Per-turn prompt composition (prefix/suffix)     │
│  conceptual-expansion.md → Why each node was selected & assumptions  │
└──────────────────────────────────────────────────────────────────────┘
```

### Prompt DAG Node Types

| Node Type | Represents | Content Ref |
|-----------|-----------|-------------|
| `SystemPrompt` | Frozen prefix for an agent role | `assembly/prefix/*.md` |
| `Skill` | A skill `.md` file with frontmatter triggers | `.agent/skills/<name>/SKILL.md` |
| `Envelope` | Delegation contract (frontmatter + body template) | `envelope/*-envelope.yaml` |
| `ContextSlice` | A byte-range reference into the manifest | `.context/manifest.json` nodes |
| `Adapter` | Model-specific dispatch config | `adapters/*.py` |
| `OutputContract` | JSON Schema or diff contract for return | `envelope/*-schema.json` |

### Edge Types

| Edge Type | Semantics | Example |
|-----------|-----------|---------|
| `requires` | Hard dependency; target must be assembled before source | Envelope requires OutputContract |
| `triggers` | Conditional inclusion; target included only when frontmatter condition matches | Skill triggered by `task_type=debugging` |
| `routes_to` | Routing edge; source delegation type selects target node | `MISSION` routes to manager envelope |
| `adapts` | Model binding; target adapter configures source for a specific model | Envelope adapts to DeepSeek 3.2 |
| `provenance_of` | Traceability; target is the evidence source for source's output | Return envelope's results point to context slices |

### DAG Compiler Stages

1. **Scope resolution** — Incoming delegation envelope carries `task_type`, `domain`, `allowed_targets`, `target_tier`. These are root selectors.
2. **Graph traversal** — Starting from the selected `Envelope` node, walk `requires`, `triggers`, and `routes_to` edges. Select only nodes whose conditions match scope.
3. **Budget-aware ordering** — Topologically sort selected nodes, then assign token budgets per layer. If total exceeds per-tier ceiling, prune nodes by edge distance from root (farthest `triggers` nodes dropped first). Never silently truncate; return `BLOCKED` with excluded node IDs.
4. **Cache-keyed rendering** — Render frozen prefix from `SystemPrompt` node + `Adapter`. Render variable suffix from remaining nodes in dependency order. Append suffix after prefix.

### Per-Tier Token Ceilings

| Tier | Suffix Ceiling | Max Tokens Floor |
|------|---------------|-----------------|
| thinking (manager) | 1,800 | 8,192 |
| low_thinking / non_thinking (production) | 1,500 | 1,024 |

### Model Adapters

| Adapter | Model | Thinking Mode | Max Tokens Floor |
|---------|-------|---------------|-----------------|
| DeepSeek V3.2 | `deepseek-v3.2-thinking` | `enabled` (manager) / `disabled` (production) | 8,192 / 1,024 |
| Nemotron 3.5 | `nvidia/nemotron-3.5-super-vl-120b-a12b` | `enable_thinking: true` (+ `medium_effort` for production) | 16,384 |

### Wiki Views

| View | Path | Purpose | Data Source |
|------|------|---------|-------------|
| Conversation | `wiki/conversation.md` | Delegation chain transcript with evidence links | Provenance log + return envelopes |
| Prompt Chunk | `wiki/prompt-chunk.md` | Per-turn prompt composition (frozen prefix, skills, context slices, output contract) | DAG compiler assembly record |
| Conceptual Expansion | `wiki/conceptual-expansion.md` | Why each node was selected, what was excluded, assumptions | Compiler selection log + adapter params + return envelope |

See [harness-contract.md](docs/integration/harness-contract.md) for the integration contract.
