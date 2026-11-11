#!/usr/bin/env python3
"""List skills with zero invocations in the usage log window.

Reads .agent/logs/skill-usage.jsonl (opt-in, local-first log) and reports
skills that have never been invoked. Feeds Task 1 demotion decisions.

Usage: python3 tools/unused_skills.py [--log-file .agent/logs/skill-usage.jsonl]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / ".agent" / "skills"
DEFAULT_LOG = ROOT / ".agent" / "logs" / "skill-usage.jsonl"


def main():
    ap = argparse.ArgumentParser(description="List unused skills from usage log")
    ap.add_argument("--log-file", default=str(DEFAULT_LOG),
                    help=f"Path to usage log (default {DEFAULT_LOG})")
    args = ap.parse_args()

    log_file = pathlib.Path(args.log_file)

    # All known skills from master library
    all_skills: set[str] = set()
    if SKILLS_DIR.exists():
        for d in SKILLS_DIR.iterdir():
            if d.is_dir() and (d / "SKILL.md").exists():
                all_skills.add(d.name)

    # Skills seen in the log
    seen_skills: set[str] = set()
    total_entries = 0

    if log_file.exists():
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    skill_id = entry.get("skill_id")
                    if skill_id:
                        seen_skills.add(skill_id)
                        total_entries += 1
                except json.JSONDecodeError:
                    continue

    unused = sorted(all_skills - seen_skills)

    print(f"Usage log entries: {total_entries}")
    print(f"Skills in master library: {len(all_skills)}")
    print(f"Skills seen in log: {len(seen_skills)}")
    print(f"Skills with zero invocations: {len(unused)}")

    if unused:
        print("\nUnused skills:")
        for sid in unused:
            print(f"  {sid}")
    else:
        print("\nAll skills have been invoked at least once.")


if __name__ == "__main__":
    main()
