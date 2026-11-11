# agent.md — Agent Runtime for This Workspace

This folder is the agent runtime for the baselayer workspace at the
root. It holds ALL agent resources (master skill library, tools,
MCP server, specialized profiles) in **three subfolders**:

```
.agent/
├── agent.md           ← this file (read first)
├── .env               ← keys (gitignored; never commit)
├── .env.example       ← template
├── skills/            ← master skill library (3,520 skills)
├── profiles/          ← specialized agents (roles, protocol, evals)
└── tools/             ← scripts: context core, provisioner, mcp/
```

## Environment facts

- Runs inside **AndroidHarness** (Android 17, API 37, arm64-v8a).
  Normal access = app UID with a Termux-derived Linux userspace
  (Python 3.14, bash). Shizuku/root are usually unavailable.
- Shell work is normal access only. No sudo/su, no Termux-app paths.
- Python 3 stdlib only at runtime (no pip installs without approval).
- Workspace root = this project's parent. All paths relative to it.

## Roles (gitignored; the profiles define the work)

- `profiles/conceptualizer.md` — human-facing agent (owns ALL human
  communication; locks scope; presents results).
- `profiles/taskmaster.md` — subagent-facing agent (planning ~
  supervision ~ integration ~ synthesis; never talks to the human).
- `profiles/protocol.md` — the contract between them (messaging
  types SCOPE-LOCK / PLAN-READY / APPROVAL / STATUS / ESCALATION /
  FINAL-REPORT).
- Profiles: `coder`, `researcher`, `reviewer` (specialists) and
  `research-manager`, `coding-manager`, `review-manager` (dispatch
  minimal-context implementer steps).
- `profiles/TEMPLATE.md` — generate a per-task profile; smallest
  viable model tier, parallel where independent.

## Daily commands (from workspace root)

```bash
python3 .wiki/seed.py && python3 .wiki/build.py   # baselayer rebuild
python3 validate.py                        # Step-6 check
python3 .harness/sync_active.py --profile <name>   # activate a profile
python3 .agent/tools/gen_skills_index.py        # refresh slim index after skill changes
python3 .agent/tools/context.py search <query>        # manifest search
python3 .agent/tools/run.py build            # seed+build+validate one command
python3 .agent/tools/registry.py && python3 .agent/tools/agent_cards.py
python3 .agent/tools/release.py --check      # release dry-run
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python3 .agent/tools/mcp/server.py
```

## Rules that never bend

1. `.agent/` never writes `.context/manifest.json` or `wiki/`.
2. Seeds and scripts take those files read-only; `.context/graph.json`
   is the master knowledge file (docs/ read-only to the build).
3. `.env` keys stay local; the tracked docs point at it but never
   inline secrets. Rotate any leaked key.
4. Profiles provision only master skills declared in frontmatter;
   never hand-copy a dump skill. Risk-flagged (offensive/critical)
   skills require an explicit profile decision.
5. At stage 04, log work/errors/lessons/decisions:
   `python3 .agent/tools/knowledge.py add --kind {work,error,lesson,decision}`
   (appends to memory/ + syncs). Before planning (stage 01),
   search it first: `knowledge.py search <words>`.

## Where to look next

- Skills: `.agent/skills/` — `CATEGORIZATION.md` (task type/subtype/
  level/os), `SKILL_AUTHORING.md` (writing rules), `PLATFORMS.md`
  (OS variants options).
- Profiles routing: `.agent/profiles/README.md`.
- Baselayer: root `AGENTS.md` (§1–§10) + `docs/resources/README.md`.
