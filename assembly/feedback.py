#!/usr/bin/env python3
"""Feedback phase — CLI entry point for the DAG compiler pipeline.

Assembles a two-zone prompt from a delegation JSON file.
Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "assembly"))

from assembler import Assembler, BLOCKED  # noqa: E402


def main() -> None:
    """CLI: assemble a prompt from a delegation JSON file."""
    ap = argparse.ArgumentParser(
        description="Assemble a two-zone prompt from a delegation"
    )
    ap.add_argument("delegation_file", help="Path to delegation JSON file")
    args = ap.parse_args()

    with open(args.delegation_file, "r", encoding="utf-8") as f:
        delegation = json.load(f)

    assembler = Assembler()
    try:
        result = assembler.assemble(delegation)
        print(json.dumps(result, indent=2))
    except BLOCKED as exc:
        print(
            json.dumps(
                {
                    "blocked": True,
                    "reason": exc.reason,
                    "excluded_nodes": exc.excluded_nodes,
                },
                indent=2,
            )
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
