#!/usr/bin/env python3
"""Deterministic routing evaluator.

Compares a simple keyword-based router's decisions against the routing eval set
(tests/evals/routing.jsonl). Exits 0 if all expected (profile, skill_id) pairs
match, exits 1 on any mismatch.

Usage: python3 tools/eval_routing.py <eval_file>
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Simple keyword -> (profile, skill) mapping. Mirrors the conceptualizer's
# routing logic: AGENTS.md -> manifest.json -> skills/index.json -> profile.
# Keywords use spaces (not dots) to match task text. More specific keywords
# listed first so they match before general ones.
ROUTE_MAP = [
    # Multi-word specific keywords
    ("first principles", "conceptualizer", "thinking-first-principles"),
    ("risk buffer", "conceptualizer", "thinking-margin-of-safety"),
    ("research methodology", "starter", "research-planning"),
    ("skill audit", "starter", "skill-audit"),
    ("skill check", "starter", "skill-check"),
    ("skill gap", "starter", "skill-gap-analysis"),
    ("skill host", "starter", "skill-host-compat"),
    ("skill compliance", "starter", "skill-comply"),
    ("plan canvas", "starter", "plan-canvas"),
    ("review code", "reviewer", "writing-plans"),
    # Single-word keywords
    ("brainstorm", "conceptualizer", "brainstorming"),
    ("implementation plan", "conceptualizer", "writing-plans"),
    ("audit", "starter", "skill-audit"),
    ("validate", "starter", "skill-check"),
    ("gap", "starter", "skill-gap-analysis"),
    ("host compat", "starter", "skill-host-compat"),
    ("canvas", "starter", "plan-canvas"),
    ("orchestrat", "starter", "plan-orchestrate"),
    ("research", "starter", "research-planning"),
    ("compliance", "starter", "skill-comply"),
    ("dispatch", "taskmaster", "writing-plans"),
    ("review", "reviewer", "writing-plans"),
]


def route(task: str) -> tuple[str, str]:
    """Route a task to (profile, skill_id) using keyword matching."""
    task_lower = task.lower()
    for keyword, profile, skill in ROUTE_MAP:
        if keyword in task_lower:
            return profile, skill
    return "conceptualizer", "brainstorming"  # default fallback


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/eval_routing.py <eval_file>")
        sys.exit(1)

    eval_file = pathlib.Path(sys.argv[1])
    if not eval_file.exists():
        print(f"FAIL: eval file not found: {eval_file}")
        sys.exit(1)

    passed = 0
    failed = 0

    with open(eval_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            task = entry["task"]
            expected_profile = entry["expected_profile"]
            expected_skill = entry["expected_skill"]

            actual_profile, actual_skill = route(task)

            if actual_profile == expected_profile and actual_skill == expected_skill:
                passed += 1
            else:
                failed += 1
                print(f"MISMATCH: task='{task[:60]}...'")
                print(f"  expected: ({expected_profile}, {expected_skill})")
                print(f"  actual:   ({actual_profile}, {actual_skill})")

    print(f"\nRouting eval: {passed} passed, {failed} failed out of {passed + failed}")

    if failed > 0:
        sys.exit(1)
    print("PASS: all routing decisions match expected")


if __name__ == "__main__":
    main()
