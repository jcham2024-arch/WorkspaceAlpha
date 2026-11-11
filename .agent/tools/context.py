"""Baselayer context tools — shared core for the MCP server and CLI.

Implements the Baselayer §9 contract:
  - compile_context(target_files): manifest traversal closure
  - read_section(node_id): exactly byte_range, sha256-verified bytes

Stdlib only. Read-only against the baselayer; never writes manifest/wiki.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / ".context" / "manifest.json"


def _load_manifest():
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"missing {MANIFEST_PATH.relative_to(ROOT)} — run python3 build.py first")
    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def _manifest_nodes():
    m = _load_manifest()
    return {n["id"]: n for n in m.get("nodes", [])}, m.get("edges", [])


def compile_context(target_files):
    """Return {target file -> [node ids in requires closure]}.

    Matches AGENTS.md §1 traversal: start from nodes whose content_ref
    is in target_files, follow requires edges transitively.
    """
    nodes, edges = _manifest_nodes()
    requires = {}
    for e in edges:
        if e.get("type") == "requires":
            requires.setdefault(e.get("from"), []).append(e.get("to"))

    seeds = {}
    for nid, n in nodes.items():
        ref = n.get("content_ref", "").split("#")[0]
        if ref in target_files:
            seeds.setdefault(ref, []).append(nid)
    for ref in target_files:
        seeds.setdefault(ref, [])

    out = {}
    for ref in target_files:
        seen = set()
        stack = list(seeds[ref])
        while stack:
            cur = stack.pop()
            if cur in seen or cur not in nodes:
                continue
            seen.add(cur)
            stack.extend(requires.get(cur, []))
        out[ref] = sorted(seen)
    return out


def read_section(node_id):
    """Return the exact bytes for node_id, verifying sha256."""
    nodes, _ = _manifest_nodes()
    if node_id not in nodes:
        raise KeyError(f"unknown node: {node_id}")
    n = nodes[node_id]
    ref = n["content_ref"].split("#")[0]
    data = (ROOT / ref).read_bytes()
    s, e = n["byte_range"]
    chunk = data[s:e]
    if hashlib.sha256(chunk).hexdigest() != n["sha256"]:
        raise ValueError(f"sha256 mismatch on {node_id} — rebuild with python3 seed.py && python3 build.py")
    return chunk


def search_nodes(query, limit=20):
    """Substring search on node summaries (convenience layer)."""
    nodes, _ = _manifest_nodes()
    q = query.lower()
    hits = [n for n in nodes.values() if q in (n.get("summary") or "").lower() or q in n["id"].lower()]
    return [{"id": n["id"], "summary": n["summary"], "content_ref": n["content_ref"]} for n in hits[:limit]]


def list_nodes(limit=50, offset=0):
    nodes, _ = _manifest_nodes()
    items = sorted(nodes.values(), key=lambda n: n["id"])
    return [{"id": n["id"], "summary": n["summary"]} for n in items[offset:offset + limit]]


def knowledge_search(query, limit=10):
    """Keyword search over the memory knowledge DB (FTS5, bounded)."""
    import sqlite3
    db = ROOT / ".context" / "knowledge.db"
    if not db.exists():
        return {"entries": [], "note": "knowledge DB missing — run knowledge.py sync"}
    con = sqlite3.connect(db)
    rows = con.execute(
        "SELECT date, kind, title, body, tags FROM entries_fts"
        " WHERE entries_fts MATCH ? LIMIT ?", (query, limit)).fetchall()
    con.close()
    return {"entries": [{"date": r[0], "kind": r[1], "title": r[2],
                         "body": (r[3] or "")[:300], "tags": r[4]} for r in rows]}


def knowledge_last(kind, n=5):
    """Most recent memory entries of one kind."""
    import sqlite3
    db = ROOT / ".context" / "knowledge.db"
    if not db.exists():
        return {"entries": [], "note": "knowledge DB missing — run knowledge.py sync"}
    con = sqlite3.connect(db)
    rows = con.execute(
        "SELECT date, title, body, tags FROM entries WHERE kind=? ORDER BY date DESC, rowid DESC LIMIT ?",
        (kind, n)).fetchall()
    con.close()
    return {"entries": [{"date": r[0], "title": r[1], "body": (r[2] or "")[:300], "tags": r[3]} for r in rows]}


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "context":
        files = sys.argv[2:]
        print(json.dumps(compile_context(files), indent=2))
    elif cmd == "section":
        sys.stdout.write(read_section(sys.argv[2]).decode("utf-8", "replace"))
    elif cmd == "search":
        print(json.dumps(search_nodes(sys.argv[2]), indent=2))
    else:
        sys.exit("usage: context.py context <file...> | section <node_id> | search <query>")
