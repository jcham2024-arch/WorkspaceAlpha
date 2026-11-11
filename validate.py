#!/usr/bin/env python3
"""Validate the baselayer (Baselayer.md §3 Step 6).

Run after any docs/, graph, or build change. Also run as the
git pre-commit hook (see .githooks/pre-commit).
"""
import hashlib, json, logging, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger("validate")

def fail(m):
    log.error(m)
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
    if s < 0:
        fail(f"byte range start {s} negative on {n['id']}")
    if e <= s:
        fail(f"byte range end {e} <= start {s} on {n['id']}")
    if e > len(src):
        fail(f"byte range end {e} exceeds file size {len(src)} on {n['id']}")
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

# Quarantine check: no quarantined skill may appear in any active profile
QUARANTINE_REG = ROOT / ".agent" / "quarantine" / "registry.json"
PROFILES_DIR = ROOT / ".agent" / "profiles"
if QUARANTINE_REG.exists():
    import json as _json
    qdata = _json.loads(QUARANTINE_REG.read_text(encoding="utf-8"))
    quarantined_ids = {e["id"] for e in qdata.get("quarantined", [])}
    for pf in sorted(PROFILES_DIR.glob("*.md")):
        text = pf.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        fm = text.split("\n---", 1)[0]
        in_skills = False
        for line in fm.splitlines():
            if line.startswith("skills:"):
                in_skills = True
                continue
            if in_skills:
                if line.startswith("  - "):
                    skill_name = line.strip("- ").strip()
                    if skill_name in quarantined_ids:
                        fail(f"quarantined skill '{skill_name}' in profile {pf.name}")
                elif line.strip() == "":
                    continue
                else:
                    break

# Tier validation: every skill has a valid tier field
SKILLS_DIR = ROOT / ".agent" / "skills"
VALID_TIERS = {"core", "curated", "experimental", "quarantine"}
if SKILLS_DIR.exists():
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        text = skill_file.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            fail(f"skill {skill_dir.name}: missing frontmatter")
        fm = text.split("\n---", 1)[0]
        tier = None
        for line in fm.splitlines():
            if line.startswith("tier:"):
                tier = line.split(":", 1)[1].strip().strip('"').strip("'")
                break
        if tier is None:
            fail(f"skill {skill_dir.name}: missing tier field")
        if tier not in VALID_TIERS:
            fail(f"skill {skill_dir.name}: invalid tier '{tier}' (must be one of {sorted(VALID_TIERS)})")

print("PASS")
budget = sum(n.get("est_tokens", 0) for n in m["nodes"])
log.info("validation passed: nodes=%d, edges=%d, wiki_bytes=%d, agents_lines=%d, router_tokens=%d",
         len(m['nodes']), len(m.get('edges', [])), len(wiki), len(lines), budget)
print(f"  nodes: {len(m['nodes'])}, edges: {len(m.get('edges', []))}")
print(f"  wiki bytes: {len(wiki)}, AGENTS.md lines: {len(lines)}")
print(f"  est. router tokens: {budget}")
