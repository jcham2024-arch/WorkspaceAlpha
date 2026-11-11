# ADR-002: Why Byte Ranges for Section-Level Access

## Status

Accepted

## Context

The baselayer indexes `docs/` Markdown files at the section level (one node per heading). Two approaches were considered:

1. **File-level indexing**: Each `.md` file is one node. Agents must read entire files to find relevant content.
2. **Section-level indexing**: Each heading-delimited section is one node with a `byte_range` pinpointing its exact location in the file.

File-level indexing wastes tokens: an agent looking for one configuration detail must read the whole file. Section-level indexing enables token-efficient hydration but requires precise byte tracking.

## Decision

Use section-level indexing with `byte_range: [start, end]` in every manifest node. The `seed.py` compiler scans each Markdown file, identifies heading lines via regex, and computes exact byte offsets. The `build.py` compiler validates that each byte range's SHA-256 matches the content at that slice.

Agents hydrate sections by reading exactly `content_ref` bytes `[start:end]` — never the whole file.

## Consequences

**Positive:**
- Token-efficient: agents read only relevant sections
- Content integrity: SHA-256 on byte slice detects any drift
- Progressive disclosure: frontmatter (~50-100 tokens) always loaded, body on demand
- Router stays under ~15% of context budget (~1,400-10,000 tokens depending on corpus size)

**Negative:**
- Byte ranges break if file content shifts (sections insert/delete lines) — requires rebuild
- No live editing of individual sections without re-indexing
- Slightly more complex compiler (must track byte positions during scan)

## Links

- Compiler: `.wiki/seed.py`
- Validator: `validate.py` (hash check on every node)
- Agent protocol: `AGENTS.md` §2
