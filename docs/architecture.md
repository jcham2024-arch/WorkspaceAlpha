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

See [harness-contract.md](docs/integration/harness-contract.md) for the integration contract.
