# BASELAYER.md — Agentic Workspace Build Specification

> **Instruction to the agent reading this file:**
> You are bootstrapping an agentic workspace. Execute Sections 3–7 in order.
> Do not skip validation. Do not invent documentation content — index what
> exists, and record gaps as observations. When you finish, the workspace
> must satisfy every invariant in Section 8.

> **Instruction to a human reading this file:**
> Drop this file at the root of a work folder and run the agent. The agent
> will produce a two-surface system: (1) an offline HTML wiki for human
> review, and (2) a token-efficient DAG router for agents. Both are
> compiled from one canonical graph. Nothing here requires npm, pip, or a
> network connection.

---

## 1. Mission

Build a **baselayer** — the lowest, least-replaceable layer of an agentic
platform. The baselayer provides exactly two surfaces and nothing more:

| Surface | Audience | Form |
|---|---|---|
| **Wiki** | Humans | `wiki/index.html` — offline, self-contained, anchor-addressable |
| **Router** | Agents | `AGENTS.md` + `.context/manifest.json` + `.context/graph.json` |

Both surfaces derive from one canonical file: `.context/graph.json`.

The baselayer does **not** include retrieval, embeddings, MCP servers, or
model integration. Those are *layers above* the baselayer and can be added
later without changing the graph. The baselayer must work in a plain
terminal with Python 3 and a browser.

---

## 2. Directory contract

The agent must produce exactly this tree. Existing user files under `docs/`
are preserved; everything else is created.

```text
<root>/
├── BASELAYER.md               ← this file (input)
├── AGENTS.md                  ← first-read agent router (generated)
├── CLAUDE.md                  ← one-line shim: @AGENTS.md
├── build.py                   ← compiler: graph.json → manifest + wiki
├── seed.py                    ← bootstrapper: docs/ → graph.json
├── .context/
│   ├── graph.json             ← canonical DAG (source of truth)
│   ├── manifest.json          ← generated agent routing table
│   └── index.md               ← plain-file fallback index (generated)
├── docs/                      ← existing project documentation
│   └── ...
└── wiki/
    └── index.html             ← generated human audit surface
```

**Rules:**
- `.context/graph.json` is the only writable knowledge source.
- `.context/manifest.json` and `wiki/index.html` are **build artifacts** —
  never hand-edited, always regenerated.
- `docs/` is never rewritten by the build. The graph **references** it.
- `AGENTS.md` is the only file an agent reads first. Keep it under 150
  lines; its content is recurring per-session token cost.

---

## 3. Execution order

Run these steps in sequence. Stop and report if any step fails.

### Step 1 — Scaffold directories

```bash
mkdir -p .context docs wiki
```

If `docs/` already contains files, do not modify them. If it is empty,
create one placeholder file so the seed step has input:

```bash
cat > docs/README.md <<'EOF'
# Project Documentation

This directory holds the project's specifications, standards, and
instructional documents. The baselayer indexes these files; it does not
rewrite them.

## Getting Started

Replace this file with real project documentation. Any Markdown file placed
under `docs/` will be indexed on the next build.
EOF
```

### Step 2 — Write `seed.py`

Copy the exact content from **Section 5.1**. This script walks `docs/` and
emits an initial `.context/graph.json` with one node per Markdown heading,
each carrying a byte range.

### Step 3 — Write `build.py`

Copy the exact content from **Section 5.2**. This script validates the DAG,
resolves byte ranges, computes hashes, and emits both
`.context/manifest.json` and `wiki/index.html`.

### Step 4 — Write `AGENTS.md` and `CLAUDE.md`

Copy the exact content from **Section 5.3** (`AGENTS.md`) and **Section
5.4** (`CLAUDE.md`).

### Step 5 — Run the build

```bash
python3 seed.py
python3 build.py
```

Expected output: `wrote .context/graph.json (N nodes)` then
`wrote .context/manifest.json (N nodes)` and `wrote wiki/index.html`.

### Step 6 — Validate

```bash
python3 - <<'EOF'
import json, pathlib, sys
g = json.load(open(".context/graph.json"))
m = json.load(open(".context/manifest.json"))
w = pathlib.Path("wiki/index.html")
assert g["nodes"], "graph has no nodes"
assert len(m["nodes"]) == len(g["nodes"]), "manifest/graph node count mismatch"
assert w.exists() and w.stat().st_size > 1000, "wiki missing or trivial"
ids = {n["id"] for n in g["nodes"]}
for e in g["edges"]:
    assert e["from"] in ids and e["to"] in ids, f"bad edge: {e}"
html = w.read_text()
for n in g["nodes"]:
    assert f'id="{n["id"]}"' in html, f"wiki missing anchor: {n['id']}"
print(f"OK: {len(g['nodes'])} nodes, {len(g['edges'])} edges, wiki {w.stat().st_size} bytes")
EOF
```

Open `wiki/index.html` in a browser to confirm it renders.

---

## 4. Schemas

### 4.1 `.context/graph.json`

The canonical DAG. Human-editable, machine-validated.

```json
{
  "version": 1,
  "nodes": [
    {
      "id": "docs/security/session.md::session-boundary",
      "type": "rule",
      "summary": "Session tokens must never cross service boundaries unencrypted.",
      "content_ref": "docs/security/session.md",
      "byte_range": [1842, 2210],
      "tags": ["security", "auth", "must"]
    }
  ],
  "edges": [
    {
      "from": "docs/api/rate-limits.md::limits",
      "to": "docs/security/session.md::session-boundary",
      "type": "requires"
    }
  ]
}
```

**Node fields:**

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Stable, unique. Convention: `<path>::<slug>` |
| `type` | yes | One of `rule`, `spec`, `workflow`, `ref`, `doc` |
| `summary` | yes | One line. The agent reads this before hydrating content. |
| `content_ref` | yes | Repo-relative path. May include `#anchor` for human navigation. |
| `byte_range` | no | `[start, end]` offsets into the file. Omit for whole-file nodes. |
| `tags` | no | Free-form labels used for wiki grouping. |

**Edge fields:**

| Field | Meaning |
|---|---|
| `from` | Source node id |
| `to` | Target node id |
| `type` | `requires` \| `specializes` \| `supersedes` \| `implements` \| `contradicts` |

**Invariants (enforced by `build.py`):** acyclic; all edge endpoints exist;
no self-loops; no duplicate ids.

### 4.2 `.context/manifest.json`

Generated. Never hand-edited. The agent reads this (via MCP later, or
directly via file read as a fallback) to route.

```json
{
  "version": 1,
  "generated_from": "graph.json",
  "nodes": [
    {
      "id": "docs/security/session.md::session-boundary",
      "type": "rule",
      "summary": "Session tokens must never cross service boundaries unencrypted.",
      "tags": ["security", "auth", "must"],
      "content_ref": "docs/security/session.md",
      "byte_range": [1842, 2210],
      "sha256": "a3f9c1…",
      "bytes": 368
    }
  ],
  "edges": [ { "from": "…", "to": "…", "type": "requires" } ]
}
```

Key property: the agent can decide whether to hydrate a node **without
reading its content**, using only `summary` and `bytes`.

---

## 5. File contents

Copy each file exactly. Do not paraphrase.

### 5.1 `seed.py`

```python
#!/usr/bin/env python3
"""Walk docs/ and emit .context/graph.json with one node per Markdown heading.

Idempotent: re-running regenerates the graph from current docs/ state. Edges
are preserved if they still reference valid nodes; otherwise they are dropped
with a warning.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
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
```

### 5.2 `build.py`

```python
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
```

### 5.3 `AGENTS.md`

```markdown
# AGENTS.md — Context Navigation Entry Point

This repository uses a DAG-routed documentation system. You are not expected
to grep, search, or read documentation files wholesale. Follow this protocol.

## 1. Orientation (read once per task)

1. Identify the **target files** or **task archetype** for the current task.
2. Read `.context/manifest.json` — it is small, and it is the routing table.
3. Select the nodes whose `summary` matches the task. Follow `requires`
   edges transitively. Stop when no further `requires` edges are relevant.
4. Do not browse `docs/` directly. Do not `grep` for content. Do not read
   whole files to find one section.

## 2. Chunk access (section-level, never file-level)

Every node in the manifest carries:
- `id` — stable identifier, also an anchor in `wiki/index.html`
- `sha256` — content hash for provenance
- `byte_range` — exact slice of the source file
- `bytes` — size of the section
- `summary` — one-line orientation

Use `summary` first. Hydrate the section only when the summary is
insufficient. To hydrate, read exactly `byte_range[0]` through
`byte_range[1]` from `content_ref`. Never read the whole file.

## 3. Missing context

If no node matches a rule you need:
- Do NOT invent a rule. Do NOT search the web to fill the gap.
- Record the gap explicitly in your final report under `doc_gap_detected`.
- The human operator will convert the gap into a new node in
  `.context/graph.json` on the next build.

## 4. Human audit surface

Every node you receive has an anchor in the offline wiki at:
`wiki/index.html#<node_id>`

Cite that anchor when reporting conclusions. The wiki is the human audit
surface; it is generated from the same graph, not maintained separately.
Do NOT edit `wiki/index.html` or `.context/manifest.json` — they are
build artifacts. To change knowledge, edit `docs/` and `.context/graph.json`,
then run `python3 seed.py && python3 build.py`.

## 5. Token budget

- Instructions and routing: 15% of window
- Task execution: 70%
- Verification reserve: 15%
- If a node's `bytes` exceeds 20% of your remaining budget, read its
  `summary` first and ask for authorization before hydrating.

## 6. Build commands (do not run unless asked)

```
python3 seed.py     # docs/ → graph.json (idempotent, preserves valid edges)
python3 build.py    # graph.json → manifest.json + wiki/index.html
```

## 7. What lives where

| Path | Purpose |
|---|---|
| `.context/graph.json` | Canonical DAG — source of truth |
| `.context/manifest.json` | Generated routing table (read this) |
| `.context/index.md` | Plain-file fallback index |
| `docs/` | Existing documentation — read via byte ranges only |
| `wiki/index.html` | Generated human wiki — do not edit |
| `AGENTS.md` | This file — entry router |

## 8. Non-negotiables

- Never modify files under `docs/` unless the task explicitly says to.
- Never modify `.context/graph.json` unless the task is "add a node/edge".
- Never modify `.context/manifest.json` or `wiki/index.html` — regenerate them.
- Cite `wiki/index.html#<node_id>` for every claim you derive from a node.
```

### 5.4 `CLAUDE.md`

```markdown
@AGENTS.md
```

That is the entire file. It is a Claude Code import shim so the same router
is loaded under both `AGENTS.md`-first and `CLAUDE.md`-first harnesses.

---

## 6. Optional: `.context/index.md`

`build.py` does not generate this file; the agent should create it as a
last-resort fallback for environments where JSON is inconvenient:

```markdown
# Context Index (fallback)

If `.context/manifest.json` is unavailable, use this index. For each entry,
read the declared byte range from `content_ref`.

<!-- generated-by: manual; refresh after each build -->

## Nodes

- `docs/README.md::project-documentation` — docs/README.md — summary: "Project Documentation"
```

For projects with many nodes, regenerate this file after each build with a
small one-liner instead of hand-maintaining it:

```bash
python3 -c "
import json
m = json.load(open('.context/manifest.json'))
print('# Context Index (fallback)\n')
for n in m['nodes']:
    print(f\"- \`{n['id']}\` — \`{n['content_ref']}\` — {n['summary']}\")
" > .context/index.md
```

---

## 7. Seeding edges (the DAG is not a file tree)

`seed.py` produces nodes but no edges — every section is an island. Edges
are what turn the island set into a DAG, and they must be **authored**,
not inferred from directory structure. After the first build, the human
operator (or an agent explicitly authorized to edit the graph) adds edges
to `.context/graph.json` using this decision rule:

| If section A... | Then add edge |
|---|---|
| cannot be implemented without reading B | `A --requires--> B` |
| is a more specific case of B | `A --specializes--> B` |
| replaces an earlier B | `A --supersedes--> B` |
| describes code that implements B | `A --implements--> B` |
| states a rule B contradicts | `A --contradicts--> B` |

Then re-run `python3 build.py`. A graph with zero edges is a valid
bootstrap state but does **not** deliver the token savings — the agent
receives the correct node set only when edges exist to transitively close
over.

**Guidance for the agent during bootstrap:** propose edges as a diff to
`graph.json`, but do not commit them. Report the proposed edges in the final
response. Human approval is required before they are merged — see
Section 8, invariant 6.

---

## 8. Invariants

`build.py` and the validation script in Section 3 enforce the mechanical
ones. The rest are protocol invariants the agent must uphold.

1. **Single source, dual render.** All wiki content and all manifest entries
   derive from `.context/graph.json`. No content exists only in one surface.
2. **DAG acyclicity is a build failure.** Cycles abort the build; they are
   never warned and continued.
3. **Deterministic build.** The same `graph.json` and the same `docs/` bytes
   produce the same `manifest.json` and `wiki/index.html`, byte-for-byte.
4. **Section-level addressing.** Every node has a `byte_range`. Whole-file
   nodes are permitted only when the file has a single heading.
5. **Provenance is hashed.** Every node carries `sha256` of its byte range.
   A reviewer can verify any citation against the source bytes.
6. **Human-gated graph mutation.** Agents may *propose* nodes and edges.
   Only a human commit changes `graph.json` — enforced by process, not by
   the build script.
7. **Artifacts are never hand-edited.** `.context/manifest.json` and
   `wiki/index.html` are regenerated, never patched.
8. **`AGENTS.md` stays under 150 lines.** Its content is recurring
   per-session cost. Move knowledge into nodes, not into the router.
9. **`docs/` is read-only to the build.** The build indexes it; it does not
   rewrite it.
10. **Zero runtime dependencies.** The baselayer builds and serves with
    Python 3 and a browser. Everything else is an *optional layer*.

---

## 9. Extension points (what belongs *above* the baselayer)

Do not build these into the baselayer. When the project needs them, add
them as separate layers that consume `.context/manifest.json`:

| Layer | What it adds | Bound by |
|---|---|---|
| **MCP tool** | `compile_context(target_files)` tool wrapping manifest traversal | Must return the same closure the manifest traversal would |
| **Byte-fetch tool** | `read_section(node_id)` returning exactly `byte_range` | Must return exactly `sha256`-verified bytes |
| **Section indexer** | jDocMunch-style heading-hash index for large `docs/` trees | Must produce the same `byte_range` semantics |
| **Cache-stable assembly** | Fixed-prefix ordering for provider APIs | Must preserve node ids and hashes |
| **Gap observation loop** | Agent writes `doc_gap_detected` events for human triage | Must not auto-commit graph mutations |

Each layer reads the baselayer's output and never writes it. The baselayer
never knows these layers exist. This is the contract that keeps the
foundation stable as the platform grows.

---

## 10. Final agent report format

When you finish building, return exactly this:

```
BASELAYER BUILD COMPLETE
- nodes: <N>
- edges: <M>
- wiki: wiki/index.html (<bytes> bytes)
- manifest: .context/manifest.json (<bytes> bytes)
- files created: <list>
- files modified: <list>  (should be empty unless docs/ was non-empty)
- proposed edges: <list of {from, to, type} or "none">
- doc gaps: <list or "none">
- validation: PASS | FAIL (<detail>)
```

If any step in Section 3 failed, do not return the success template. Return
the failure, the step number, and the raw error.

---

*End of BASELAYER.md. This file is the root instruction for bootstrapping
the workspace. It is not itself part of the graph; it may be archived after
the build succeeds.*