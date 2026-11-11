# ADR-001: Why a DAG for Documentation Routing

## Status

Accepted

## Context

The baselayer workspace needs a documentation system that serves two audiences:
- **Humans** who need an explorable, cross-linked wiki
- **AI agents** who need a token-efficient router that surfaces only relevant sections

A flat directory of Markdown files doesn't scale: agents can't tell which sections are relevant without reading everything, and humans can't navigate cross-references without manual link maintenance.

A graph database would be powerful but adds dependencies and operational complexity. A simple index file loses the structural relationships between sections.

## Decision

Use a Directed Acyclic Graph (DAG) where:
- **Nodes** are documentation sections (one per Markdown heading), identified by `path::slug`
- **Edges** are `requires` relationships between sections
- **Byte ranges** pin each node to an exact slice of its source file
- **SHA-256 hashes** verify content integrity

The graph is compiled from `docs/` by `seed.py`, then rendered to `manifest.json` (agent router) and `.wiki/index.html` (human wiki) by `build.py`.

## Consequences

**Positive:**
- Agents read only relevant sections (byte-range hydration), keeping router under ~15% of context budget
- Humans get an explorable, cross-linked wiki with search
- Content integrity verified via SHA-256 on every build
- DAG acyclicity enforced at build time — no circular references

**Negative:**
- Adding a new section requires editing `docs/` then rebuilding (not live-editing the graph)
- Edge relationships are manual (declared in manifest edges, not auto-discovered)
- The DAG is a compile-time artifact, not a runtime query engine

## Links

- Build pipeline: `BOOTSTRAPPER.md` §3
- Agent router: `AGENTS.md`
- Wiki: `.wiki/index.html`
