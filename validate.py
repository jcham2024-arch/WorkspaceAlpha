#!/usr/bin/env python3
"""Validate the baselayer (Baselayer.md §3 Step 6).

Run after any docs/, graph, or build change. Also run as the
git pre-commit hook (see .githooks/pre-commit).
"""
import hashlib, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent

def fail(m):
    print(f"FAIL: {m}")
    sys.exit(1)

for r in ["AGENTS.md", "CLAUDE.md", ".wiki/seed.py", ".wiki/build.py",
          ".context/graph.json", ".context/manifest.json", ".wiki/index.html"]:
    if not (ROOT / r).exists():
        fail(f"missing {r}")

m = json.loads((ROOT / ".context/manifest.json").read_text())
if m.get("version") != 1: fail("manifest version")
if "generated_from" not in m: fail("manifest missing generated_from")
if not isinstance(m.get("nodes"), list): fail("manifest nodes not a list")

for n in m["nodes"]:
    src = (ROOT / n["content_ref"]).read_bytes()
    s, e = n["byte_range"]
    if hashlib.sha256(src[s:e]).hexdigest() != n["sha256"]:
        fail(f"hash mismatch on {n['id']}")

ids = {n["id"] for n in m["nodes"]}
for e in m.get("edges", []):
    if e["from"] not in ids or e["to"] not in ids:
        fail(f"dangling edge {e}")

wiki = (ROOT / ".wiki/index.html").read_text(encoding="utf-8")
if len(wiki) < 500: fail("wiki suspiciously small")
if "<html" not in wiki.lower(): fail("wiki missing <html>")
if "<script" not in wiki.lower(): fail("wiki missing search script")

adj = {n["id"]: [] for n in m["nodes"]}
for e in m.get("edges", []):
    adj[e["from"]].append(e["to"])
WHITE, GRAY, BLACK = 0, 1, 2
color = dict.fromkeys(adj, WHITE)
def dfs(u):
    color[u] = GRAY
    for v in adj[u]:
        if color[v] == GRAY: fail("cycle detected")
        if color[v] == WHITE: dfs(v)
    color[u] = BLACK
for i in adj:
    if color[i] == WHITE: dfs(i)

lines = (ROOT / "AGENTS.md").read_text(encoding="utf-8").splitlines()
if len(lines) > 150: fail(f"AGENTS.md has {len(lines)} lines (> 150)")

print("PASS")
print(f"  nodes: {len(m['nodes'])}, edges: {len(m.get('edges', []))}")
print(f"  wiki bytes: {len(wiki)}, AGENTS.md lines: {len(lines)}")
budget = sum(n.get("est_tokens", 0) for n in m["nodes"])
print(f"  est. router tokens: {budget}")
