#!/usr/bin/env python3
"""Opt-in, local-first skill usage logger.

Appends {ts, profile, skill_id, outcome} to .agent/logs/skill-usage.jsonl.
No network, no telemetry by default. Call this from skill invocation paths
to enable usage tracking for unused_skills.py and demotion decisions.

Usage:
    python3 tools/log_skill_usage.py --profile conceptualizer --skill brainstorming --outcome success
    # or import: from tools.log_skill_usage import log_usage
"""
from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
LOG_FILE = ROOT / ".agent" / "logs" / "skill-usage.jsonl"
TODAY = datetime.date(2026, 11, 10)


def log_usage(profile: str, skill_id: str, outcome: str, log_file: pathlib.Path = LOG_FILE) -> None:
    """Append a skill usage record to the JSONL log."""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": f"{TODAY.isoformat()}T00:00:00+00:00",
        "profile": profile,
        "skill_id": skill_id,
        "outcome": outcome,
    }
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser(description="Log a skill usage event (opt-in, local-only)")
    ap.add_argument("--profile", required=True, help="Profile that invoked the skill")
    ap.add_argument("--skill", required=True, help="Skill ID that was invoked")
    ap.add_argument("--outcome", required=True, help="Outcome: success, failure, skipped")
    args = ap.parse_args()

    log_usage(args.profile, args.skill, args.outcome)
    print(f"Logged: {args.profile} -> {args.skill} ({args.outcome})")


if __name__ == "__main__":
    main()
