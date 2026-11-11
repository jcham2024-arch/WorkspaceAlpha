#!/usr/bin/env python3
"""Backfill `owner:` field into every skill's SKILL.md frontmatter.

Default owner: "taskmaster" (owns the skill library).
Idempotent: re-running is safe.

Usage: python3 tools/backfill_owner.py
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agent" / "skills"
PROFILES = ROOT / ".agent" / "profiles"
DEFAULT_OWNER = "taskmaster"


def parse_frontmatter(text: str) -> tuple[dict, str, str]:
    if not text.startswith("---\n"):
        return {}, "", text
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return {}, "", text
    header = parts[0][4:]
    rest = parts[1]
    fields = {}
    for line in header.splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, _, v = line.partition(":")
            fields[k.strip()] = v.strip().strip('"').strip("'")
    return fields, header, rest


def add_field_to_frontmatter(text: str, field: str, value: str) -> str:
    fields, header, rest = parse_frontmatter(text)
    if field in fields:
        return text  # already present
    lines = header.splitlines()
    lines.append(f'{field}: "{value}"')
    new_header = "\n".join(lines)
    return f"---\n{new_header}\n---{rest}"


def main():
    # Skills
    changed = 0
    already = 0
    for skill_dir in sorted(SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        text = skill_file.read_text(encoding="utf-8", errors="replace")
        new_text = add_field_to_frontmatter(text, "owner", DEFAULT_OWNER)
        if new_text != text:
            skill_file.write_text(new_text, encoding="utf-8")
            changed += 1
        else:
            already += 1

    print(f"Skills: {changed} added owner, {already} already had it")

    # Profiles
    p_changed = 0
    p_already = 0
    profile_owners = {
        "conceptualizer": "conceptualizer",
        "taskmaster": "taskmaster",
        "coder": "coder",
        "researcher": "researcher",
        "reviewer": "reviewer",
        "coding-manager": "coding-manager",
        "research-manager": "research-manager",
        "review-manager": "review-manager",
        "wiki-producer": "wiki-producer",
        "starter": "taskmaster",
    }

    for profile_file in sorted(PROFILES.glob("*.md")):
        profile_name = profile_file.stem
        owner = profile_owners.get(profile_name, "taskmaster")
        text = profile_file.read_text(encoding="utf-8", errors="replace")
        new_text = add_field_to_frontmatter(text, "owner", owner)
        if new_text != text:
            profile_file.write_text(new_text, encoding="utf-8")
            p_changed += 1
        else:
            p_already += 1

    print(f"Profiles: {p_changed} added owner, {p_already} already had it")


if __name__ == "__main__":
    main()
