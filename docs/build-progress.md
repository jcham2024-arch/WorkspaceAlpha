# ChatWorkspace Build Progress

Companion tracker for the master task index (`docs/build-overview/`, indexed in `CONTEXT.md` §2.D).

Seeded from the task tables. The index states "124" tasks but only **98** are defined; the gap is noted
in the overview (Phase 0 range `T-001 … T-018` lacks `T-008`, `T-009`, `T-019`). Additional tasks are
appended to the end of their phase section as they are discovered.

## How to update

- Status values: `not-started`, `in-progress`, `blocked`, `review`, `done`.
- Update on every state change. A milestone gate cannot pass with any task in that phase below `done`.
- Owner: Engineer A / Engineer B per the parallelization guide (`docs/build-overview/10-dependencies-parallelization.md`), or `Shared`.
- Dates use `YYYY-MM-DD`, or `—` when not started/finished.
- Keep the row's Notes cell short (dependencies, blockers); detail lives in the phase overview file.

## Phase 0 — Foundation (gate M0)

| ID | Task | WS | Status | Owner | Started | Done | Notes |
|----|------|----|--------|-------|---------|------|-------|
| T-001 | Commit repair kit MD files to Harness | WS-R | not-started | A | — | — | Depends: — |
| T-002 | Create repair/compile branch; run baseline build | WS-R | not-started | A | — | — | Depends: T-001; expect 286 |
| T-003 | Wave 1: foundational DI (A1-A4) | WS-R | not-started | A | — | — | Depends: T-002; target <=271 |
| T-004 | Wave 2: Compose UI (B1-B4) | WS-R | not-started | A | — | — | Depends: T-003; target <=171 |
| T-005 | Wave 3: type and syntax (C1-C6) | WS-R | not-started | A | — | — | Depends: T-004; target =0 |
| T-006 | Wave 4: donor tests green | WS-R | not-started | A | — | — | Depends: T-005 |
| T-007 | Write docs/repair-report.md; PR for review | WS-R | not-started | A | — | — | Depends: T-006 |
| T-010 | Create 8-module Gradle project with version catalog | WS-S | not-started | B | — | — | Depends: — |
| T-011 | Enforce module dependency rules via api/implementation | WS-S | not-started | B | — | — | Depends: T-010 |
| T-012 | Scaffold :security, :workspace, :core-engine skeletons | WS-S | not-started | B | — | — | Depends: T-010 |
| T-013 | Scaffold :app, :data, :git, :mcp, :prompt skeletons | WS-S | not-started | B | — | — | Depends: T-010 |
| T-014 | Compose Navigation graph with 4 destinations (stubs) | WS-S | not-started | B | — | — | Depends: T-013 |
| T-015 | Room AppDatabase with empty schema + migration harness | WS-S | not-started | B | — | — | Depends: T-013 |
| T-016 | Manual DI container (match donor style; no Hilt/Koin) | WS-S | not-started | B | — | — | Depends: T-015 |
| T-017 | WorkspaceManager scaffold; per-chat root sandboxing | WS-S | not-started | B | — | — | Depends: T-012 |
| T-018 | Dependency spike: JGit + MCP Kotlin SDK on Android | WS-S | not-started | B | — | — | Depends: —; SPIKE.md output |

## Phase 1 — Providers (gate M1)

| ID | Task | WS | Status | Owner | Started | Done | Notes |
|----|------|----|--------|-------|---------|------|-------|
| T-020 | Port D6 ProviderPresets (7 presets) | WS-P | not-started | A | — | — | Depends: T-012 |
| T-021 | Port D7 ProviderConfigurationManager (DataStore) | WS-P | not-started | A | — | — | Depends: T-020 |
| T-022 | Port D8 AndroidKeyStoreManager (AES-256/GCM) | WS-P | not-started | A | — | — | Depends: T-012 |
| T-023 | Define ProviderConfig Room entity + DAO | WS-S | not-started | B | — | — | Depends: T-015 |
| T-024 | ProviderRepository in :data | WS-I | not-started | B | — | — | Depends: T-021, T-023 |
| T-025 | Providers list screen | WS-N | not-started | B | — | — | Depends: T-014, T-024 |
| T-026 | Add/Edit provider screen | WS-N | not-started | B | — | — | Depends: T-024 |
| T-027 | Delete provider guard (blocked if referenced) | WS-N | not-started | B | — | — | Depends: T-024; A12 |
| T-028 | Donor checklist D6-D8 complete | WS-P | not-started | A | — | — | Depends: T-020-T-022 |
| T-029 | Integration test: full provider lifecycle | WS-H | not-started | Shared | — | — | Depends: T-025-T-027 |

## Phase 2 — Chat Creation & Git (gate M2)

| ID | Task | WS | Status | Owner | Started | Done | Notes |
|----|------|----|--------|-------|---------|------|-------|
| T-030 | GitHub OAuth Device Flow + PAT fallback | WS-N | not-started | B | — | — | Depends: T-016 |
| T-031 | GitHubApi Retrofit: branches, refs, repo validation | WS-N | not-started | B | — | — | Depends: T-030 |
| T-032 | Branch naming agent/{shortId} + collision handling | WS-N | not-started | B | — | — | Depends: T-031 |
| T-033 | JGit wrapper: shallow clone, checkout, status | WS-N | not-started | B | — | — | Depends: T-018 |
| T-034 | Commit + push with branch guard | WS-N | not-started | B | — | — | Depends: T-033, T-013 |
| T-035 | Sync check on chat load (diverge detection) | WS-N | not-started | B | — | — | Depends: T-033 |
| T-036 | Extend ChatSession with provider/repo/branch fields | WS-S | not-started | B | — | — | Depends: T-023 |
| T-037 | CreateChatUseCase: deterministic 8-step sequence | WS-N | not-started | B | — | — | Depends: T-031, T-033, T-036, T-024 |
| T-038 | Create Chat screen: repo fields + branch picker | WS-N | not-started | B | — | — | Depends: T-014, T-031 |
| T-039 | PerChatProviderResolver adapter | WS-P | not-started | A | — | — | Depends: T-024, T-036; A18 |
| T-040 | Seed docs commit | WS-N | not-started | B | — | — | Depends: T-037 |
| T-041 | Init failure handling: init_failed + retry | WS-N | not-started | B | — | — | Depends: T-037 |
| T-042 | ChatListScreen: rows, FAB, empty state, retry banner | WS-N | not-started | B | — | — | Depends: T-014, T-036 |
| T-043 | Secret redaction in GitClient and GitHubApi loggers | WS-H | not-started | Shared | — | — | Depends: T-030 |
| T-044 | Donor checklist D7 adapter complete | WS-P | not-started | A | — | — | Depends: T-039 |

## Phase 3 — Chat Core (gate M3)

| ID | Task | WS | Status | Owner | Started | Done | Notes |
|----|------|----|--------|-------|---------|------|-------|
| T-050 | Port D9 core-engine streaming port + OpenAiCompatibleLlmClient | WS-P | not-started | A | — | — | Depends: T-012, T-021; A20 |
| T-051 | LlmClient interface + provider schema mapper | WS-I | not-started | Shared | — | — | Depends: T-050 |
| T-052 | ChatViewModel turn loop: text + single tool cycle | WS-I | not-started | B | — | — | Depends: T-050, T-051, T-016 |
| T-053 | Room MessageEntity + ToolCallEntity DAOs | WS-S | not-started | B | — | — | Depends: T-036 |
| T-054 | ChatRepository contract: append, load, rehydrate | WS-I | not-started | B | — | — | Depends: T-053 |
| T-055 | JSONL history.jsonl append per turn | WS-N | not-started | B | — | — | Depends: T-017, T-037 |
| T-056 | Chat screen: message list, streaming indicator, input bar | WS-N | not-started | B | — | — | Depends: T-014, T-054 |
| T-057 | Message bubble + role styling | WS-N | not-started | B | — | — | Depends: T-056 |
| T-058 | Error banner + retry | WS-N | not-started | B | — | — | Depends: T-052 |
| T-059 | Rehydration on restart | WS-I | not-started | B | — | — | Depends: T-054, T-055; A9 |
| T-060 | Streaming cancel action | WS-N | not-started | B | — | — | Depends: T-052 |
| T-061 | Integration test: conversation persists and resumes | WS-H | not-started | Shared | — | — | Depends: T-059 |

## Phase 4 — MCP & Tools (gate M4)

| ID | Task | WS | Status | Owner | Started | Done | Notes |
|----|------|----|--------|-------|---------|------|-------|
| T-070 | McpToolRegistry: local in-process server adapter | WS-N | not-started | B | — | — | Depends: T-018, T-051 |
| T-071 | Remote MCP client (Streamable HTTP) | WS-N | not-started | B | — | — | Depends: T-070 |
| T-072 | Tool descriptor to provider schema mapper | WS-I | not-started | B | — | — | Depends: T-070, T-051 |
| T-073 | Port D1 SecurityInterlock + SecurityToolExecutorAdapter | WS-P | not-started | A | — | — | Depends: T-003 |
| T-074 | Port D3 ToolRiskRegistry + register CW tools | WS-P | not-started | A | — | — | Depends: T-073 |
| T-075 | Branch guard in adapter (not donor) | WS-I | not-started | A | — | — | Depends: T-073, T-034; A17 |
| T-076 | Port D2 RiskLevel + D4 audit chain | WS-P | not-started | A | — | — | Depends: T-073 |
| T-077 | Register GitHub MCP Server tools | WS-N | not-started | B | — | — | Depends: T-071, T-074 |
| T-078 | Tool-call chips in UI | WS-N | not-started | B | — | — | Depends: T-056, T-072 |
| T-079 | Destructive-tool confirmation chip | WS-N | not-started | B | — | — | Depends: T-078, T-073 |
| T-080 | Per-tool timeout (60s) + surfaced error | WS-I | not-started | Shared | — | — | Depends: T-070 |
| T-081 | Integration test: agent reads/writes on its branch | WS-H | not-started | Shared | — | — | Depends: T-077, T-075 |

## Phase 5 — System Prompt & Workspace Docs (gate M5)

| ID | Task | WS | Status | Owner | Started | Done | Notes |
|----|------|----|--------|-------|---------|------|-------|
| T-090 | SystemPromptBuilder: four-block assembly | WS-N | not-started | B | — | — | Depends: T-051, T-033 |
| T-091 | Root AGENTS.md template (15-40 lines, index only) | WS-N | not-started | B | — | — | Depends: T-090 |
| T-092 | Seed templates: context docs, skills/README.md, workspace/ | WS-N | not-started | B | — | — | Depends: T-040, T-091 |
| T-093 | Read-discipline prompt block | WS-N | not-started | B | — | — | Depends: T-090 |
| T-094 | Inject root AGENTS.md from local mirror per turn | WS-I | not-started | B | — | — | Depends: T-090, T-033 |
| T-095 | Prompt regression suite (fixtures) | WS-H | not-started | Shared | — | — | Depends: T-090-T-094 |
| T-096 | Verify agent does not grep for instruction files | WS-H | not-started | Shared | — | — | Depends: T-095; A7 |
| T-097 | Verify agent lists directory before reading | WS-H | not-started | Shared | — | — | Depends: T-095; A8 |

## Phase 6 — Provider Switching & Polish (gate M6)

| ID | Task | WS | Status | Owner | Started | Done | Notes |
|----|------|----|--------|-------|---------|------|-------|
| T-100 | Chat top-bar provider/model dropdown | WS-N | not-started | B | — | — | Depends: T-056, T-039 |
| T-101 | System-note append on switch | WS-I | not-started | Shared | — | — | Depends: T-100, T-054; A5 |
| T-102 | Workspace Inspector screen (read-only, guarded) | WS-N | not-started | B | — | — | Depends: T-017, T-039 |
| T-103 | Error banners, cancel, retry, loop cap surfacing | WS-N | not-started | B | — | — | Depends: T-058, T-060 |
| T-104 | Accessibility pass (labels, contrast, touch targets) | WS-H | not-started | Shared | — | — | Depends: all UI |
| T-105 | Dark theme + empty/loading states | WS-N | not-started | B | — | — | Depends: all UI |
| T-106 | Iteration cap (8) config + budget surfacing | WS-I | not-started | Shared | — | — | Depends: T-073 |
| T-107 | Per-chat provider resolution test on switch | WS-H | not-started | Shared | — | — | Depends: T-100, T-039; A18 |
| T-108 | Delete/rename/archive chat actions | WS-N | not-started | B | — | — | Depends: T-042 |
| T-109 | Polish pass: spacing, transitions, icons imports | WS-N | not-started | B | — | — | Depends: all UI |

## Phase 7 — Hardening & Release (gate M7)

| ID | Task | WS | Status | Owner | Started | Done | Notes |
|----|------|----|--------|-------|---------|------|-------|
| T-110 | Cross-chat sandbox escape tests | WS-H | not-started | Shared | — | — | Depends: T-017, T-039; A16 |
| T-111 | Secret redaction audit across logs and crash reporter | WS-H | not-started | Shared | — | — | Depends: T-043; A10 |
| T-112 | Audit chain tamper test on fresh install | WS-H | not-started | Shared | — | — | Depends: T-076 |
| T-113 | Donor checklist audit (supplement §4) | WS-P | not-started | A | — | — | Depends: all WS-P tasks; A13 |
| T-114 | Adapter contract tests in CI for all 4 adapters | WS-H | not-started | Shared | — | — | Depends: T-073, T-039, T-050, T-017; A14 |
| T-115 | No-Android-imports check in CI for :core-engine | WS-H | not-started | Shared | — | — | Depends: T-011; A15 |
| T-116 | Cross-chat escape and branch-guard end-to-end tests | WS-H | not-started | Shared | — | — | Depends: T-075, T-110; A16, A17 |
| T-117 | No references to donor broken members | WS-H | not-started | Shared | — | — | Depends: T-113; A19 |
| T-118 | Stream vs non-stream parity test in CI | WS-H | not-started | Shared | — | — | Depends: T-050; A20 |
| T-119 | Crash/ANR sweep; StrictMode clean | WS-H | not-started | Shared | — | — | Depends: all |
| T-120 | Baseline profile generation | WS-H | not-started | Shared | — | — | Depends: all |
| T-121 | Device matrix: API 26, 30, 34+ | WS-H | not-started | Shared | — | — | Depends: T-119 |
| T-122 | Release build: signing, R8, size audit | WS-H | not-started | Shared | — | — | Depends: T-121 |
| T-123 | Play listing assets + internal track upload | WS-H | not-started | Shared | — | — | Depends: T-122 |
| T-124 | Final acceptance walkthrough A1-A20 | WS-H | not-started | Shared | — | — | Depends: T-123 |

## Task count

| Phase | Defined | Note |
|-------|---------|------|
| 0 | 16 | Index range T-001…T-018; T-008, T-009, T-019 absent |
| 1 | 10 | |
| 2 | 15 | |
| 3 | 12 | |
| 4 | 12 | |
| 5 | 8 | |
| 6 | 10 | |
| 7 | 15 | |
| **Total** | **98** | Index states 124 |
