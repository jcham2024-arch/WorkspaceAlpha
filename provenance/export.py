#!/usr/bin/env python3
"""Provenance Export — export audit bundle for SIEM ingestion.

Exports a bundle containing:
- Provenance records (Record A) for a delegation
- Access log entries
- Policy version info

The export bundle is suitable for SIEM ingestion and audit review.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROVENANCE_DIR = ROOT / "provenance"


class ExportManager:
    """Exports provenance data for audit purposes."""

    def __init__(self, provenance_dir: Path | None = None):
        self.provenance_dir = provenance_dir or PROVENANCE_DIR
        self.jsonl_path = self.provenance_dir / "turns.jsonl"
        self.debug_trace_path = self.provenance_dir / "debug_traces.jsonl"

    def export_delegation(self, delegation_id: str) -> dict:
        """Export all provenance data for a delegation.

        Returns a dict containing:
        - delegation_id
        - export_timestamp
        - provenance_records: list of Record A entries
        - debug_traces: list of Record B entries (if any)
        - policy_version: redaction policy version
        - export_format: "jsonl-bundle"
        """
        from provenance.recorder import ProvenanceRecorder

        recorder = ProvenanceRecorder(self.provenance_dir)
        records = recorder.get_turns(delegation_id=delegation_id)
        debug_traces = recorder.get_debug_traces(delegation_id=delegation_id)

        # Get policy version from latest record if available
        policy_version = None
        if records:
            policy_version = records[-1].get("redaction_policy_version")

        bundle = {
            "delegation_id": delegation_id,
            "export_timestamp": datetime.now(timezone.utc).isoformat(),
            "export_format": "jsonl-bundle",
            "provenance_records": records,
            "debug_traces": debug_traces,
            "policy_version": policy_version,
            "record_count": len(records),
            "debug_trace_count": len(debug_traces),
        }

        return bundle

    def export_to_file(self, delegation_id: str, output_path: str) -> str:
        """Export delegation data to a JSON file.

        Returns the output path.
        """
        bundle = self.export_delegation(delegation_id)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(bundle, f, ensure_ascii=False, indent=2)
        return str(output_path)

    def export_all_delegations(self, output_dir: str) -> list[str]:
        """Export all delegations to individual JSON files.

        Returns list of output file paths.
        """
        from provenance.recorder import ProvenanceRecorder

        recorder = ProvenanceRecorder(self.provenance_dir)
        records = recorder.get_turns()

        # Collect unique delegation IDs
        delegation_ids = set()
        for record in records:
            did = record.get("delegation_id")
            if did:
                delegation_ids.add(did)

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        paths = []
        for did in delegation_ids:
            path = output_dir / f"{did}.json"
            self.export_to_file(did, str(path))
            paths.append(str(path))

        return paths


def main():
    """CLI: export provenance data."""
    import argparse

    ap = argparse.ArgumentParser(description="Provenance export manager")
    ap.add_argument(
        "--delegation-id",
        help="Delegation ID to export",
    )
    ap.add_argument(
        "--output",
        help="Output file path (for single delegation export)",
    )
    ap.add_argument(
        "--output-dir",
        help="Output directory (for exporting all delegations)",
    )
    args = ap.parse_args()

    exporter = ExportManager()

    if args.delegation_id and args.output:
        path = exporter.export_to_file(args.delegation_id, args.output)
        print(f"Exported to {path}")
    elif args.delegation_id:
        bundle = exporter.export_delegation(args.delegation_id)
        print(json.dumps(bundle, indent=2))
    elif args.output_dir:
        paths = exporter.export_all_delegations(args.output_dir)
        print(f"Exported {len(paths)} delegation bundles to {args.output_dir}")
        for p in paths:
            print(f"  {p}")
    else:
        print("Use --delegation-id with --output, or --output-dir")


if __name__ == "__main__":
    main()
