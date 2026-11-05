> **ChatWorkspace Build Task Overview** — Part 6 of 12
> Index: [`CONTEXT.md` §2.D](../../CONTEXT.md) · Prev: [`05-phase3-chat-core.md`](05-phase3-chat-core.md) · Next: [`07-phase5-prompt-docs.md`](07-phase5-prompt-docs.md)

## 7. Phase 4 — MCP & Tools (Weeks 7–8)

Goal: tools visible in UI, interlock enforced, branch guard proven.

| ID | Task | WS | Depends | Acceptance |
|---|---|---|---|---|
| T-070 | `McpToolRegistry`: local in-process server adapter | WS-N | T-018, T-051 | Local tool returns descriptor |
| T-071 | Remote MCP client (Streamable HTTP) | WS-N | T-070 | Connect to a test server; list tools |
| T-072 | Tool descriptor → provider schema mapper | WS-I | T-070, T-051 | Parity test against `ToolDefinitionMapper` |
| T-073 | Port D1 `SecurityInterlock` + `SecurityToolExecutorAdapter` | WS-P | T-003 (or fallback spec) | Fail-closed tests green |
| T-074 | Port D3 `ToolRiskRegistry` + register ChatWorkspace tools | WS-P | T-073 | Every tool has explicit level |
| T-075 | Branch guard in adapter (not donor) | WS-I | T-073, T-034 | A17 passes: wrong-branch commit rejected before network |
| T-076 | Port D2 `RiskLevel` + D4 audit chain (root → `filesDir/audit/`) | WS-P | T-073 | Chain tamper test passes; per-chat tag present |
| T-077 | Register GitHub MCP Server tools (`list_contents`, `get_file`, `create_or_update_file`, `create_branch`, `list_branches`) | WS-N | T-071, T-074 | Tools callable end to end |
| T-078 [P] | Tool-call chips in UI: pending/success/error, expandable args/result | WS-N | T-056, T-072 | States render correctly |
| T-079 [P] | Destructive-tool confirmation chip | WS-N | T-078, T-073 | L3/L4 tools require confirmation |
| T-080 | Per-tool timeout (60s) + surfaced error to agent | WS-I | T-070 | Timeout test |
| T-081 | Integration test: agent reads/writes files on its branch | WS-H | T-077, T-075 | CI test with real repo |

### Phase 4 exit gate — M4

- A4 (streaming + tool chips with final status) passes.
- A6 (writes land on branch only) passes.
- A17 (branch guard before network) passes.
- D1–D3 checklists complete; A13 satisfied for these parts.

---
