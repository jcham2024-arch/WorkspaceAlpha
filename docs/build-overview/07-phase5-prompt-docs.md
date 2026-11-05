> **ChatWorkspace Build Task Overview** — Part 7 of 12
> Index: [`CONTEXT.md` §2.D](../../CONTEXT.md) · Prev: [`06-phase4-mcp-tools.md`](06-phase4-mcp-tools.md) · Next: [`08-phase6-switch-polish.md`](08-phase6-switch-polish.md)

## 8. Phase 5 — System Prompt & Workspace Docs (Week 9)

Goal: progressive disclosure proven, agent reads only what it needs.

| ID | Task | WS | Depends | Acceptance |
|---|---|---|---|---|
| T-090 | `SystemPromptBuilder`: four-block assembly (scope §9) | WS-N | T-051, T-033 | Block order test |
| T-091 | Root `AGENTS.md` template (15–40 lines, index only) | WS-N | T-090 | Line count enforced by test |
| T-092 | Seed templates: `context/for-agent/*.md`, `skills/README.md`, `workspace/` | WS-N | T-040, T-091 | Seeded on chat creation; single initial commit |
| T-093 | Read-discipline prompt block | WS-N | T-090 | Static text verified in test fixture |
| T-094 | Inject root `AGENTS.md` from local mirror per turn | WS-I | T-090, T-033 | Injected verbatim; no tool call needed |
| T-095 | Prompt regression suite (fixtures) | WS-H | T-090–T-094 | Asserts tool-call patterns and file-read counts |
| T-096 | Verify agent does not grep for instruction files | WS-H | T-095 | A7 passes |
| T-097 | Verify agent lists directory before reading | WS-H | T-095 | A8 passes |

### Phase 5 exit gate — M5

- A7 (root `AGENTS.md` injected, not tool-read) passes.
- A8 (list-before-read, task-relevant only) passes.
- Prompt regression suite green in CI.

---
