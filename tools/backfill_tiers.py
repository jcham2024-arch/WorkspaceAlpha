#!/usr/bin/env python3
"""Backfill `tier:` field into every skill's SKILL.md frontmatter.

All skills use the pattern: `---\n---\n<yaml fields>\n---\n<body>`
where the frontmatter is empty and YAML fields appear in the body.

This script moves `tier:` into the frontmatter block.

Usage: python3 tools/backfill_tiers.py
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agent" / "skills"
QUARANTINE = ROOT / ".agent" / "quarantine" / "registry.json"
STARTER = ROOT / ".agent" / "profiles" / "starter.md"

VALID_TIERS = {"core", "curated", "experimental", "quarantine"}


def load_quarantined() -> set[str]:
    if not QUARANTINE.exists():
        return set()
    data = json.loads(QUARANTINE.read_text(encoding="utf-8"))
    return {e["id"] for e in data.get("quarantined", [])}


def load_starter_skills() -> set[str]:
    if not STARTER.exists():
        return set()
    text = STARTER.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return set()
    fm = text.split("\n---", 1)[0]
    names, in_skills = [], False
    for line in fm.splitlines():
        if line.startswith("skills:"):
            in_skills = True
            continue
        if in_skills:
            if line.startswith("  - "):
                names.append(line.strip("- ").strip())
            elif line.strip() == "":
                continue
            else:
                break
    return set(names)


def extract_tier_from_body(text: str) -> str | None:
    """Look for tier: in the body (after empty frontmatter)."""
    for line in text.splitlines():
        if line.startswith("tier:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return None


def main():
    quarantined = load_quarantined()
    starter = load_starter_skills()

    changed = 0
    already = 0
    for skill_dir in sorted(SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        skill_id = skill_dir.name
        text = skill_file.read_text(encoding="utf-8")

        # Determine desired tier
        if skill_id in quarantined:
            tier = "quarantine"
        elif skill_id in starter:
            tier = "core"
        else:
            existing = extract_tier_from_body(text)
            if existing:
                tier = existing
                if tier not in VALID_TIERS:
                    tier = "experimental"
            else:
                tier = "experimental"

        # Normalize
        if tier == "STANDARD":
            tier = "curated"

        # Check if frontmatter already has tier
        if text.startswith("---\n---\n"):
            # Empty frontmatter: insert tier between the --- markers
            new_text = f"---\ntier: \"{tier}\"\n---\n" + text[len("---\n---\n"):]
            skill_file.write_text(new_text, encoding="utf-8")
            changed += 1
        elif text.startswith("---\n"):
            # Has frontmatter; check if tier already there
            fm = text.split("\n---", 1)[0]
            has_tier = any(l.startswith("tier:") for l in fm.splitlines())
            if not has_tier:
                # Insert tier after opening ---
                lines = text.split("\n")
                # lines[0] = "---", find insertion point
                insert_idx = 1
                new_lines = lines[:insert_idx] + [f'tier: "{tier}"'] + lines[insert_idx:]
                new_text = "\n".join(new_lines)
                skill_file.write_text(new_text, encoding="utf-8")
                changed += 1
            else:
                already += 1
        else:
            already += 1

    print(f"Backfill complete: {changed} changed, {already} already correct")


if __name__ == "__main__":
    main()
