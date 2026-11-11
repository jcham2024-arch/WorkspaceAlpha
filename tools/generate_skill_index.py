#!/usr/bin/env python3
"""Generate skill documentation index from frontmatter.

Reads all SKILL.md files in .agent/skills/ and produces a comprehensive
documentation index organized by category and tier. The index includes:
- Skill name, description, tier, risk, category
- Associated scripts, references, and other files
- Source provenance (license, source_repo, source_type)
- Owner and last_reviewed dates

Output: docs/skills/SKILL_INDEX.md - a searchable reference index
that agents can use to find skills without reading individual files.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / ".agent" / "skills"
OUTPUT_DIR = ROOT / "docs" / "skills"
OUTPUT_FILE = OUTPUT_DIR / "SKILL_INDEX.md"

FIELD_RE = re.compile(r"^([a-z_][a-z0-9_]*)\s*:\s*(.*)$")
LIST_ITEM_RE = re.compile(r"^\s*-\s+(.+)$")


def parse_frontmatter(text: str):
    """Parse frontmatter from SKILL.md text. Returns (fields_dict, body_text)."""
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return {}, text
    fm = parts[0][4:]
    body = parts[1]
    fields = {}
    list_field = None
    list_items = []

    def flush():
        nonlocal list_field, list_items
        if list_field is not None:
            fields[list_field] = list_items
            list_field = None
            list_items = []

    for line in fm.splitlines():
        stripped = line.strip()
        m = FIELD_RE.match(stripped)
        if m:
            flush()
            key, val = m.group(1), m.group(2).strip()
            if val == "":
                list_field = key
                list_items = []
            else:
                fields[key] = val
        elif list_field is not None:
            lm = LIST_ITEM_RE.match(line)
            if lm:
                list_items.append(lm.group(1).strip())
            else:
                flush()
        else:
            break  # end of frontmatter fields
    flush()
    return fields, body


def get_skill_files(skill_dir: Path):
    """Get associated files for a skill."""
    scripts = []
    references = []
    other = []

    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists() and scripts_dir.is_dir():
        scripts = sorted(f.name for f in scripts_dir.iterdir() if f.is_file())

    refs_dir = skill_dir / "references"
    if refs_dir.exists() and refs_dir.is_dir():
        references = sorted(f.name for f in refs_dir.iterdir() if f.is_file())

    for f in sorted(skill_dir.iterdir()):
        if f.name in ("SKILL.md", "scripts", "references", "LICENSE"):
            continue
        if f.is_file():
            other.append(f.name)

    return scripts, references, other


def generate_index(skills: list[dict]):
    """Generate the skill index markdown document."""
    lines = []

    lines.append("# Skill Index")
    lines.append("")
    lines.append("Auto-generated from skill frontmatter. Do not edit by hand.")
    lines.append("")
    lines.append(f"Total skills: {len(skills)}")
    lines.append("")

    # Summary by tier
    tier_counts = defaultdict(int)
    for s in skills:
        tier_counts[s.get("tier", "unknown")] += 1

    lines.append("## By Tier")
    lines.append("")
    for tier in sorted(tier_counts):
        lines.append(f"- **{tier}**: {tier_counts[tier]} skills")
    lines.append("")

    # Summary by category
    cat_counts = defaultdict(int)
    for s in skills:
        cat = s.get("category", "uncategorized")
        cat_counts[cat] += 1

    lines.append("## By Category")
    lines.append("")
    for cat in sorted(cat_counts, key=lambda c: -cat_counts[c]):
        lines.append(f"- **{cat}**: {cat_counts[cat]} skills")
    lines.append("")

    # Summary by risk
    risk_counts = defaultdict(int)
    for s in skills:
        risk_counts[s.get("risk", "unknown")] += 1

    lines.append("## By Risk Level")
    lines.append("")
    for risk in sorted(risk_counts):
        lines.append(f"- **{risk}**: {risk_counts[risk]} skills")
    lines.append("")

    # Detailed listing grouped by category, then tier
    lines.append("## Skill Details")
    lines.append("")

    # Group by category
    by_category = defaultdict(list)
    for s in skills:
        cat = s.get("category", "uncategorized")
        by_category[cat].append(s)

    for cat in sorted(by_category):
        skills_in_cat = sorted(by_category[cat], key=lambda s: s.get("name", ""))
        lines.append(f"### {cat.title()} ({len(skills_in_cat)})")
        lines.append("")

        # Sub-group by tier within category
        by_tier = defaultdict(list)
        for s in skills_in_cat:
            by_tier[s.get("tier", "unknown")].append(s)

        for tier in sorted(by_tier):
            lines.append(f"#### {tier.title()}")
            lines.append("")
            for s in sorted(by_tier[tier], key=lambda s: s.get("name", "")):
                name = s.get("name", "unknown")
                desc = s.get("description", "No description")
                risk = s.get("risk", "unknown")
                owner = s.get("owner", "unknown")
                source_repo = s.get("source_repo", "")
                upstream_license = s.get("upstream_license", "unknown")
                last_reviewed = s.get("last_reviewed", "unknown")

                lines.append(f"##### {name}")
                lines.append("")
                lines.append(f"- **Description**: {desc}")
                lines.append(f"- **Tier**: {tier} | **Risk**: {risk} | **Owner**: {owner}")
                lines.append(f"- **Last Reviewed**: {last_reviewed} | **License**: {upstream_license}")
                if source_repo:
                    lines.append(f"- **Source**: {source_repo}")
                if s.get("source_type"):
                    lines.append(f"- **Source Type**: {s['source_type']}")
                if s.get("tags"):
                    tags = s["tags"] if isinstance(s["tags"], list) else [s["tags"]]
                    lines.append(f"- **Tags**: {', '.join(tags)}")
                if s.get("tools"):
                    tools = s["tools"] if isinstance(s["tools"], list) else [s["tools"]]
                    lines.append(f"- **Tools**: {', '.join(tools)}")
                lines.append("")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*Generated by tools/generate_skill_index.py from skill frontmatter.*")
    lines.append("*Run with --fix to regenerate.*")

    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Generate skill documentation index")
    ap.add_argument("--fix", action="store_true", help="Write the index file")
    args = ap.parse_args()

    skills = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name == "_quarantine":
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        text = skill_file.read_text(encoding="utf-8", errors="replace")
        fields, body = parse_frontmatter(text)

        scripts, references, other = get_skill_files(skill_dir)

        skill_info = {
            "name": skill_dir.name,
            "path": str(skill_dir.relative_to(ROOT)),
            "fields": fields,
            "scripts": scripts,
            "references": references,
            "other_files": other,
        }
        skills.append(skill_info)

    # Flatten fields into top-level for template
    for s in skills:
        for k, v in s["fields"].items():
            s[k] = v
        s["scripts"] = s["scripts"]
        s["references"] = s["references"]
        s["other_files"] = s["other_files"]

    index_md = generate_index(skills)

    if args.fix:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_FILE.write_text(index_md, encoding="utf-8")
        print(f"Wrote skill index to {OUTPUT_FILE} ({len(skills)} skills)")
    else:
        print(index_md[:5000])
        print(f"\n... (truncated, {len(skills)} skills total)")
        print("Run with --fix to write the full index.")


if __name__ == "__main__":
    main()
