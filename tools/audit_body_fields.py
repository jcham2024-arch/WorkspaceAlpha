#!/usr/bin/env python3
"""Secondary skill audit: detect skills with name/description in the body.

The standard audit.py checks frontmatter (between the first two --- markers)
for name/description. Some imported skills have empty frontmatter
(---\n---\n) with name/description fields appearing in the body after the
second --- marker. This script identifies those skills and can optionally
promote the fields into frontmatter so audit.py passes.

Usage:
  python3 tools/audit_body_fields.py          # report only
  python3 tools/audit_body_fields.py --fix    # promote name/description to frontmatter

Exit code 1 if any skills have body-located name/description.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / ".agent" / "skills"


def split_skill(text: str):
    """Split a SKILL.md into (frontmatter_lines, body_lines).

    Returns (fm_text, body_text) where fm_text is everything between the
    first two --- markers (empty if no frontmatter), and body_text is
    everything after the second --- marker.
    """
    if not text.startswith("---\n"):
        return "", text
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return "", text
    fm = parts[0][4:]  # strip leading "---\n"
    rest = parts[1]    # starts with "\n" then body
    return fm, rest


def extract_field(text: str, field: str) -> str | None:
    """Extract a YAML scalar field value from text."""
    for line in text.splitlines():
        m = re.match(rf"^{re.escape(field)}:\s*(.+)$", line.strip())
        if m:
            return m.group(1).strip().strip('"').strip("'")
    return None


def main():
    ap = argparse.ArgumentParser(
        description="Audit skills with name/description in body (not frontmatter)"
    )
    ap.add_argument(
        "--fix",
        action="store_true",
        help="Promote name/description from body into frontmatter",
    )
    args = ap.parse_args()

    affected = []
    fixed = 0

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name == "_quarantine":
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        text = skill_file.read_text(encoding="utf-8", errors="replace")
        fm, body = split_skill(text)

        fm_name = extract_field(fm, "name")
        fm_desc = extract_field(fm, "description")
        body_name = extract_field(body, "name")
        body_desc = extract_field(body, "description")

        has_body_name = body_name is not None
        has_body_desc = body_desc is not None

        if not has_body_name and not has_body_desc:
            continue

        affected.append(skill_dir.name)

        if args.fix:
            new_lines = []
            # Build new frontmatter: existing fm + promoted fields
            existing_fields = set()
            for line in fm.splitlines():
                new_lines.append(line)
                m = re.match(r"^([a-z_]+):", line.strip())
                if m:
                    existing_fields.add(m.group(1))

            if has_body_name and "name" not in existing_fields:
                new_lines.append(f'name: "{body_name}"')
                existing_fields.add("name")
            if has_body_desc and "description" not in existing_fields:
                new_lines.append(f'description: "{body_desc}"')

            new_fm = "\n".join(new_lines)
            new_text = f"---\n{new_fm}\n---{body}"
            skill_file.write_text(new_text, encoding="utf-8")
            fixed += 1
            log_detail = "FIXED"
        else:
            log_detail = "report"

        print(f"  {skill_dir.name}: name_in_body={has_body_name}, "
              f"description_in_body={has_body_desc} [{log_detail}]")

    print(f"\nAffected skills: {len(affected)}")
    if args.fix:
        print(f"Fixed: {fixed}")
    else:
        print("Use --fix to promote name/description into frontmatter.")

    if affected:
        sys.exit(1)


if __name__ == "__main__":
    main()
