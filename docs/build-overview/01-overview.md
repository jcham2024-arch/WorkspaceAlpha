> **ChatWorkspace Build Task Overview** — Part 1 of 12
> Index: [`CONTEXT.md` §2.D](../../CONTEXT.md) · Next: [`02-phase0-foundation.md`](02-phase0-foundation.md)

# ChatWorkspace — Build Task Overview

**Document version:** 1.0
**Role:** Master task index for the ChatWorkspace build. References, but does not restate, the scope, supplement, and Harness repair kit.
**Audience:** Build lead, engineers, reviewers.
**Status:** Approved

---

## 0. How to use this document

This file is the single index of every build task. Each task has an ID (`T-xxx`), a phase, a workstream, a dependency list, an owner role, and an acceptance gate. Detailed acceptance criteria live in the referenced documents; this file only sequences and tracks.

- Product requirements: `ChatWorkspace — Project Scope & Build Plan` (the scope).
- Donor porting contracts and checklists: `ChatWorkspace — Supplement A: Clean Build with Donor Parts` (the supplement).
- Harness repair prompt and agent docs: the repair kit (prompt + 4 MD files).
- Per-task status: `docs/build-progress.md` (this file's companion tracker).

Update `docs/build-progress.md` when a task changes state. Update this file only when scope changes.

---

## 1. Workstreams

Six workstreams run across the twelve-week plan. Every task belongs to exactly one.

| ID | Workstream | Owner role | Purpose |
|---|---|---|---|
| WS-R | **Repair** | Android eng (donor) | Make the `Harness` branch compile and pass donor tests so donor parts are extractable |
| WS-S | **Scaffold** | Android eng (core) | ChatWorkspace module topology, Gradle, navigation, Room, DI |
| WS-P | **Donor port** | Android eng (donor) | Port D1–D9 behind adapters, complete checklists |
| WS-N | **New subsystems** | Android eng (feature) | Git, MCP, prompt builder, per-chat workspace, Create Chat, Providers UI |
| WS-I | **Integration** | Android eng (core) | Wire subsystems into the turn loop, chat UI, mid-chat switch |
| WS-H | **Hardening** | QA + Android eng | Security review, test matrix, release build |

WS-R runs **in parallel** with WS-S during Weeks 1–2 and must reach green before WS-P can port donor code from `Harness`. If WS-R slips, WS-P falls back to writing primitives from scratch — a 1.5-week buffer exists for this (§10).

---

## 2. Phase map and task counts

| Phase | Weeks | Tasks | Exit milestone |
|---|---|---|---|
| 0 Foundation | 1 | T-001 … T-018 | M0: Scaffold builds, donor parts compile, Harness green |
| 1 Providers | 2 | T-020 … T-029 | M1: Provider CRUD + encryption verified end to end |
| 2 Chat Creation & Git | 3–4 | T-030 … T-044 | M2: Branch-per-chat works against a real repo |
| 3 Chat Core | 5–6 | T-050 … T-061 | M3: End-to-end conversation persists and resumes |
| 4 MCP & Tools | 7–8 | T-070 … T-081 | M4: Tools visible, branch guard enforced |
| 5 Prompt & Docs | 9 | T-090 … T-097 | M5: Progressive disclosure proven by scripted scenarios |
| 6 Switch & Polish | 10 | T-100 … T-109 | M6: Mid-chat switch works, all UI states covered |
| 7 Hardening & Release | 11–12 | T-110 … T-124 | M7: Internal-track build passes A1–A20 |

Total tasks: **124**. Tasks marked `[P]` are parallelizable within their phase.

---
