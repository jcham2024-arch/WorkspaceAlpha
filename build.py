#!/usr/bin/env python3
"""Compile .context/graph.json into .context/manifest.json and wiki/index.html.

Zero external dependencies. Validates the DAG (acyclicity, referential
integrity, uniqueness) and fails hard on violation.
"""
from __future__ import annotations
import hashlib, html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GRAPH_PATH = ROOT / ".context" / "graph.json"
MANIFEST_PATH = ROOT / ".context" / "manifest.json"
WIKI_PATH = ROOT / "wiki" / "index.html"

def load_graph() -> dict:
    if not GRAPH_PATH.exists():
        sys.exit(f"missing {GRAPH_PATH.relative_to(ROOT)} — run seed.py first")
    with GRAPH_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def validate(graph: dict) -> None:
    ids = [n["id"] for n in graph["nodes"]]
    if len(ids) != len(set(ids)):
        sys.exit("duplicate node id")
    id_set = set(ids)
    adj = {i: [] for i in ids}
    for e in graph.get("edges", []):
        f, t = e.get("from"), e.get("to")
        if f not in id_set or t not in id_set:
            sys.exit(f"edge references unknown node: {e}")
        if f == t:
            sys.exit(f"self-loop: {e}")
        adj[f].append(t)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {i: WHITE for i in ids}
    def dfs(u):
        color[u] = GRAY
        for v in adj[u]:
            if color[v] == GRAY:
                sys.exit(f"cycle detected through {u} -> {v}")
            if color[v] == WHITE:
                dfs(v)
        color[u] = BLACK
    for i in ids:
        if color[i] == WHITE:
            dfs(i)

def read_node_bytes(node: dict) -> bytes:
    ref = node["content_ref"].split("#")[0]
    path = ROOT / ref
    if not path.exists():
        sys.exit(f"node {node['id']}: content file missing: {ref}")
    data = path.read_bytes()
    br = node.get("byte_range")
    if br:
        start, end = br
        data = data[start:end]
    return data

def build_manifest(graph: dict) -> dict:
    nodes = []
    for n in graph["nodes"]:
        raw = read_node_bytes(n)
        nodes.append({
            "id": n["id"],
            "type": n.get("type", "doc"),
            "summary": n.get("summary", ""),
            "tags": n.get("tags", []),
            "content_ref": n["content_ref"],
            "byte_range": n.get("byte_range"),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
        })
    return {
        "version": graph.get("version", 1),
        "generated_from": "graph.json",
        "nodes": nodes,
        "edges": graph.get("edges", []),
    }

def md_to_html(text: str) -> str:
    out, in_code, code_buf, para = [], False, [], []
    def inline(s: str) -> str:
        s = html.escape(s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        return s
    def flush_para():
        if para:
            joined = " ".join(x.strip() for x in para).strip()
            if joined:
                out.append(f"<p>{inline(joined)}</p>")
            para.clear()
    for line in text.splitlines():
        if line.startswith("```"):
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>")
                code_buf.clear()
                in_code = False
            else:
                flush_para()
                in_code = True
            continue
        if in_code:
            code_buf.append(line)
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush_para()
            out.append(f"<h{len(m.group(1))}>{inline(m.group(2))}</h{len(m.group(1))}>")
            continue
        if not line.strip():
            flush_para()
            continue
        para.append(line)
    if in_code and code_buf:
        out.append("<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>")
    flush_para()
    return "\n".join(out)

def build_wiki(graph: dict) -> str:
    requires = {n["id"]: [] for n in graph["nodes"]}
    required_by = {n["id"]: [] for n in graph["nodes"]}
    for e in graph.get("edges", []):
        requires[e["from"]].append((e["to"], e.get("type", "requires")))
        required_by[e["to"]].append((e["from"], e.get("type", "requires")))

    groups = {}
    for n in graph["nodes"]:
        ref = n["content_ref"]
        prefix = ref.split("/")[0] if "/" in ref else "(root)"
        groups.setdefault(prefix, []).append(n)

    sidebar = []
    for g in sorted(groups):
        sidebar.append(f'<div class="group-label">{html.escape(g)}</div>')
        for n in sorted(groups[g], key=lambda x: x["id"]):
            label = (n.get("summary") or n["id"])[:60]
            sidebar.append(f'<a class="nav-item" href="#{html.escape(n["id"])}">{html.escape(label)}</a>')

    sections = []
    for n in graph["nodes"]:
        raw_bytes = read_node_bytes(n)
        raw_text = raw_bytes.decode("utf-8", "replace")
        sha = hashlib.sha256(raw_bytes).hexdigest()
        req = "".join(
            f'<a href="#{html.escape(t)}">{html.escape(t)}</a> <span class="edge-type">({html.escape(ty)})</span><br>'
            for t, ty in requires[n["id"]]) or "<em>none</em>"
        req_by = "".join(
            f'<a href="#{html.escape(f)}">{html.escape(f)}</a> <span class="edge-type">({html.escape(ty)})</span><br>'
            for f, ty in required_by[n["id"]]) or "<em>none</em>"
        sections.append(f'''
<section id="{html.escape(n["id"])}" data-sha256="{sha}">
  <div class="node-meta">
    <span class="badge">{html.escape(n.get("type","doc"))}</span>
    <span class="ref">{html.escape(n["content_ref"])}</span>
  </div>
  <h2>{html.escape(n["id"])}</h2>
  <p class="summary">{html.escape(n.get("summary",""))}</p>
  <div class="content">{md_to_html(raw_text)}</div>
  <div class="edges">
    <div><strong>requires</strong><br>{req}</div>
    <div><strong>required by</strong><br>{req_by}</div>
  </div>
</section>''')

    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<title>Workspace Wiki</title>
<style>
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
        display: grid; grid-template-columns: 300px 1fr; min-height: 100vh; color: #1a1a1a; }}
nav {{ background: #f6f7f9; border-right: 1px solid #e3e5e8; padding: 16px; height: 100vh;
      overflow-y: auto; position: sticky; top: 0; }}
nav input {{ width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 6px;
             font-size: 14px; margin-bottom: 12px; }}
.group-label {{ font-size: 11px; font-weight: 700; text-transform: uppercase;
                letter-spacing: 0.5px; color: #6b7280; margin: 14px 0 6px; }}
.nav-item {{ display: block; padding: 6px 8px; font-size: 13px; color: #333;
             text-decoration: none; border-radius: 4px; overflow: hidden;
             text-overflow: ellipsis; white-space: nowrap; }}
.nav-item:hover {{ background: #e8eaee; }}
main {{ padding: 32px 48px; max-width: 960px; }}
section {{ padding: 24px 0; border-bottom: 1px solid #eee; scroll-margin-top: 16px; }}
section:target {{ background: #fffbe6; }}
.node-meta {{ font-size: 12px; color: #6b7280; margin-bottom: 6px; }}
.badge {{ background: #e0e7ff; color: #3730a3; padding: 2px 8px; border-radius: 4px;
          font-size: 11px; margin-right: 8px; font-weight: 600; }}
.ref {{ font-family: ui-monospace, SFMono-Regular, monospace; }}
h2 {{ margin: 4px 0 8px; font-family: ui-monospace, SFMono-Regular, monospace; font-size: 18px; }}
.summary {{ color: #555; font-style: italic; margin: 0 0 16px; }}
.content pre {{ background: #f4f5f7; padding: 12px; border-radius: 6px; overflow-x: auto; font-size: 13px; }}
.content code {{ background: #f4f5f7; padding: 1px 5px; border-radius: 3px; font-size: 0.9em; }}
.content a {{ color: #2563eb; }}
.edges {{ margin-top: 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 16px;
          font-size: 13px; padding: 12px; background: #fafbfc; border-radius: 6px; }}
.edges a {{ color: #2563eb; text-decoration: none; font-family: ui-monospace, monospace; }}
.edge-type {{ color: #9ca3af; font-size: 11px; }}
</style></head>
<body>
<nav>
  <input id="search" placeholder="Search nodes…" oninput="filterNodes()">
  {chr(10).join(sidebar)}
</nav>
<main>
  <h1 style="margin-top:0">Workspace Wiki</h1>
  <p style="color:#6b7280; font-size:14px; margin-bottom:32px">
    Generated from <code>.context/graph.json</code>. Every node is addressable as <code>#node_id</code>.
  </p>
  {chr(10).join(sections)}
</main>
<script>
function filterNodes() {{
  const q = document.getElementById('search').value.toLowerCase();
  document.querySelectorAll('.nav-item').forEach(a => {{
    a.style.display = a.textContent.toLowerCase().includes(q) ? 'block' : 'none';
  }});
}}
</script>
</body></html>'''

def main():
    graph = load_graph()
    validate(graph)
    manifest = build_manifest(graph)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    WIKI_PATH.parent.mkdir(parents=True, exist_ok=True)
    WIKI_PATH.write_text(build_wiki(graph), encoding="utf-8")
    print(f"wrote {MANIFEST_PATH.relative_to(ROOT)} ({len(manifest['nodes'])} nodes)")
    print(f"wrote {WIKI_PATH.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
