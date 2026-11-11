#!/usr/bin/env python3
"""Fix quoting issues in skill frontmatter.

Some skills have values like `description: ""Usar al iniciar...` where
the original quotes were preserved and then the value was re-quoted.
This script strips outer quotes from scalar values and re-quotes only
when necessary (value contains :, #, or starts with [ or {).

Usage:
  python3 tools/fix_quoting.py           # report only
  python3 tools/fix_quoting.py --fix     # apply changes
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / ".agent" / "skills"

FIELD_RE = re.compile(r"^([a-z_][a-z0-9_]*)\s*:\s*(.*)$")


def strip_outer_quotes(val: str):
    """Strip matching outer quotes from a value."""
    if len(val) >= 2:
        if (val.startswith('"') and val.endswith('"')) or \
           (val.startswith("'") and val.endswith("'")):
            return val[1:-1]
    return val


def needs_quoting(val: str):
    """Check if a value needs quoting in YAML."""
    return ":" in val or "#" in val or val.startswith("[") or val.startswith("{") or val.startswith("'") or val.startswith('"')


def format_value(val: str):
    """Format a value for YAML output."""
    if needs_quoting(val):
        return f'"{val}"'
    return val


def fix_skill(text: str):
    """Fix quoting in frontmatter."""
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
    fixed = False

    for line in fm_lines:
        m = FIELD_RE.match(line.strip())
        if m:
            key, val = m.group(1), m.group(2).strip()
            # Strip outer quotes
            stripped = strip_outer_quotes(val)
            if stripped != val:
                fixed = True
            # Re-quote only if necessary
            new_val = format_value(stripped)
            if new_val != val:
                fixed = True
            new_fm_lines.append(f"{key}: {new_val}")
        else:
            new_fm_lines.append(line)

    if fixed:
        new_fm = "\n".join(new_fm_lines)
        new_text = f"---\n{new_fm}\n---{body}"
        changes.append("fixed quoting")
        return new_text, changes

    return text, changes


def main():
    ap = argparse.ArgumentParser(description="Fix quoting issues in skill frontmatter")
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

        text = skill_file.read_text(encoding="utf-8", errors="replace")
        new_text, changes = fix_skill(text)

        if changes:
            changed += 1
            print(f"  {skill_dir.name}: {', '.join(changes)}")
            if args.fix:
                skill_file.write_text(new_text, encoding="utf-8")

    print(f"\nTotal skills scanned: {total}")
    print(f"Skills with quoting issues: {changed}")
    if not args.fix:
        print("Run with --fix to apply changes.")


if __name__ == "__main__":
    main()
