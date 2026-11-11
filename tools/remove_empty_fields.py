#!/usr/bin/env python3
"""Remove empty fields from skill frontmatter.

Skills may have fields like `tags: ` or `tools: ` with no value,
or `source_url: ""` etc. These are unnecessary and waste tokens.
This script removes fields that have empty or whitespace-only values.

Usage:
  python3 tools/remove_empty_fields.py           # report only
  python3 tools/remove_empty_fields.py --fix     # apply changes
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / ".agent" / "skills"

FIELD_RE = re.compile(r"^([a-z_][a-z0-9_]*)\s*:\s*(.*)$")


def fix_skill(text: str):
    """Remove empty fields from frontmatter."""
    changes = []

    if not text.startswith("---\n"):
        return text, changes

    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return text, changes

    fm = parts[0][4:]  # strip opening ---
    body = parts[1]

    fm_lines = fm.split("\n")
    new_fm_lines = []
    removed = []

    for line in fm_lines:
        m = FIELD_RE.match(line.strip())
        if m:
            key, val = m.group(1), m.group(2).strip()
            # Remove if value is empty or just quotes
            if val == "" or val == '""' or val == "''":
                removed.append(key)
                continue
        new_fm_lines.append(line)

    if removed:
        new_fm = "\n".join(new_fm_lines)
        new_text = f"---\n{new_fm}\n---{body}"
        changes.append(f"removed empty fields: {', '.join(removed)}")
        return new_text, changes

    return text, changes


def main():
    ap = argparse.ArgumentParser(description="Remove empty frontmatter fields from skills")
    ap.add_argument("--fix", action="store_true", help="Apply changes to files")
    ap.add_argument("--limit", type=int, default=0, help="Process only N skills (0 = all)")
    args = ap.parse_args()

    total = 0
    changed = 0
    total_removed = 0

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name == "_quarantine":
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        total += 1
        if args.limit and total > args.limit:
            break

        text = skill_file.read_text(encoding="utf-8", errors="replace")
        new_text, changes = fix_skill(text)

        if changes:
            changed += 1
            total_removed += len(changes)
            print(f"  {skill_dir.name}: {', '.join(changes)}")
            if args.fix:
                skill_file.write_text(new_text, encoding="utf-8")

    print(f"\nTotal skills scanned: {total}")
    print(f"Skills with empty fields removed: {changed}")
    print(f"Total empty fields removed: {total_removed}")
    if not args.fix:
        print("Run with --fix to apply changes.")


if __name__ == "__main__":
    main()
