#!/usr/bin/env python3
"""Provenance Retention — manages retention of provenance and debug trace records.

Implements tiered retention:
- Provenance records (Record A): indefinite retention
- Debug traces (Record B): 30-day retention, then deleted

Provides cleanup and erasure functions.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROVENANCE_DIR = ROOT / "provenance"


class RetentionManager:
    """Manages retention of provenance records and debug traces."""

    def __init__(
        self,
        provenance_dir: Path | None = None,
        retention_days: int = 30,
    ):
        self.provenance_dir = provenance_dir or PROVENANCE_DIR
        self.retention_days = retention_days
        self.jsonl_path = self.provenance_dir / "turns.jsonl"
        self.debug_trace_path = self.provenance_dir / "debug_traces.jsonl"

    def cleanup_debug_traces(self) -> dict[str, int]:
        """Remove debug trace records older than retention_days.

        Returns dict with counts of records before/after cleanup.
        """
        if not self.debug_trace_path.exists():
            return {"before": 0, "after": 0, "removed": 0}

        cutoff = datetime.now(timezone.utc) - timedelta(days=self.retention_days)
        cutoff_iso = cutoff.isoformat()

        kept_lines = []
        removed_count = 0
        total_count = 0

        with self.debug_trace_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    kept_lines.append(line)
                    continue
                total_count += 1
                try:
                    record = json.loads(line)
                    ts = record.get("turn_timestamp", "")
                    if ts and ts < cutoff_iso:
                        removed_count += 1
                    else:
                        kept_lines.append(line)
                except json.JSONDecodeError:
                    # Keep malformed lines
                    kept_lines.append(line)

        # Write back kept lines
        with self.debug_trace_path.open("w", encoding="utf-8") as f:
            for line in kept_lines:
                f.write(line + "\n")

        return {
            "before": total_count,
            "after": len(kept_lines),
            "removed": removed_count,
        }

    def erase_delegation(self, delegation_id: str) -> dict[str, int]:
        """Erase all records for a given delegation ID.

        Provenance records (Record A) are kept but stripped of any
        identifying content beyond what's already there (they contain
        no raw prompt text). Debug traces (Record B) are fully removed.

        Returns dict with counts of records affected.
        """
        removed_debug = 0
        kept_provenance = []

        # Remove debug traces for this delegation
        if self.debug_trace_path.exists():
            with self.debug_trace_path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        record = json.loads(line)
                        if record.get("delegation_id") == delegation_id:
                            removed_debug += 1
                        else:
                            kept_lines.append(line)
                    except json.JSONDecodeError:
                        kept_lines.append(line)

            with self.debug_trace_path.open("w", encoding="utf-8") as f:
                for line in kept_lines:
                    f.write(line + "\n")

        # Provenance records: keep but they contain no raw text anyway
        # (they contain hashes, IDs, counts only)
        # No action needed for provenance records

        return {
            "debug_traces_removed": removed_debug,
            "provenance_records_kept": True,
        }

    def get_stats(self) -> dict[str, int]:
        """Get record counts for both files."""
        stats = {
            "provenance_records": 0,
            "debug_trace_records": 0,
        }

        if self.jsonl_path.exists():
            with self.jsonl_path.open("r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        stats["provenance_records"] += 1

        if self.debug_trace_path.exists():
            with self.debug_trace_path.open("r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        stats["debug_trace_records"] += 1

        return stats


def main():
    """CLI: run retention cleanup."""
    import argparse

    ap = argparse.ArgumentParser(description="Provenance retention manager")
    ap.add_argument(
        "--cleanup-debug-traces",
        action="store_true",
        help="Remove debug traces older than retention_days",
    )
    ap.add_argument(
        "--erase-delegation",
        help="Erase all records for a delegation ID",
    )
    ap.add_argument(
        "--stats",
        action="store_true",
        help="Show record counts",
    )
    args = ap.parse_args()

    manager = RetentionManager()

    if args.cleanup_debug_traces:
        result = manager.cleanup_debug_traces()
        print(json.dumps(result, indent=2))
    elif args.erase_delegation:
        result = manager.erase_delegation(args.erase_delegation)
        print(json.dumps(result, indent=2))
    elif args.stats:
        print(json.dumps(manager.get_stats(), indent=2))
    else:
        print("Use --cleanup-debug-traces, --erase-delegation, or --stats")


if __name__ == "__main__":
    main()
