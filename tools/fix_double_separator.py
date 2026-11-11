#!/usr/bin/env python3
"""Fix double frontmatter separators (---\n---\n) in skill files.

Some skills have ---\n---\n at the start, meaning an empty frontmatter block
followed by another --- delimiter. This collapses them to a single proper
frontmatter block.

Usage:
  python3 tools/fix_double_separator.py           # report only
  python3 tools/fix_double_separator.py --fix     # apply changes
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / ".agent" / "skills"


def fix_skill(text: str):
    """Fix double separators at start of file."""
    changes = []

    # Pattern: ---\n---\n at the very start means empty opening frontmatter
    # We want: ---\n<actual frontmatter>\n---<body>
    
    if text.startswith("---\n---\n"):
        # Find where the actual content starts after the double separator
        # The content after ---\n---\n should be frontmatter fields then --- then body
        rest = text[len("---\n---\n"):]
        
        # Now rest should be: field1: value1\nfield2: value2\n---<body>
        # OR: field1: value1\n---\n<body> (if there were no fields between)
        
        # Check if rest starts with --- (meaning empty frontmatter between)
        if rest.startswith("---\n"):
            # ---\n---\n---\n<body> -> ---\n<body> (empty frontmatter, just collapse)
            # Find the body after the third ---
            body_start = rest.find("\n", 4)  # after "---\n"
            if body_start >= 0:
                body = rest[body_start + 1:]
            else:
                body = ""
            new_text = f"---\n---\n{body}"
            changes.append("collapsed empty double frontmatter")
            return new_text, changes
        
        # rest starts with field lines, then ---, then body
        # Find the closing ---
        close_idx = rest.find("\n---")
        if close_idx >= 0:
            fm_content = rest[:close_idx]  # field lines
            body = rest[close_idx + 4:]  # after \n---
            new_text = f"---\n{fm_content}\n---{body}"
            changes.append("collapsed double separator into single frontmatter")
            return new_text, changes
    
    return text, changes


def main():
    ap = argparse.ArgumentParser(description="Fix double frontmatter separators")
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
    print(f"Skills with double separators: {changed}")
    if not args.fix:
        print("Run with --fix to apply changes.")


if __name__ == "__main__":
    main()
