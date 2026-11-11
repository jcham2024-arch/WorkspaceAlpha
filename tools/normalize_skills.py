#!/usr/bin/env python3
"""Bulk skill normalizer.

For every SKILL.md in .agent/skills/:
  1. Splits into frontmatter (between first two ---) and body (after second ---)
  2. Extracts YAML fields (scalars and lists) from the start of the body
  3. Promotes any body field not already in frontmatter into frontmatter
  4. Removes promoted field lines and their list items from the body
  5. Strips the original closing --- delimiter from body start
  6. Leaves actual skill content (instructions, examples, etc.) untouched

Usage:
  python3 tools/normalize_skills.py           # report only
  python3 tools/normalize_skills.py --fix     # apply changes
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / ".agent" / "skills"

# Fields that are metadata and belong in frontmatter (not body content)
METADATA_FIELDS = {
    "name", "description", "tier", "risk", "source", "date_added",
    "source_type", "source_repo", "category", "author", "license",
    "license_source", "tags", "tools", "compatibility", "version",
    "upstream_commit", "homepage", "role", "phase", "squad", "origin",
    "id", "upstream", "date_updated", "docs", "metadata", "platforms",
    "trigger", "owner", "last_reviewed", "source_url", "source_ref",
    "source_commit", "content_hash", "fetched_at", "upstream_license",
}

FIELD_RE = re.compile(r"^([a-z_][a-z0-9_]*)\s*:\s*(.*)$")
LIST_ITEM_RE = re.compile(r"^\s*-\s+(.+)$")


def split_skill(text: str):
    """Split into (frontmatter_text, body_text)."""
    if not text.startswith("---\n"):
        return "", text
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return "", text
    fm = parts[0][4:]  # strip leading "---\n"
    rest = parts[1]    # starts with "\n"
    return fm, rest


def extract_fields(text: str):
    """Extract YAML fields (scalars and lists) from text.

    Returns (fields_dict, remaining_text).
    Fields at the start of the body are consumed; everything after the
    field section (including list items belonging to those fields) is
    returned as remaining_text.
    """
    fields = {}
    lines = text.splitlines()
    body_lines = []
    in_fields = False
    current_list_field = None
    list_items = []

    def flush_list():
        nonlocal current_list_field, list_items
        if current_list_field and list_items:
            fields[current_list_field] = list_items
        current_list_field = None
        list_items = []

    for line in lines:
        stripped = line.strip()

        if not in_fields:
            if stripped == "":
                continue  # skip leading blanks
            if stripped.startswith("#"):
                body_lines.append(line)
                continue
            m = FIELD_RE.match(stripped)
            if m:
                flush_list()
                in_fields = True
                key, val = m.group(1), m.group(2).strip()
                if key in METADATA_FIELDS:
                    if val == "":
                        # Could be a list field - check next lines
                        current_list_field = key
                        list_items = []
                        continue
                    else:
                        fields[key] = val
                        continue
                else:
                    # Non-metadata field - end field section
                    in_fields = False
                    body_lines.append(line)
                    continue
            # First non-blank, non-field line ends field section
            in_fields = False
            body_lines.append(line)
            continue

        # in_fields is True
        if stripped == "":
            flush_list()
            in_fields = False
            body_lines.append(line)
            continue
        if stripped.startswith("#"):
            flush_list()
            in_fields = False
            body_lines.append(line)
            continue

        # Check for list item
        m = LIST_ITEM_RE.match(line)
        if m and current_list_field is not None:
            list_items.append(m.group(1).strip())
            continue

        # Check for new scalar field
        m = FIELD_RE.match(stripped)
        if m:
            flush_list()
            key, val = m.group(1), m.group(2).strip()
            if key in METADATA_FIELDS:
                if val == "":
                    current_list_field = key
                    list_items = []
                    continue
                else:
                    fields[key] = val
                    continue
            # Non-metadata field
            in_fields = False
            body_lines.append(line)
            continue

        # Non-field, non-blank, non-comment line ends field section
        flush_list()
        in_fields = False
        body_lines.append(line)

    flush_list()
    return fields, "\n".join(body_lines)


def get_frontmatter_fields(fm_text: str):
    """Parse existing frontmatter fields (scalars only)."""
    fields = {}
    for line in fm_text.splitlines():
        m = FIELD_RE.match(line.strip())
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields


def format_value(val):
    """Format a field value for YAML output."""
    if isinstance(val, list):
        if not val:
            return ""
        lines = []
        for item in val:
            # Quote items with special chars
            if ":" in item or "#" in item:
                lines.append(f'  - "{item}"')
            else:
                lines.append(f"  - {item}")
        return "\n" + "\n".join(lines)
    # Scalar
    s = str(val)
    if ":" in s or "#" in s or s.startswith("[") or s.startswith("{") or s.startswith('"'):
        return f'"{s}"'
    return s


def normalize_skill(text: str):
    """Return (new_text, changes_made, field_count)."""
    fm_text, body_text = split_skill(text)
    fm_fields = get_frontmatter_fields(fm_text)
    body_fields, clean_body = extract_fields(body_text)

    # Strip a leading --- delimiter from clean_body (was the original
    # closing frontmatter marker that we're replacing)
    clean_body_stripped = clean_body
    if clean_body_stripped.startswith("---\n"):
        clean_body_stripped = clean_body_stripped[len("---\n"):]

    # Determine which body fields need promotion
    to_promote = {}
    for key, val in body_fields.items():
        if key not in fm_fields:
            to_promote[key] = val

    if not to_promote:
        return text, [], 0

    # Build new frontmatter
    new_fm_lines = fm_text.splitlines()
    for key in sorted(to_promote.keys()):
        val = to_promote[key]
        new_fm_lines.append(f"{key}:{format_value(val)}")

    new_fm = "\n".join(new_fm_lines)
    new_text = f"---\n{new_fm}\n---{clean_body_stripped}"

    changes = [f"promoted {k}" for k in sorted(to_promote.keys())]
    return new_text, changes, len(to_promote)


def main():
    ap = argparse.ArgumentParser(description="Normalize skill SKILL.md files")
    ap.add_argument("--fix", action="store_true", help="Apply changes to files")
    ap.add_argument("--limit", type=int, default=0, help="Process only N skills (0 = all)")
    args = ap.parse_args()

    total = 0
    changed = 0
    total_fields = 0

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
        new_text, changes, field_count = normalize_skill(text)

        if changes:
            changed += 1
            total_fields += field_count
            print(f"  {skill_dir.name}: {', '.join(changes)}")
            if args.fix:
                skill_file.write_text(new_text, encoding="utf-8")

    print(f"\nTotal skills scanned: {total}")
    print(f"Skills needing changes: {changed}")
    print(f"Total fields to promote: {total_fields}")
    if not args.fix:
        print("Run with --fix to apply changes.")


if __name__ == "__main__":
    main()
