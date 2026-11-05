> **ChatWorkspace Build Task Overview** — Part 5 of 12
> Index: [`CONTEXT.md` §2.D](../../CONTEXT.md) · Prev: [`04-phase2-chat-creation-git.md`](04-phase2-chat-creation-git.md) · Next: [`06-phase4-mcp-tools.md`](06-phase4-mcp-tools.md)

## 6. Phase 3 — Chat Core (Weeks 5–6)

Goal: end-to-end conversation, persisted and resumable.

| ID | Task | WS | Depends | Acceptance |
|---|---|---|---|---|
| T-050 | Port D9 `core-engine` streaming port + adapter `OpenAiCompatibleLlmClient` | WS-P | T-012, T-021 | A20 passes (stream and non-stream produce identical final message) |
| T-051 | `LlmClient` interface finalization + provider schema mapper | WS-I | T-050 | Mapper test against donor output |
| T-052 | `ChatViewModel` turn loop: text + single tool cycle | WS-I | T-050, T-051, T-016 | Loop cap (8) and cancel tested |
| T-053 | Room `MessageEntity` + `ToolCallEntity` DAOs | WS-S | T-036 | Schema migration test passes |
| T-054 | `ChatRepository` contract: append, load, rehydrate | WS-I | T-053 | Contract tests green |
| T-055 | JSONL `history.jsonl` append on each turn | WS-N | T-017, T-037 | Append-only, survives restart |
| T-056 [P] | Chat screen: message list, streaming indicator, input bar | WS-N | T-014, T-054 | UI renders streamed tokens |
| T-057 [P] | Message bubble + role styling per D11 patterns | WS-N | T-056 | Material 3 roles verified against pinned BOM |
| T-058 | Error banner + retry | WS-N | T-052 | Failed turn recoverable |
| T-059 | Rehydration on restart | WS-I | T-054, T-055 | A9 passes |
| T-060 | Streaming cancel action | WS-N | T-052 | Cancel mid-stream leaves consistent history |
| T-061 | Integration test: full conversation persists and resumes | WS-H | T-059 | CI test |

### Phase 3 exit gate — M3

- A9 (restart restores chat list and per-chat history) passes.
- A20 (stream vs non-stream parity) passes.
- D9 checklist complete.

---
