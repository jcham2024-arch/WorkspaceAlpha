#!/usr/bin/env python3
"""Validate the baselayer (Baselayer.md §3 Step 6).

Run after any docs/, graph, or build change. Also run as the
git pre-commit hook (see .githooks/pre-commit).
"""
import ast, hashlib, json, logging, pathlib, re, sys
from pathlib import Path

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

# --- Navigator and tooling structure checks ---
# Importable functions so they can be unit-tested against fixtures
# (tests/test_validate_checks.py) as well as run by this script.

NAV_PATH = ROOT / ".agent" / "tools" / "stair_navigator.py"


def check_navigator_loop_constructs(nav_path=None) -> list[str]:
    """Fail if stair_navigator.py has a while loop anywhere in the module."""
    path = nav_path or NAV_PATH
    if not path.exists():
        return [f"missing: {path}"]
    violations = []
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError as exc:
        return [f"{path}: syntax error: {exc}"]
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "navigate":
            for inner in ast.walk(node):
                if isinstance(inner, ast.While):
                    violations.append(
                        f"{path}: while loop in navigate() — prediction must be "
                        f"single-shot, see FIX_STAIR_LOOP.md §1"
                    )
    return violations


def check_navigator_dispatch_path(nav_path=None) -> list[str]:
    """Fail if an inline dispatch call or a second prediction attempt appears.

    Keyword-fallback detection uses the two precise patterns from
    FIX_STAIR_LOOP.md Part IV rather than a loose 'keyword' + 'fallback' pair,
    so a docstring mentioning the word 'fallback' does not trip the gate.
    """
    path = nav_path or NAV_PATH
    if not path.exists():
        return []
    src = path.read_text(encoding="utf-8")
    violations = []
    if "dispatcher.dispatch" in src:
        violations.append(
            f"{path}: inline dispatcher.dispatch() present — route through the "
            f"dispatch module only, see FIX_STAIR_LOOP.md Part IV"
        )
    for pattern, label in (
        ("query_lower", "keyword fallback (query_lower present)"),
        ("query.lower()", "keyword fallback (query.lower() present)"),
    ):
        if pattern in src:
            violations.append(
                f"{path}: {label} — second prediction attempt, "
                f"see FIX_STAIR_LOOP.md §1"
            )
    if "def _dispatch_llm" in src:
        violations.append(
            f"{path}: _dispatch_llm defined inline — dispatch belongs in "
            f"adapters/, see FIX_STAIR_LOOP.md §1"
        )
    if "except Exception" in src or re.search(r"^\s*except\s*:\s*$", src, re.M):
        violations.append(
            f"{path}: bare or broad except — fail specific, "
            f"see FIX_STAIR_LOOP.md §9"
        )
    if "adapters.navigator" not in src:
        violations.append(
            f"{path}: must import dispatch from adapters.navigator"
        )
    return violations


LINE_COUNT_LIMITS = {
    "assembly/*.py": 200,
    ".agent/tools/*.py": 200,
    ".agent/tools/mcp/*.py": 200,
}
LINE_COUNT_WAIVER = "wa:allow-long-file"


def check_line_counts() -> list[str]:
    """Fail if any tooling file exceeds its limit without a waiver."""
    violations = []
    for pattern, limit in LINE_COUNT_LIMITS.items():
        for path in sorted(ROOT.glob(pattern)):
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            if LINE_COUNT_WAIVER in text[:200]:
                continue
            count = len(text.splitlines())
            if count > limit:
                violations.append(
                    f"{path.relative_to(ROOT)}: {count} lines exceeds "
                    f"{limit}-line limit. Split per CLEANUP_DIRECTIVE.md, or "
                    f"add '{LINE_COUNT_WAIVER}' to the first 200 characters."
                )
    return violations


def check_graph_manifest_coherence(graph_path=None, manifest_path=None) -> list[str]:
    """Fail if graph.json and manifest.json disagree on node IDs."""
    gpath = graph_path or ROOT / ".context" / "graph.json"
    mpath = manifest_path or ROOT / ".context" / "manifest.json"
    violations = []
    g = json.loads(Path(gpath).read_text(encoding="utf-8"))
    mj = json.loads(Path(mpath).read_text(encoding="utf-8"))
    g_nodes = {n["id"] for n in (g.get("nodes") or [])}
    m_nodes = {n["id"] for n in (mj.get("nodes") or [])}
    for missing in sorted(g_nodes - m_nodes):
        violations.append(
            f"node {missing} in graph.json but not manifest.json — run build.py"
        )
    for stale in sorted(m_nodes - g_nodes):
        violations.append(
            f"node {stale} in manifest.json but not graph.json — regenerate"
        )
    return violations


def check_navigator_size(max_lines=100) -> list[str]:
    """The navigator must stay small enough to read in one screen."""
    if not NAV_PATH.exists():
        return []
    count = len(NAV_PATH.read_text(encoding="utf-8").splitlines())
    if count >= max_lines:
        return [
            f"{NAV_PATH.relative_to(ROOT)} is {count} lines, must be under "
            f"{max_lines}"
        ]
    return []


for v in check_navigator_loop_constructs():
    fail(v)
for v in check_navigator_dispatch_path():
    fail(v)
for v in check_navigator_size():
    fail(v)
for v in check_graph_manifest_coherence():
    fail(v)

print("PASS")
budget = sum(n.get("est_tokens", 0) for n in m["nodes"])
log.info("validation passed: nodes=%d, edges=%d, wiki_bytes=%d, agents_lines=%d, router_tokens=%d",
         len(m['nodes']), len(m.get('edges', [])), len(wiki), len(lines), budget)
print(f"  nodes: {len(m['nodes'])}, edges: {len(m.get('edges', []))}")
print(f"  wiki bytes: {len(wiki)}, AGENTS.md lines: {len(lines)}")
print(f"  est. router tokens: {budget}")
