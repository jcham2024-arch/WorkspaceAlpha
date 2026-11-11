#!/usr/bin/env python3
"""Bulk backfill provenance metadata into every skill's SKILL.md frontmatter.

Adds: source_url, source_ref, source_commit, content_hash, fetched_at, upstream_license.

- content_hash: SHA-256 of the SKILL.md file
- fetched_at: 2026-11-10 (backfill date)
- upstream_license: read from LICENSE file in skill folder, or "unknown"
- source_url/source_ref/source_commit: empty (not available from archive import)

Idempotent: re-running is safe.

Usage: python3 tools/backfill_provenance.py
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agent" / "skills"
FETCHED_AT = "2026-11-10"

PROVENANCE_FIELDS = [
    "source_url", "source_ref", "source_commit",
    "content_hash", "fetched_at", "upstream_license",
]


def read_license(skill_dir: pathlib.Path) -> str:
    """Read upstream license from LICENSE file in skill folder."""
    lic_file = skill_dir / "LICENSE"
    if not lic_file.exists():
        return "unknown"
    try:
        text = lic_file.read_text(encoding="utf-8", errors="replace").strip()
        # Extract first line as license identifier
        first_line = text.splitlines()[0] if text else ""
        if "MIT" in first_line:
            return "MIT"
        if "Apache" in first_line:
            return "Apache-2.0"
        if "Creative Commons" in first_line or "CC0" in first_line:
            return "CC0-1.0"
        if "BSD" in first_line:
            return "BSD-3-Clause"
        return "unknown"
    except Exception:
        return "unknown"


def compute_content_hash(skill_file: pathlib.Path) -> str:
    return hashlib.sha256(skill_file.read_bytes()).hexdigest()


def parse_frontmatter(text: str) -> tuple[dict, str, str]:
    """Return (fields_dict, frontmatter_block, body_after_second_dash)."""
    if not text.startswith("---\n"):
        return {}, "", text
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return {}, "", text
    header = parts[0][4:]  # strip leading "---\n"
    rest = parts[1]  # starts with "\n"
    fields = {}
    for line in header.splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, _, v = line.partition(":")
            fields[k.strip()] = v.strip().strip('"').strip("'")
    return fields, header, rest


def main():
    changed = 0
    already = 0

    for skill_dir in sorted(SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        text = skill_file.read_text(encoding="utf-8", errors="replace")
        fields, header, rest = parse_frontmatter(text)

        # Check if all provenance fields already present
        has_all = all(f in fields for f in PROVENANCE_FIELDS)
        if has_all:
            already += 1
            continue

        # Compute missing values
        content_hash = compute_content_hash(skill_file)
        upstream_license = read_license(skill_dir)

        # Build new frontmatter
        lines = header.splitlines()
        # Add missing provenance fields
        for f in PROVENANCE_FIELDS:
            if f not in fields:
                if f == "content_hash":
                    val = content_hash
                elif f == "fetched_at":
                    val = FETCHED_AT
                elif f == "upstream_license":
                    val = upstream_license
                else:
                    val = ""
                lines.append(f'{f}: "{val}"')

        new_header = "\n".join(lines)
        new_text = f"---\n{new_header}\n---{rest}"
        skill_file.write_text(new_text, encoding="utf-8")
        changed += 1

    print(f"Provenance backfill complete: {changed} changed, {already} already complete")


if __name__ == "__main__":
    main()
