#!/usr/bin/env python3
"""Distill skill usage patterns from provenance records into GPM entries.

Reads `memory/runs/*.jsonl` provenance records and identifies patterns
of tool/skill usage. Abstracts concrete skill names into type-level
categories based on skill name prefixes and frontmatter categories.

Writes results to `.context/pattern-memory/gpm.json`.

Usage:
    python tools/distill.py                    # Run full distillation
    python tools/distill.py --dry-run          # Preview without writing
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MEMORY_RUNS_DIR = ROOT / "memory" / "runs"
GPM_PATH = ROOT / ".context" / "pattern-memory" / "gpm.json"
GPM_INDEX_PATH = ROOT / ".context" / "pattern-memory" / "gpm.index"

# Mapping from skill name prefixes to type-level categories
SKILL_CATEGORY_MAP: dict[str, str] = {
    "brainstorming": "brainstorming",
    "writing-plans": "writing-plans",
    "thinking-first-principles": "thinking-first-principles",
    "thinking-margin-of-safety": "thinking-margin-of-safety",
    "skill-audit": "skill-audit",
    "skill-check": "skill-check",
    "skill-gap-analysis": "skill-gap-analysis",
    "skill-host-compat": "skill-host-compat",
    "plan-canvas": "plan-canvas",
    "plan-orchestrate": "plan-orchestrate",
    "research-planning": "research-planning",
    "skill-comply": "skill-comply",
}


def categorize_skill(skill_name: str) -> str:
    """Categorize a skill name into a type-level category."""
    # Check exact match first
    if skill_name in SKILL_CATEGORY_MAP:
        return SKILL_CATEGORY_MAP[skill_name]
    # Check prefix match
    for prefix, category in SKILL_CATEGORY_MAP.items():
        if skill_name.startswith(prefix):
            return category
    # Default: use the skill name itself as category
    return skill_name


def load_provenance_records() -> list[dict[str, Any]]:
    """Load all provenance records from memory/runs/*.jsonl."""
    records = []
    if not MEMORY_RUNS_DIR.exists():
        return records

    for run_file in sorted(MEMORY_RUNS_DIR.glob("*.jsonl")):
        with run_file.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    records.append(record)
                except json.JSONDecodeError:
                    continue
    return records


def load_gpm() -> dict[str, Any]:
    """Load the existing GPM registry."""
    if not GPM_PATH.exists():
        return {"version": "1.0", "patterns": []}
    with GPM_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_gpm(gpm: dict[str, Any]) -> None:
    """Save the GPM registry."""
    GPM_PATH.parent.mkdir(parents=True, exist_ok=True)
    GPM_PATH.write_text(json.dumps(gpm, indent=2), encoding="utf-8")


def abstract_skill_name(skill_name: str) -> str:
    """Abstract a skill name to a type-level category."""
    return categorize_skill(skill_name)


def extract_patterns_from_record(record: dict) -> list[dict[str, Any]]:
    """Extract pattern candidates from a single provenance record.

    Looks at the assembled nodes in the record and extracts skill usage
    patterns. Returns a list of pattern dicts with skeleton and evidence.
    """
    patterns = []
    assembled_nodes = record.get("assembled_nodes", [])
    outcome = record.get("return_envelope", {}).get("status", "unknown")

    # Only process successful outcomes
    if outcome not in ("COMPLETE", "ok"):
        return patterns

    # Group nodes by abstracted type
    type_sequence: list[str] = []
    node_evidence: dict[str, list[str]] = {}

    for node in assembled_nodes:
        node_id = node.get("node_id", "")
        node_type = node.get("node_type", "")
        skill_name = node.get("node_id", "")

        # Extract category from node_id (skill name pattern)
        category = abstract_skill_name(node_id)
        type_sequence.append(category)
        node_evidence.setdefault(category, []).append(node_id)

    if not type_sequence:
        return patterns

    # Build skeleton from type sequence
    skeleton = list(type_sequence)

    # Create pattern
    pattern = {
        "pattern_id": f"pattern-{hash(tuple(skeleton)) % 10000:04d}",
        "type_signature": " > ".join(type_sequence),
        "skeleton": skeleton,
        "concrete_example": {
            "nodes": list(node_evidence.keys())[:5],
            "outcome": outcome,
        },
        "signature_embedding": None,  # Will be filled by embedder
        "reward_score": 1.0 if outcome == "COMPLETE" else 0.5,
        "support_count": 1,
        "created_at": None,  # Will be filled by caller
        "last_used_at": None,
    }
    patterns.append(pattern)

    return patterns


def distill(records: list[dict]) -> list[dict]:
    """Distill patterns from all provenance records.

    Groups patterns by skeleton and merges duplicates, updating support
    counts and reward scores.
    """
    pattern_map: dict[str, dict] = {}

    for record in records:
        patterns = extract_patterns_from_record(record)
        for pattern in patterns:
            skeleton_key = " > ".join(pattern["skeleton"])
            if skeleton_key in pattern_map:
                existing = pattern_map[skeleton_key]
                existing["support_count"] += 1
                # Exponential moving average with alpha=0.2
                existing["reward_score"] = 0.8 * existing["reward_score"] + 0.2 * pattern["reward_score"]
                # Merge evidence
                existing["concrete_example"]["nodes"].extend(
                    pattern["concrete_example"]["nodes"]
                )
                existing["concrete_example"]["nodes"] = list(
                    set(existing["concrete_example"]["nodes"])
                )[:10]
            else:
                pattern_map[skeleton_key] = pattern

    return list(pattern_map.values())


def main():
    """CLI: run distillation."""
    import argparse

    ap = argparse.ArgumentParser(description="Distill skill patterns from provenance")
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without writing to GPM registry",
    )
    args = ap.parse_args()

    records = load_provenance_records()
    print(f"Loaded {len(records)} provenance records")

    patterns = distill(records)
    print(f"Discovered {len(patterns)} unique patterns")

    for p in sorted(patterns, key=lambda p: p["support_count"], reverse=True)[:10]:
        print(f"  {p['pattern_id']}: {p['type_signature']} (support={p['support_count']}, "
              f"reward={p['reward_score']:.2f})")

    if args.dry_run:
        print("\nDry run - no changes written")
    else:
        save_gpm({"version": "1.0", "patterns": patterns})
        print(f"\nWrote {len(patterns)} patterns to {GPM_PATH}")


if __name__ == "__main__":
    main()
