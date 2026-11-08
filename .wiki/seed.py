#!/usr/bin/env python3
"""Walk docs/ and emit .context/graph.json with one node per Markdown heading.

Idempotent: re-running regenerates the graph from current docs/ state. Edges
are preserved if they still reference valid nodes; otherwise they are dropped
with a warning.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
GRAPH = ROOT / ".context" / "graph.json"

HEADING_RE = re.compile(rb"^(#{1,6})\s+(.*)$")

def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "section"

def section_ranges(data: bytes):
    """Yield (byte_start, byte_end, level, title) for each heading-delimited section."""
    heads = []
    pos = 0
    for line in data.split(b"\n"):
        m = HEADING_RE.match(line)
        if m:
            heads.append((pos, len(m.group(1)), m.group(2).decode("utf-8", "replace").strip()))
        pos += len(line) + 1
    for i, (start, level, title) in enumerate(heads):
        end = heads[i + 1][0] if i + 1 < len(heads) else len(data)
        yield start, end, level, title

def load_existing_edges():
    if not GRAPH.exists():
        return []
    try:
        old = json.loads(GRAPH.read_text(encoding="utf-8"))
        return old.get("edges", [])
    except Exception:
        return []

def main():
    nodes, seen = [], set()
    if DOCS.exists():
        for path in sorted(DOCS.rglob("*.md")):
            rel = str(path.relative_to(ROOT))
            data = path.read_bytes()
            if not data:
                continue
            for (start, end, level, title) in section_ranges(data):
                nid = f"{rel}::{slug(title)}"
                if nid in seen:
                    continue
                seen.add(nid)
                nodes.append({
                    "id": nid,
                    "type": "doc",
                    "summary": title,
                    "content_ref": rel,
                    "byte_range": [start, end],
                    "tags": [],
                })
    edges = [e for e in load_existing_edges()
             if e.get("from") in seen and e.get("to") in seen]
    GRAPH.parent.mkdir(parents=True, exist_ok=True)
    GRAPH.write_text(json.dumps({"version": 1, "nodes": nodes, "edges": edges},
                                indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {GRAPH.relative_to(ROOT)} ({len(nodes)} nodes, {len(edges)} edges)")

if __name__ == "__main__":
    main()
