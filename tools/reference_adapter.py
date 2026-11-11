#!/usr/bin/env python3
"""Reference adapter — end-to-end consumption of the WorkspaceAlpha baselayer.

Demonstrates the harness-adapter contract:
1. Read AGENTS.md for orientation
2. Read .context/manifest.json for the routing table
3. Hydrate sections by byte_range
4. Validate invariants (acyclic, unique IDs, valid hashes)
5. List active skills from .harness/skills/

This is a minimal working example. Real adapters can extend this pattern.

Usage: python3 tools/reference_adapter.py
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def read_agents_md() -> str:
    path = ROOT / "AGENTS.md"
    return path.read_text(encoding="utf-8")


def load_manifest() -> dict:
    path = ROOT / ".context" / "manifest.json"
    return json.loads(path.read_text(encoding="utf-8"))


def validate_invariants(manifest: dict) -> list[str]:
    """Return list of violation messages (empty if all pass)."""
    violations = []

    nodes = manifest.get("nodes", [])
    edges = manifest.get("edges", [])

    # Unique IDs
    ids = [n["id"] for n in nodes]
    if len(ids) != len(set(ids)):
        violations.append("duplicate node IDs")

    id_set = set(ids)

    # Edge referential integrity
    for e in edges:
        if e["from"] not in id_set:
            violations.append(f"edge from unknown node: {e['from']}")
        if e["to"] not in id_set:
            violations.append(f"edge to unknown node: {e['to']}")

    # DAG acyclicity (DFS)
    adj = {i: [] for i in ids}
    for e in edges:
        adj[e["from"]].append(e["to"])
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {i: WHITE for i in ids}

    def dfs(u):
        color[u] = GRAY
        for v in adj[u]:
            if color[v] == GRAY:
                violations.append(f"cycle detected: {u} -> {v}")
                return
            if color[v] == WHITE:
                dfs(v)
        color[u] = BLACK

    for i in ids:
        if color[i] == WHITE:
            dfs(i)

    # Hash verification
    for n in nodes:
        ref = n["content_ref"]
        s, e = n["byte_range"]
        try:
            data = (ROOT / ref).read_bytes()
            actual = hashlib.sha256(data[s:e]).hexdigest()
            if actual != n["sha256"]:
                violations.append(f"hash mismatch on {n['id']}")
        except Exception:
            violations.append(f"cannot read {ref} for {n['id']}")

    # Contract version
    if "contract_version" not in manifest:
        violations.append("missing contract_version")

    return violations


def list_active_skills() -> list[str]:
    """List active skills from .harness/skills/."""
    skills_dir = ROOT / ".harness" / "skills"
    if not skills_dir.exists():
        return []
    return sorted(d.name for d in skills_dir.iterdir() if d.is_dir())


def hydrate_section(node: dict) -> str:
    """Read a node's content by byte range."""
    ref = node["content_ref"]
    s, e = n_byte_range = node["byte_range"]
    data = (ROOT / ref).read_bytes()
    return data[s:e].decode("utf-8", "replace")


def main():
    print("=== Reference Adapter ===\n")

    # Step 1: Read AGENTS.md
    agents_md = read_agents_md()
    print(f"[1] AGENTS.md: {len(agents_md.splitlines())} lines, {len(agents_md)} bytes")

    # Step 2: Load manifest
    manifest = load_manifest()
    print(f"[2] manifest.json: {len(manifest['nodes'])} nodes, {len(manifest.get('edges', []))} edges")
    print(f"    contract_version: {manifest.get('contract_version', 'MISSING')}")

    # Step 3: Validate invariants
    violations = validate_invariants(manifest)
    if violations:
        print(f"[3] INVARIANT VIOLATIONS ({len(violations)}):")
        for v in violations:
            print(f"    - {v}")
        sys.exit(1)
    print("[3] All invariants pass (acyclic, unique IDs, valid hashes, contract_version)")

    # Step 4: Hydrate a section (first node)
    if manifest["nodes"]:
        first = manifest["nodes"][0]
        content = hydrate_section(first)
        print(f"[4] Hydrated '{first['id']}': {len(content)} bytes from {first['content_ref']}")

    # Step 5: List active skills
    skills = list_active_skills()
    print(f"[5] Active skills ({len(skills)}): {', '.join(skills) if skills else '(none)'}")

    print("\n=== Reference adapter complete ===")


if __name__ == "__main__":
    main()
