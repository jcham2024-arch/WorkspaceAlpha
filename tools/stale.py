#!/usr/bin/env python3
"""List skills unreviewed for > 180 days, grouped by tier.

Reads `last_reviewed:` from each skill's SKILL.md frontmatter and flags
those whose review date is older than 180 days from today (2026-11-10).

Usage: python3 tools/stale.py [--days 180]
"""
from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agent" / "skills"
TIER_FILE = ROOT / ".agent" / "skills" / "TIERS.md"
TODAY = datetime.date(2026, 11, 10)
DEFAULT_DAYS = 180


def read_tier(skill_dir: pathlib.Path) -> str:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return "unknown"
    text = skill_file.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return "unknown"
    fm = text.split("\n---", 1)[0]
    for line in fm.splitlines():
        if line.startswith("tier:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return "unknown"


def read_last_reviewed(skill_dir: pathlib.Path) -> datetime.date | None:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return None
    text = skill_file.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return None
    fm = text.split("\n---", 1)[0]
    for line in fm.splitlines():
        if line.startswith("last_reviewed:"):
            val = line.split(":", 1)[1].strip()
            try:
                return datetime.date.fromisoformat(val)
            except ValueError:
                return None
    return None


def main():
    ap = argparse.ArgumentParser(description="List stale skills by tier")
    ap.add_argument("--days", type=int, default=DEFAULT_DAYS,
                    help=f"Days threshold for staleness (default {DEFAULT_DAYS})")
    args = ap.parse_args()

    cutoff = TODAY - datetime.timedelta(days=args.days)
    stale_by_tier: dict[str, list[tuple[str, str]]] = {}  # tier -> [(id, last_reviewed)]

    total = 0
    missing_review = 0
    for skill_dir in sorted(SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue
        if not (skill_dir / "SKILL.md").exists():
            continue
        total += 1
        tier = read_tier(skill_dir)
        reviewed = read_last_reviewed(skill_dir)
        if reviewed is None:
            missing_review += 1
            continue
        if reviewed < cutoff:
            stale_by_tier.setdefault(tier, []).append(
                (skill_dir.name, reviewed.isoformat())
            )

    print(f"Total skills: {total}")
    print(f"Missing last_reviewed: {missing_review}")
    print(f"Stale cutoff: {cutoff.isoformat()} ({args.days} days before {TODAY.isoformat()})")

    total_stale = 0
    for tier in sorted(stale_by_tier.keys()):
        skills = stale_by_tier[tier]
        total_stale += len(skills)
        print(f"\n{tier} ({len(skills)} stale):")
        for sid, date in sorted(skills):
            print(f"  {sid} (last_reviewed: {date})")

    print(f"\nTotal stale: {total_stale}")


if __name__ == "__main__":
    main()
