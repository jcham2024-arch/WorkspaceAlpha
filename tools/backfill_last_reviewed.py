#!/usr/bin/env python3
"""Backfill `last_reviewed:` field into every skill's SKILL.md frontmatter.

All skills now have frontmatter like: `---\ntier: "core"\n---`
This script adds `last_reviewed: 2026-11-10` after tier.

Idempotent: re-running is safe.

Usage: python3 tools/backfill_last_reviewed.py
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agent" / "skills"
REVIEW_DATE = "2026-11-10"


def main():
    changed = 0
    already = 0
    for skill_dir in sorted(SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        text = skill_file.read_text(encoding="utf-8")

        if not text.startswith("---\n"):
            already += 1
            continue

        # Split frontmatter from rest
        parts = text.split("\n---", 1)
        if len(parts) < 2:
            already += 1
            continue

        fm = parts[0]  # everything after first --- but before second ---
        rest = parts[1]  # everything after second ---

        # Check if last_reviewed already in frontmatter
        if "last_reviewed:" in fm:
            already += 1
            continue

        # Insert last_reviewed after tier line
        fm_lines = fm.splitlines()
        new_fm_lines = []
        inserted = False
        for line in fm_lines:
            new_fm_lines.append(line)
            if line.startswith("tier:") and not inserted:
                new_fm_lines.append(f"last_reviewed: {REVIEW_DATE}")
                inserted = True
        if not inserted:
            new_fm_lines.append(f"last_reviewed: {REVIEW_DATE}")

        new_fm = "\n".join(new_fm_lines)
        new_text = f"{new_fm}\n---{rest}"
        skill_file.write_text(new_text, encoding="utf-8")
        changed += 1

    print(f"last_reviewed backfill complete: {changed} changed, {already} already correct")


if __name__ == "__main__":
    main()
