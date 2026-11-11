#!/usr/bin/env python3
"""Cleanup script for already-normalized skills.

Fixes issues from the first normalization pass:
  1. Fixes `------` separator (should be `---\n---`)
  2. Re-attaches orphaned YAML list items to their `tags:`/`tools:` fields
  3. Removes duplicate blank lines
  4. Ensures proper frontmatter/body separation

Usage:
  python3 tools/cleanup_skills.py           # report only
  python3 tools/cleanup_skills.py --fix     # apply changes
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / ".agent" / "skills"

# Fields that can have YAML list values
LIST_FIELDS = {"tags", "tools"}

FIELD_RE = re.compile(r"^([a-z_][a-z0-9_]*)\s*:\s*(.*)$")
LIST_ITEM_RE = re.compile(r"^\s*-\s+(.+)$")


def read_skill(path: Path):
    return path.read_text(encoding="utf-8", errors="replace")


def write_skill(path: Path, text: str):
    path.write_text(text, encoding="utf-8")


def cleanup_skill(text: str):
    """Return (new_text, changes_made)."""
    changes = []

    # 1. Fix `------` separator (6+ dashes) -> proper `---` frontmatter close
    # Pattern: ---\n--- at the boundary between frontmatter and body
    # The issue: ---\n--- became ------ when body started with ---
    if "------" in text:
        # Replace 6+ consecutive dashes on a line with just ---
        text = re.sub(r"^-{6,}$", "---", text, flags=re.MULTILINE)
        changes.append("fixed separator dashes")

    # 2. Re-attach orphaned list items to tags/tools fields
    lines = text.split("\n---", 1)
    if len(lines) == 2:
        fm = lines[0]
        body = lines[1]

        # Check if body starts with --- (orphaned closing delimiter)
        if body.startswith("\n---"):
            body = body[4:]  # skip \n---
            changes.append("stripped orphaned closing delimiter")

        # Check for orphaned list items at start of body
        body_lines = body.split("\n")
        new_body_lines = []
        i = 0
        while i < len(body_lines):
            stripped = body_lines[i].strip()
            m = re.match(r"^\s*-\s+(.+)$", body_lines[i])
            if m and i > 0:
                # Check if previous line was a tags: or tools: field with empty value
                prev = body_lines[i - 1].strip()
                prev_m = re.match(r"^(tags|tools):\s*$", prev)
                if prev_m:
                    field_name = prev_m.group(1)
                    # Collect all consecutive list items
                    items = [m.group(1).strip()]
                    j = i + 1
                    while j < len(body_lines):
                        jm = re.match(r"^\s*-\s+(.+)$", body_lines[j])
                        if jm:
                            items.append(jm.group(1).strip())
                            j += 1
                        else:
                            break
                    # Replace the empty field line and skip the list items
                    new_body_lines[-1] = f"{field_name}:\n" + "\n".join(
                        f"  - {item}" for item in items
                    )
                    i = j
                    changes.append(f"reattached {field_name} list ({len(items)} items)")
                    continue
            new_body_lines.append(body_lines[i])
            i += 1
        body = "\n".join(new_body_lines)
        text = lines[0] + "\n---" + body

    # 3. Remove excessive blank lines (3+ -> 2)
    text = re.sub(r"\n{4,}", "\n\n\n", text)

    return text, changes


def main():
    ap = argparse.ArgumentParser(description="Cleanup normalized skill files")
    ap.add_argument("--fix", action="store_true", help="Apply changes to files")
    ap.add_argument("--limit", type=int, default=0, help="Process only N skills (0 = all)")
    args = ap.parse_args()

    total = 0
    changed = 0

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name == "_quarantine":
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        total += 1
        if args.limit and total > args.limit:
            break

        text = read_skill(skill_file)
        new_text, changes = cleanup_skill(text)

        if changes:
            changed += 1
            print(f"  {skill_dir.name}: {', '.join(changes)}")
            if args.fix:
                write_skill(skill_file, new_text)

    print(f"\nTotal skills scanned: {total}")
    print(f"Skills needing cleanup: {changed}")
    if not args.fix:
        print("Run with --fix to apply changes.")


if __name__ == "__main__":
    main()
