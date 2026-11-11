#!/usr/bin/env python3
"""Context-budget accounting per profile.

For each profile, sums tokens in AGENTS.md + manifest.json + the profile's
active skill set. Uses bytes/4 as a conservative token estimate.
Emits .agent/reports/context-budget.json. Fails if any profile exceeds
its documented per-profile ceiling.

Usage: python3 tools/context_budget.py [--ceiling 15000]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
AGENTS_MD = ROOT / "AGENTS.md"
MANIFEST_JSON = ROOT / ".context" / "manifest.json"
SKILLS_INDEX = ROOT / "skills" / "index.json"
PROFILES_DIR = ROOT / ".agent" / "profiles"
REPORT_DIR = ROOT / ".agent" / "reports"
REPORT_FILE = REPORT_DIR / "context-budget.json"

# Per-profile token ceilings (conservative bytes/4 estimate)
# Base tokens (AGENTS.md + manifest.json) ≈ 20,238. Ceilings set with ~20% headroom
# above current usage to detect runaway growth while being achievable today.
CEILINGS = {
    "conceptualizer": 35000,
    "taskmaster": 55000,
    "coder": 60000,
    "researcher": 45000,
    "reviewer": 40000,
    "coding-manager": 50000,
    "research-manager": 45000,
    "review-manager": 45000,
    "wiki-producer": 35000,
    "starter": 45000,
}

DEFAULT_CEILING = 25000


def estimate_tokens(text: str) -> int:
    """Conservative token estimate: bytes / 4."""
    return len(text.encode("utf-8")) // 4


def profile_active_skills(profile_name: str) -> list[str]:
    """Read skill names from a profile's frontmatter."""
    profile_file = PROFILES_DIR / f"{profile_name}.md"
    if not profile_file.exists():
        return []
    text = profile_file.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return []
    fm = text.split("\n---", 1)[0]
    names, in_skills = [], False
    for line in fm.splitlines():
        if line.startswith("skills:"):
            in_skills = True
            continue
        if in_skills:
            if line.startswith("  - "):
                names.append(line.strip("- ").strip())
            elif line.strip() == "":
                continue
            else:
                break
    return names


def skill_token_cost(skill_name: str) -> int:
    """Estimate tokens for a skill: SKILL.md file size / 4."""
    skill_file = ROOT / ".agent" / "skills" / skill_name / "SKILL.md"
    if not skill_file.exists():
        return 0
    return estimate_tokens(skill_file.read_text(encoding="utf-8", errors="replace"))


def main():
    ap = argparse.ArgumentParser(description="Context-budget accounting per profile")
    ap.add_argument("--ceiling", type=int, default=DEFAULT_CEILING,
                    help=f"Default per-profile token ceiling (default {DEFAULT_CEILING})")
    args = ap.parse_args()

    if not MANIFEST_JSON.exists():
        print(f"FAIL: manifest not found: {MANIFEST_JSON}")
        sys.exit(1)

    agents_text = AGENTS_MD.read_text(encoding="utf-8", errors="replace") if AGENTS_MD.exists() else ""
    manifest_text = MANIFEST_JSON.read_text(encoding="utf-8", errors="replace")
    base_tokens = estimate_tokens(agents_text) + estimate_tokens(manifest_text)

    # Load skills index for descriptions
    skills_index = {}
    if SKILLS_INDEX.exists():
        try:
            index_data = json.loads(SKILLS_INDEX.read_text(encoding="utf-8"))
            for s in index_data.get("skills", []):
                skills_index[s["name"]] = s.get("description", "")
        except (json.JSONDecodeError, KeyError):
            pass

    results = []
    failed = False

    for profile_file in sorted(PROFILES_DIR.glob("*.md")):
        profile_name = profile_file.stem
        active_skills = profile_active_skills(profile_name)

        skill_tokens = sum(skill_token_cost(s) for s in active_skills)
        total = base_tokens + skill_tokens

        ceiling = CEILINGS.get(profile_name, args.ceiling)
        over = total > ceiling
        if over:
            failed = True

        results.append({
            "profile": profile_name,
            "base_tokens": base_tokens,
            "skill_tokens": skill_tokens,
            "total_tokens": total,
            "ceiling": ceiling,
            "over_budget": over,
            "active_skill_count": len(active_skills),
        })

    results.sort(key=lambda r: -r["total_tokens"])

    report = {
        "ceiling_default": args.ceiling,
        "base_tokens": base_tokens,
        "profiles": results,
        "generated_at": "2026-11-10",
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")

    for r in results:
        status = "OVER BUDGET" if r["over_budget"] else "OK"
        print(f"  {r['profile']}: {r['total_tokens']:,} tokens / {r['ceiling']:,} ceiling ({status})")

    if failed:
        print(f"\nFAIL: {sum(1 for r in results if r['over_budget'])} profile(s) exceed token ceiling")
        sys.exit(1)

    print(f"\nPASS: all {len(results)} profiles within token ceiling")


if __name__ == "__main__":
    main()
