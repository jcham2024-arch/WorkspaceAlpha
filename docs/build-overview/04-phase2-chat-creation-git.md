> **ChatWorkspace Build Task Overview** — Part 4 of 12
> Index: [`CONTEXT.md` §2.D](../../CONTEXT.md) · Prev: [`03-phase1-providers.md`](03-phase1-providers.md) · Next: [`05-phase3-chat-core.md`](05-phase3-chat-core.md)

## 5. Phase 2 — Chat Creation & Git (Weeks 3–4)

Goal: per-chat branch from a user-selected base, on-device mirror, seed docs.

### Auth and API

| ID | Task | WS | Depends | Acceptance |
|---|---|---|---|---|
| T-030 | GitHub OAuth Device Flow + PAT fallback | WS-N | T-016 | Token stored encrypted via donor D8 |
| T-031 | `GitHubApi` Retrofit: branch list, ref creation, repo validation | WS-N | T-030 | Mocked server tests green |
| T-032 | Branch naming convention `agent/{shortId}` + collision handling | WS-N | T-031 | Test: two chats get distinct branches |

### Git client

| ID | Task | WS | Depends | Acceptance |
|---|---|---|---|---|
| T-033 | JGit wrapper: shallow clone of specific branch, checkout, status | WS-N | T-018 | Clone test repo into `chats/{id}/repo` under 30s |
| T-034 | Commit + push with branch guard | WS-N | T-033, T-013 | Push to wrong branch rejected |
| T-035 | Sync check on chat load (`git status` → diverge detection) | WS-N | T-033 | Test: simulated remote change surfaces "sync" action |

### Schema and creation flow

| ID | Task | WS | Depends | Acceptance |
|---|---|---|---|---|
| T-036 | Extend `ChatSession` with `providerId`, `modelId`, `repoOwner`, `repoName`, `baseBranch`, `agentBranch` | WS-S | T-023 | Migration test: existing row upgrades cleanly |
| T-037 | `CreateChatUseCase` — the deterministic 8-step sequence (supplement §8.2 of scope) | WS-N | T-031, T-033, T-036, T-024 | Integration test against test repo, all 8 steps succeed |
| T-038 [P] | Create Chat screen: form with repo fields + branch picker | WS-N | T-014, T-031 | Branch picker loads from API; validation inline |
| T-039 | Per-chat provider resolution adapter (`PerChatProviderResolver`) | WS-P | T-024, T-036 | A18 passes (switch affects only that chat) |
| T-040 | Seed docs commit — templates referenced from Phase 5 | WS-N | T-037 | Placeholder commit lands on `agent/{shortId}` |
| T-041 | Init failure handling: `init_failed` status + retry from Chat List | WS-N | T-037 | Test: clone failure recoverable |
| T-042 | `ChatListScreen`: session rows, FAB, empty state, retry banner | WS-N | T-014, T-036 | Renders provider chip, branch name, timestamp |
| T-043 | Secret redaction in `GitClient` and `GitHubApi` loggers | WS-H | T-030 | Test: tokens never in logs |
| T-044 | Donor checklist D7 adapter complete | WS-P | T-039 | Checklist items checked |

### Phase 2 exit gate — M2

- A2 (branch from any base) passes on a real test repo.
- A3 (distinct folder + JSONL per chat) passes.
- Failure paths recoverable without orphaned sessions.
- A10 (keys/tokens never in workspace/metadata/logs) passes for Git paths.

---
