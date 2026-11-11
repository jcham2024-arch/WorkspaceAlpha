# ADR-005: Phase 0 Audit Findings and Phase 1 Release Gates

## Status

Accepted

## Context

The attached "WorkspaceAlpha Next-Step Implementation Instructions" defines seven workstreams for converting the baselayer from a prototype into a production-grade context engine. Phase 0 (audit) and Phase 1 (hardening) are the immediate priority.

## Phase 0 Audit Findings

| Area | Finding | Severity |
|------|---------|----------|
| Graph schema | `graph.json` has `version: 1` but no `schema_version` field | Medium |
| Manifest | Already has `contract_version: "1.0.0"` | OK |
| Byte range validation | `validate.py` checked SHA-256 but not range bounds (start<end, within file) | Medium |
| Structured logging | `print()` statements only, no severity levels | Low |
| Malformed input | `seed.py` crashes on symlinks, binary files, oversized files | Medium |
| MCP server | Synchronous, no timeouts, no metrics, no graceful shutdown, no per-call hash verification | High |
| Test coverage | No tests for MCP server, audit, lint_dag, dedup, stale, context_budget, check_links, scan_secrets, validate, reference_adapter | High |
| CI | No CI workflow | High |
| Skill licensing | All 3,518 skills have `upstream_license` field; 104 have known licenses, rest "unknown" | OK |

## Phase 1 Changes Implemented (COMPLETE)

1. **Graph schema versioning** — Added `schema_version: "1.0.0"` to `graph.json` (seed.py) and propagated to `manifest.json` (build.py).
2. **Byte range validation** — `build.py` and `validate.py` now check: start >= 0, end > start, end <= file size.
3. **Structured logging** — `seed.py`, `build.py`, `validate.py`, MCP `server.py` use `logging` module with INFO/WARNING/ERROR severity to stderr.
4. **Graceful malformed input** — `seed.py` skips symlinks, files > 10MB, and binary files (null byte check) with WARNING logs.
5. **MCP server hardening** — Added structured logging, request metrics (count, latency, token bytes, verification failures, errors), per-call SHA-256 verification on `read_section`, graceful shutdown on SIGTERM/SIGINT, health check (`ping` returns structured status).
6. **MCP integration tests** — `tests/test_mcp.py` with 9 tests covering ping, tools/list, read_section (verified + unknown node), compile_context, search_nodes, list_nodes, unknown tool, invalid JSON.
7. **CI workflow** — `.github/workflows/ci.yml` runs unit tests, build pipeline, skill audit, build determinism check, .env-not-committed check, pre-commit hook executable check, Python syntax linting.

## Phase 2 — Unified Prompt Stack (COMPLETE)

1. **Envelope schemas** — `envelope/handoff-envelope.schema.json`, `envelope/return-envelope.schema.json` (JSON Schema draft-07).
2. **Envelope templates** — `envelope/mission-envelope.yaml`, `envelope/execution-envelope.yaml` (MISSION/EXECUTION delegation templates).
3. **Prompt DAG** — `.context/prompt-graph.json` (16 nodes: 3 SystemPrompt, 4 Skill, 2 Envelope, 2 Adapter, 1 OutputContract, 4 ContextSlice; 16 edges across 5 types).
4. **DAG Compiler** — `assembly/manifest_reader.py`, `assembly/slicer.py`, `assembly/budgeter.py`, `assembly/assembler.py` (Plan→Bind→Optimize→Execute→Feedback with budget-aware pruning).
5. **Model Adapters** — `adapters/deepseek_v32.py`, `adapters/nemotron_35.py`, `adapters/dispatch.py` (thinking mode, token floors, format selection).
6. **Provenance Recorder** — `provenance/recorder.py` (per-turn JSONL + human-readable summaries).
7. **Wiki Views** — `wiki/views/generator.py` (conversation, prompt-chunk, conceptual-expansion views).
8. **Prompt Prefixes** — `assembly/prefix/orchestrator.md`, `assembly/prefix/manager.md`, `assembly/prefix/production.md` (byte-identical, cache-keyed).

## Release Gates (per attached document)

| Gate | Criteria | Status |
|------|----------|--------|
| Deterministic builds | `manifest.json` byte-identical across consecutive `build.py` runs | ✅ CI verifies |
| Validated graphs | `validate.py` passes (hashes, DAG, byte ranges) | ✅ CI verifies |
| Async MCP runtime | Async request handling, bounded concurrency, timeouts, cancellation | ⏳ Phase 1 added metrics/shutdown; async not yet implemented |
| Health checks + metrics | MCP `ping` returns healthy; request metrics logged | ✅ Implemented |
| Reproducible benchmarks | Benchmark harness with measurable value | ❌ Not yet started |
| Two ecosystem integrations | LangChain + TypeScript client examples | ❌ Not yet started |
| Automated license enforcement | CI blocks unlicensed/restricted skills from trusted tiers | ❌ Not yet started |
| No plaintext `.env` in production | `.agent/.env` gitignored; CI verifies not tracked | ✅ CI verifies |
| Offline-first privacy | All tooling stdlib-only; no network by default | ✅ Maintained |
| Prompt DAG schema | Versioned graph schema + routing protocol spec | ✅ Complete (prompt-graph.schema.json) |
| DAG compiler | Plan→Bind→Optimize→Execute→Feedback with budget enforcement | ✅ Implemented |
| Model adapters | DeepSeek V3.2 + Nemotron 3.5 with tiered dispatch | ✅ Implemented |
| Provenance recording | Per-turn JSONL records + human-readable summaries | ✅ Implemented |
| Wiki views | Conversation, Prompt Chunk, Conceptual Expansion | ✅ Implemented |

## Links

- Build pipeline: `.wiki/seed.py`, `.wiki/build.py`
- Validator: `validate.py`
- MCP server: `.agent/tools/mcp/server.py`
- CI: `.github/workflows/ci.yml`
- Skill audit: `.agent/tools/audit.py`
- Tier definitions: `.agent/skills/TIERS.md`
- Prompt DAG: `.context/prompt-graph.json`
- DAG Compiler: `assembly/assembler.py`
- Model Adapters: `adapters/`
- Provenance: `provenance/recorder.py`
- Wiki Views: `wiki/views/generator.py`
