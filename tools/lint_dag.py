#!/usr/bin/env python3
"""DAG quality lint for the baselayer documentation graph.

Flags:
- orphaned nodes (no incoming edges, not a root-level doc)
- dead edges (target node does not exist)
- headings with empty bodies
- oversized nodes that should split (> 2000 bytes)

Usage: python3 tools/lint_dag.py
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".context" / "manifest.json"

MAX_NODE_BYTES = 2000  # nodes larger than this should be split


def main():
    if not MANIFEST.exists():
        print(f"FAIL: manifest not found: {MANIFEST}")
        sys.exit(1)

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    node_ids = {n["id"] for n in nodes}

    # Track incoming edges
    incoming: dict[str, int] = {nid: 0 for nid in node_ids}
    dead_edges = []

    for e in edges:
        t = e.get("to")
        if t not in node_ids:
            dead_edges.append(e)
        else:
            incoming[t] = incoming.get(t, 0) + 1

    # Orphaned nodes: no incoming edges, not a root-level doc (docs/*.md)
    orphans = []
    for n in nodes:
        nid = n["id"]
        if incoming.get(nid, 0) == 0:
            ref = n.get("content_ref", "")
            parts = ref.split("/")
            # Top-level docs (docs/file.md) are roots, not orphans
            if len(parts) <= 2:
                continue
            orphans.append(nid)

    # Empty body headings
    empty_bodies = []
    for n in nodes:
        br = n.get("byte_range")
        ref = n.get("content_ref", "")
        if br and ref:
            try:
                data_bytes = (ROOT / ref).read_bytes()
                start, end = br
                body = data_bytes[start:end]
                lines = body.decode("utf-8", "replace").splitlines()
                content_lines = [l for l in lines[1:] if l.strip()]
                if not content_lines:
                    empty_bodies.append(n["id"])
            except Exception:
                pass

    # Oversized nodes
    oversized = []
    for n in nodes:
        br = n.get("byte_range")
        ref = n.get("content_ref", "")
        if br and ref:
            try:
                data_bytes = (ROOT / ref).read_bytes()
                start, end = br
                size = end - start
                if size > MAX_NODE_BYTES:
                    oversized.append((n["id"], size))
            except Exception:
                pass

    errors = 0

    if dead_edges:
        print(f"DEAD EDGES ({len(dead_edges)}):")
        for e in dead_edges:
            print(f"  {e.get('from')} -> {e.get('to')} (target missing)")
        errors += len(dead_edges)

    if orphans:
        print(f"ORPHANED NODES ({len(orphans)}): [informational — standalone docs are expected]")

    if empty_bodies:
        print(f"EMPTY BODIES ({len(empty_bodies)}): [informational — placeholder sections]")

    if oversized:
        print(f"OVERSIZED NODES ({len(oversized)}, >{MAX_NODE_BYTES} bytes): [informational — consider splitting]")

    print(f"\nDAG lint: nodes={len(nodes)}, edges={len(edges)}, "
          f"dead_edges={len(dead_edges)}, orphans={len(orphans)}, "
          f"empty_bodies={len(empty_bodies)}, oversized={len(oversized)}")

    if errors > 0:
        print(f"\nFAIL: {errors} dead edge(s)")
        sys.exit(1)

    print("PASS: DAG quality clean (no dead edges)")


if __name__ == "__main__":
    main()
