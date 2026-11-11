#!/usr/bin/env python3
"""Detect duplicate and overlapping skills by discipline.

Uses name-prefix blocking to avoid O(n²) comparison. Compares skills
with similar names within the same category to find duplicates.

Usage:
  python3 tools/find_duplicate_skills.py           # report only
"""
from __future__ import annotations

import argparse
import difflib
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / ".agent" / "skills"

FIELD_RE = re.compile(r"^([a-z_][a-z0-9_]*)\s*:\s*(.*)$")
LIST_ITEM_RE = re.compile(r"^\s*-\s+(.+)$")


def parse_frontmatter(text: str):
    """Parse frontmatter from SKILL.md text."""
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return {}, text
    fm = parts[0][4:]
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
            break
    flush()
    return fields, ""


def normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def description_similarity(desc1: str, desc2: str) -> float:
    n1 = normalize_text(desc1)
    n2 = normalize_text(desc2)
    if not n1 or not n2:
        return 0.0
    return difflib.SequenceMatcher(None, n1, n2).ratio()


def name_similarity(name1: str, name2: str) -> float:
    n1 = normalize_text(name1)
    n2 = normalize_text(name2)
    if not n1 or not n2:
        return 0.0
    return difflib.SequenceMatcher(None, n1, n2).ratio()


def name_prefix(name: str, length: int = 3):
    """Get first `length` alphanumeric characters of name for blocking."""
    n = normalize_text(name)
    return n[:length]


def main():
    ap = argparse.ArgumentParser(description="Find duplicate/overlapping skills")
    ap.add_argument("--desc-threshold", type=float, default=0.75,
                    help="Description similarity threshold")
    ap.add_argument("--name-threshold", type=float, default=0.85,
                    help="Name similarity threshold")
    args = ap.parse_args()

    # Load all skills
    skills = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name == "_quarantine":
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        text = skill_file.read_text(encoding="utf-8", errors="replace")
        fields, _ = parse_frontmatter(text)
        skills.append({
            "name": skill_dir.name,
            "path": str(skill_dir.relative_to(ROOT)),
            "description": fields.get("description", ""),
            "category": fields.get("category", "uncategorized"),
            "tier": fields.get("tier", "unknown"),
            "risk": fields.get("risk", "unknown"),
        })

    print(f"Loaded {len(skills)} skills")
    print()

    # Group by category
    by_category = defaultdict(list)
    for s in skills:
        by_category[s["category"]].append(s)

    duplicate_groups = []
    compared = 0

    # Compare within each category using name-prefix blocking
    for category, cat_skills in sorted(by_category.items()):
        if len(cat_skills) < 2:
            continue

        # Block by name prefix (first 3 chars)
        prefix_groups = defaultdict(list)
        for s in cat_skills:
            prefix_groups[name_prefix(s["name"])].append(s)

        for prefix, group in prefix_groups.items():
            if len(group) < 2:
                continue
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    s1 = group[i]
                    s2 = group[j]
                    compared += 1

                    desc_sim = description_similarity(s1["description"], s2["description"])
                    name_sim = name_similarity(s1["name"], s2["name"])

                    if desc_sim >= args.desc_threshold:
                        duplicate_groups.append({
                            "skill_a": s1["name"],
                            "skill_b": s2["name"],
                            "category": category,
                            "desc_similarity": round(desc_sim, 3),
                            "name_similarity": round(name_sim, 3),
                            "reason": "high description similarity",
                            "a_tier": s1["tier"],
                            "b_tier": s2["tier"],
                            "a_risk": s1["risk"],
                            "b_risk": s2["risk"],
                        })
                    elif name_sim >= args.name_threshold and desc_sim >= 0.4:
                        duplicate_groups.append({
                            "skill_a": s1["name"],
                            "skill_b": s2["name"],
                            "category": category,
                            "desc_similarity": round(desc_sim, 3),
                            "name_similarity": round(name_sim, 3),
                            "reason": "high name similarity + moderate description overlap",
                            "a_tier": s1["tier"],
                            "b_tier": s2["tier"],
                            "a_risk": s1["risk"],
                            "b_risk": s2["risk"],
                        })

    print(f"Compared {compared} skill pairs")
    print(f"Found {len(duplicate_groups)} potential duplicate groups")
    print()

    # Sort by combined similarity
    duplicate_groups.sort(key=lambda g: -(g["desc_similarity"] + g["name_similarity"]) / 2)

    # Group by category for reporting
    by_cat = defaultdict(list)
    for g in duplicate_groups:
        by_cat[g["category"]].append(g)

    total_reported = 0
    for cat in sorted(by_cat):
        groups = by_cat[cat]
        total_reported += len(groups)
        print(f"## {cat.title()} ({len(groups)} potential duplicates)")
        print("")
        for g in groups[:15]:
            print(f"  - {g['skill_a']} <-> {g['skill_b']}")
            print(f"    Desc: {g['desc_similarity']}, Name: {g['name_similarity']} | {g['reason']}")
            print(f"    Tiers: {g['a_tier']}/{g['b_tier']} | Risks: {g['a_risk']}/{g['b_risk']}")
            print("")
        if len(groups) > 15:
            print(f"    ... and {len(groups) - 15} more")
            print("")

    print(f"Total duplicate groups reported: {total_reported}")


if __name__ == "__main__":
    main()
