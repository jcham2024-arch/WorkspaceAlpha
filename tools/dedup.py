#!/usr/bin/env python3
"""Deduplication candidate finder for the master skill library.

Computes Jaccard similarity on token sets between skill pairs, using
rarest-token blocking to minimize comparisons. Outputs candidate clusters
to .agent/reports/dedup-candidates.json.

Does NOT delete or modify any skill — output is a report for human review.

Usage: python3 tools/dedup.py [--threshold 0.7]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agent" / "skills"
REPORT_DIR = ROOT / ".agent" / "reports"
REPORT_FILE = REPORT_DIR / "dedup-candidates.json"

DEFAULT_THRESHOLD = 0.7


def tokenize(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", text.lower()) if len(t) >= 3}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def read_skill_text(skill_file: pathlib.Path) -> str:
    return skill_file.read_text(encoding="utf-8", errors="replace")


def main():
    ap = argparse.ArgumentParser(description="Find dedup candidates in skill library")
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                    help=f"Jaccard similarity threshold (default {DEFAULT_THRESHOLD})")
    args = ap.parse_args()

    if not SKILLS.exists():
        print(f"FAIL: skills directory not found: {SKILLS}")
        sys.exit(1)

    # Read all skill texts and compute token sets
    skill_data: list[tuple[str, set[str]]] = []
    for skill_dir in sorted(SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        text = read_skill_text(skill_file)
        toks = tokenize(text)
        skill_data.append((skill_dir.name, toks))

    print(f"Read {len(skill_data)} skills")

    # Compute token frequency across all skills
    token_freq: dict[str, int] = defaultdict(int)
    for _, toks in skill_data:
        for t in toks:
            token_freq[t] += 1

    # Rarest-token blocking: for each skill, use its rarest token as blocking key
    # This ensures each skill appears in a small blocking group
    rare_token_to_skills: dict[str, list[tuple[str, set[str]]]] = defaultdict(list)
    for sid, toks in skill_data:
        if not toks:
            continue
        rarest = min(toks, key=lambda t: token_freq[t])
        rare_token_to_skills[rarest].append((sid, toks))

    candidates = []
    comparisons = 0
    for rare_tok, group in rare_token_to_skills.items():
        if len(group) < 2:
            continue
        for i in range(len(group)):
            sid_a, toks_a = group[i]
            for j in range(i + 1, len(group)):
                sid_b, toks_b = group[j]
                comparisons += 1
                sim = jaccard(toks_a, toks_b)
                if sim >= args.threshold:
                    candidates.append({
                        "skill_a": sid_a,
                        "skill_b": sid_b,
                        "similarity": round(sim, 3),
                        "recommendation": "review",
                    })

    print(f"Made {comparisons} comparisons")

    candidates.sort(key=lambda c: -c["similarity"])

    # Cluster using union-find
    parent: dict[str, str] = {}

    def find(x: str) -> str:
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for c in candidates:
        union(c["skill_a"], c["skill_b"])

    clusters: dict[str, set[str]] = defaultdict(set)
    for c in candidates:
        root = find(c["skill_a"])
        clusters[root].add(c["skill_a"])
        clusters[root].add(c["skill_b"])

    cluster_list = [
        {"cluster_id": root, "skills": sorted(members), "size": len(members)}
        for root, members in clusters.items()
    ]
    cluster_list.sort(key=lambda c: -c["size"])

    report = {
        "threshold": args.threshold,
        "total_skills": len(skill_data),
        "comparisons": comparisons,
        "candidate_pairs": len(candidates),
        "clusters": cluster_list,
        "pairs": candidates,
        "generated_at": "2026-11-10",
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")

    print(f"Found {len(candidates)} candidate pairs above threshold {args.threshold}")
    print(f"Found {len(cluster_list)} clusters")
    print(f"Report written to {REPORT_FILE}")


if __name__ == "__main__":
    main()
