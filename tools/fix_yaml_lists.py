#!/usr/bin/env python3
"""Fix orphaned YAML list items in skill bodies.

Some skills have list fields (tags:, tools:) with empty values in frontmatter,
and their list items (- item) appear at the start of the body after the frontmatter
separator. This script reattaches those list items to their fields.

Usage:
  python3 tools/fix_yaml_lists.py           # report only
  python3 tools/fix_yaml_lists.py --fix     # apply changes
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / ".agent" / "skills"

LIST_FIELDS = {"tags", "tools"}
FIELD_RE = re.compile(r"^([a-z_][a-z0-9_]*)\s*:\s*(.*)$")
LIST_ITEM_RE = re.compile(r"^\s*-\s+(.+)$")


def fix_skill(text: str):
    """Return (new_text, changes_made)."""
    if not text.startswith("---\n"):
        return text, []

    # Split at the second --- (frontmatter close)
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return text, []

    fm = parts[0]  # everything after first --- but before second ---
    # Strip leading --- if present (opening delimiter)
    if fm.startswith("---\n"):
        fm = fm[4:]
    body = parts[1]

    # Parse frontmatter lines
    fm_lines = fm.split("\n")
    body_lines = body.split("\n")

    # Find list fields with empty values at the end of frontmatter
    # We need to check the last few fields
    list_field_positions = {}  # field_name -> line_index in fm_lines
    for i, line in enumerate(fm_lines):
        m = FIELD_RE.match(line.strip())
        if m:
            key, val = m.group(1), m.group(2).strip()
            if key in LIST_FIELDS and val == "":
                list_field_positions[key] = i

    if not list_field_positions:
        return text, []

    # Check if body starts with YAML list items
    if not body_lines:
        return text, []

    first_body_line = body_lines[0].strip()
    list_match = LIST_ITEM_RE.match(body_lines[0])
    if not list_match:
        return text, []

    # Collect consecutive list items from start of body
    list_items = []
    i = 0
    while i < len(body_lines):
        m = LIST_ITEM_RE.match(body_lines[i])
        if m:
            list_items.append(m.group(1).strip())
            i += 1
        else:
            break

    if not list_items:
        return text, []

    # Find the LAST list field in frontmatter (the one the items belong to)
    # The items belong to the last empty list field before the separator
    last_list_field = None
    last_list_pos = -1
    for key, pos in list_field_positions.items():
        if pos > last_list_pos:
            last_list_pos = pos
            last_list_field = key

    if last_list_field is None:
        return text, []

    # Replace the empty field line with field + list items
    indent = "  "
    new_fm_lines = []
    for j, line in enumerate(fm_lines):
        if j == last_list_pos:
            new_fm_lines.append(f"{last_list_field}:")
            for item in list_items:
                new_fm_lines.append(f"{indent}- {item}")
        else:
            new_fm_lines.append(line)

    new_fm = "\n".join(new_fm_lines)
    # Remove the consumed list items from body
    remaining_body = "\n".join(body_lines[i:])

    new_text = f"---\n{new_fm}\n---{remaining_body}"
    changes = [f"reattached {len(list_items)} items to {last_list_field}"]
    return new_text, changes


def main():
    ap = argparse.ArgumentParser(description="Fix orphaned YAML list items in skills")
    ap.add_argument("--fix", action="store_true", help="Apply changes to files")
    ap.add_argument("--limit", type=int, default=0, help="Process only N skills (0 = all)")
    args = ap.parse_args()

    total = 0
    changed = 0
    total_items = 0

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
            total_items += sum(int(c.split()[1]) for c in changes if c.split()[1].isdigit())
            print(f"  {skill_dir.name}: {', '.join(changes)}")
            if args.fix:
                skill_file.write_text(new_text, encoding="utf-8")

    print(f"\nTotal skills scanned: {total}")
    print(f"Skills with orphaned list items: {changed}")
    print(f"Total list items reattached: {total_items}")
    if not args.fix:
        print("Run with --fix to apply changes.")


if __name__ == "__main__":
    main()
