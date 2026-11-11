#!/usr/bin/env python3
"""Generate the agent registry (.agent/agents.json) from profiles.

The registry is the factory's machine-readable index: every role
with its skills, tools, tools allowlist, stage, and model tier.
Agents are discovered from here, not by parsing markdown.

  .agent/agents.json
    { "agent": "coder",
      "role": "...", "stage": "03-execute",
      "model_tier": "...", "skills": [...], "tools": [...],
      "mcp_allowlist": [...], "profile_file": "profiles/coder.md" }
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
PROFILES = ROOT / ".agent" / "profiles"
MCP = ROOT / ".agent" / "tools" / "mcp" / "mcp.json"
OUT = ROOT / ".agent" / "agents.json"
VERSION_FILE = ROOT / ".agent" / "models.json"  # carries factory version

MODELS = json.loads((ROOT / ".agent" / "models.json").read_text(encoding="utf-8"))["tiers"]
ALLOW = json.loads(MCP.read_text(encoding="utf-8")).get("allowlist_by_profile", {})

def parse_frontmatter(path: pathlib.Path):
    text = path.read_text(encoding="utf-8")
    fm = text.split("\n---", 1)[0]
    out, in_skills, in_tools = {}, False, False
    for line in fm.splitlines():
        if line.startswith("skills:"):
            in_skills, in_tools = True, False
            continue
        if line.startswith("tools:"):
            in_tools, in_skills = True, False
            continue
        if line.startswith(("role:", "stage:", "model-tier:", "name:")):
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
            in_skills = in_tools = False
            continue
        if in_skills and line.startswith("  - "):
            out.setdefault("skills", []).append(line.strip("- ").strip())
        if in_tools and line.startswith("  - "):
            out.setdefault("tools", []).append(line.strip("- ").strip())
    return out

def main():
    version = "0.1.0"
    try:
        version = json.loads(VERSION_FILE.read_text(encoding="utf-8")).get("version", version)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    agents = []
    for p in sorted(PROFILES.glob("*.md")):
        if p.name in ("README.md", "TEMPLATE.md") or p.stem == "protocol" or p.stem == "eval-agents":
            continue
        fm = parse_frontmatter(p)
        tier = fm.get("model-tier", "")
        tier_key = next((k for k in MODELS if k in tier), "")
        agents.append({
            "agent": p.stem,
            "profile_file": f"profiles/{p.name}",
            "role": fm.get("role", ""),
            "stage": fm.get("stage", ""),
            "model_tier": tier,
            "model_suggestion": MODELS.get(tier_key, {}).get("model", "unspecified"),
            "skills": fm.get("skills", []),
            "tools": fm.get("tools", []),
            "mcp_allowlist": ALLOW.get(p.stem, []),
        })
    OUT.write_text(json.dumps({"version": 1, "factory_version": version, "agents": agents}, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(f"wrote {OUT} ({len(agents)} agents)")
    for a in agents:
        print(f"  {a['agent']}: {len(a['skills'])} skills, tier={a['model_tier']!r}")

if __name__ == "__main__":
    main()
