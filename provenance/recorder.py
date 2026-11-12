#!/usr/bin/env python3
"""Provenance Recorder — captures per-turn provenance records.

Implements a two-record split:

- Record A (provenance): indefinite retention, NO raw prompt text.
  Contains delegation metadata, node references, token counts, adapter
  params, cache keys, and return envelope status. Safe for long-term
  storage and human review.
- Record B (debug trace): 30-day retention, sampled, redacted. Contains
  the full redacted prompt text and model response. Sampled at a
  configurable rate. Redacted before writing.

Stdlib only. Append-only JSONL files.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROVENANCE_DIR = ROOT / "provenance"
JSONL_PATH = PROVENANCE_DIR / "turns.jsonl"
DEBUG_TRACE_PATH = PROVENANCE_DIR / "debug_traces.jsonl"


class ProvenanceRecorder:
    """Records per-turn provenance with two-record split.

    Record A (provenance) is always written and contains no raw prompt
    text — only hashes, IDs, counts, and metadata. Safe for indefinite
    retention.

    Record B (debug trace) is written only when sampling decides to
    capture, and only after redaction. Contains redacted prompt text
    and model response. Retained for 30 days.
    """

    def __init__(self, provenance_dir: Path | None = None):
        self.provenance_dir = provenance_dir or PROVENANCE_DIR
        self.provenance_dir.mkdir(parents=True, exist_ok=True)
        self.jsonl_path = self.provenance_dir / "turns.jsonl"
        self.debug_trace_path = self.provenance_dir / "debug_traces.jsonl"

    def record_turn(
        self,
        delegation_id: str,
        from_agent: str,
        to_agent: str,
        delegation_type: str,
        target_tier: str,
        assembled_nodes: list[dict],
        token_counts: dict,
        adapter_params: dict,
        return_envelope: dict | None = None,
        cache_hit: bool = False,
        cache_key: str | None = None,
        pruned_nodes: list[str] | None = None,
        # Debug trace (optional, sampled):
        redacted_prompt: str | None = None,
        model_response: str | None = None,
        sampled: bool = False,
        sample_rate: float = 0.1,
        redaction_policy_version: str = "1.0",
        redactions: list[dict] | None = None,
    ) -> dict:
        """Record a turn and return the Record A dict.

        Record A (provenance) is always written. Record B (debug trace)
        is written only when sampled and redacted prompt text is provided.

        Args:
            delegation_id: Unique delegation identifier.
            from_agent: Originating agent name.
            to_agent: Target agent name.
            delegation_type: "MISSION" or "EXECUTION".
            target_tier: "thinking", "low_thinking", or "non_thinking".
            assembled_nodes: List of node dicts with node_id, node_type,
                token_count, cache_hit, etc.
            token_counts: Dict with prefix_tokens, suffix_tokens,
                total_tokens, ceiling_tokens, budget_exceeded.
            adapter_params: Dict with model, thinking, max_tokens, etc.
            return_envelope: Return envelope dict or None.
            cache_hit: Whether the frozen prefix was cache-hit.
            cache_key: SHA-256 of prefix + adapter params.
            pruned_nodes: List of node IDs pruned due to budget.
            redacted_prompt: Redacted prompt text (for Record B only).
            model_response: Model response text (for Record B only).
            sampled: Whether this turn was sampled for debug trace.
            sample_rate: Sampling rate for debug traces (0.0-1.0).
            redaction_policy_version: Version of redaction policy used.
            redactions: List of redaction events.

        Returns:
            The Record A dict that was written.
        """
        now = datetime.now(timezone.utc)
        timestamp = now.isoformat()

        if cache_key is None:
            cache_input = json.dumps(adapter_params, sort_keys=True)
            cache_key = hashlib.sha256(cache_input.encode("utf-8")).hexdigest()[:16]

        # --- Record A: Provenance (NEVER contains raw prompt text) ---
        record_a = {
            "record_type": "provenance",
            "schema_version": "1.0",
            "delegation_id": delegation_id,
            "turn_timestamp": timestamp,
            "from_agent": from_agent,
            "to_agent": to_agent,
            "delegation_type": delegation_type,
            "target_tier": target_tier,
            "assembled_nodes": assembled_nodes,
            "token_counts": token_counts,
            "adapter_params": adapter_params,
            "return_envelope": return_envelope or {},
            "cache_hit": cache_hit,
            "cache_key": cache_key,
            "pruned_nodes": pruned_nodes or [],
        }

        # Always write Record A
        self._write_record(self.jsonl_path, record_a)

        # --- Record B: Debug trace (sampled, redacted) ---
        if sampled and redacted_prompt is not None:
            record_b = {
                "record_type": "debug_trace",
                "schema_version": "1.0",
                "delegation_id": delegation_id,
                "turn_timestamp": timestamp,
                "from_agent": from_agent,
                "to_agent": to_agent,
                "redacted_prompt": redacted_prompt,
                "model_response": model_response,
                "sampled": True,
                "sample_rate": sample_rate,
                "redaction_policy_version": redaction_policy_version,
                "redactions": redactions or [],
            }
            self._write_record(self.debug_trace_path, record_b)

        return record_a

    def _write_record(self, path: Path, record: dict) -> None:
        """Append a JSONL record to the given file."""
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def get_turns(
        self, limit: int | None = None, delegation_id: str | None = None
    ) -> list[dict]:
        """Read turn records (Record A only), optionally filtered."""
        if not self.jsonl_path.exists():
            return []

        records = []
        with self.jsonl_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    if delegation_id is None or record.get("delegation_id") == delegation_id:
                        records.append(record)
                except json.JSONDecodeError:
                    continue

        if limit:
            records = records[-limit:]
        return records

    def get_debug_traces(
        self, limit: int | None = None, delegation_id: str | None = None
    ) -> list[dict]:
        """Read debug trace records (Record B), optionally filtered."""
        if not self.debug_trace_path.exists():
            return []

        records = []
        with self.debug_trace_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    if delegation_id is None or record.get("delegation_id") == delegation_id:
                        records.append(record)
                except json.JSONDecodeError:
                    continue

        if limit:
            records = records[-limit:]
        return records

    def get_summary(self, delegation_id: str) -> dict | None:
        """Get a human-readable summary for a delegation."""
        records = self.get_turns(delegation_id=delegation_id)
        if not records:
            return None

        latest = records[-1]
        return {
            "delegation_id": delegation_id,
            "turn_count": len(records),
            "from_agent": latest.get("from_agent"),
            "to_agent": latest.get("to_agent"),
            "delegation_type": latest.get("delegation_type"),
            "target_tier": latest.get("target_tier"),
            "latest_timestamp": latest.get("turn_timestamp"),
            "final_status": latest.get("return_envelope", {}).get("status", "unknown"),
            "total_tokens": latest.get("token_counts", {}).get("total_tokens", 0),
            "cache_hit": latest.get("cache_hit", False),
            "cache_key": latest.get("cache_key"),
            "pruned_nodes": latest.get("pruned_nodes", []),
        }

    def write_human_readable(self, delegation_id: str) -> str | None:
        """Write a human-readable summary file for a delegation."""
        summary = self.get_summary(delegation_id)
        if summary is None:
            return None

        summary_path = self.provenance_dir / f"{delegation_id}.md"
        lines = [
            f"# Provenance Summary: {delegation_id}",
            "",
            f"- **From**: {summary['from_agent']}",
            f"- **To**: {summary['to_agent']}",
            f"- **Type**: {summary['delegation_type']}",
            f"- **Tier**: {summary['target_tier']}",
            f"- **Status**: {summary['final_status']}",
            f"- **Turns**: {summary['turn_count']}",
            f"- **Latest**: {summary['latest_timestamp']}",
            f"- **Total Tokens**: {summary['total_tokens']}",
            f"- **Cache Hit**: {summary['cache_hit']}",
            f"- **Cache Key**: {summary['cache_key']}",
            "",
            "## Pruned Nodes",
            "",
        ]
        if summary["pruned_nodes"]:
            for node_id in summary["pruned_nodes"]:
                lines.append(f"- {node_id}")
        else:
            lines.append("- None")
        lines.append("")
        lines.append("## Turn Details")
        lines.append("")

        records = self.get_turns(delegation_id=delegation_id)
        for i, record in enumerate(records, 1):
            lines.append(f"### Turn {i}")
            lines.append("")
            lines.append(f"- **Timestamp**: {record.get('turn_timestamp')}")
            lines.append(f"- **Cache Hit**: {record.get('cache_hit')}")
            tc = record.get("token_counts", {})
            lines.append(
                f"- **Tokens**: prefix={tc.get('prefix_tokens', 0)}, "
                f"suffix={tc.get('suffix_tokens', 0)}, "
                f"total={tc.get('total_tokens', 0)}"
            )
            lines.append(f"- **Ceiling**: {tc.get('ceiling_tokens', 'N/A')}")
            lines.append(f"- **Budget Exceeded**: {tc.get('budget_exceeded', False)}")
            lines.append("")
            re_ = record.get("return_envelope", {})
            if re_:
                lines.append(f"- **Return Status**: {re_.get('status', 'unknown')}")
                lines.append(f"- **Steps Used**: {re_.get('steps_used', 'N/A')}")
                ar = re_.get("acceptance_results", [])
                if ar:
                    lines.append("- **Acceptance Results**:")
                    for r in ar:
                        lines.append(
                            f"  - Criterion {r.get('criterion')}: {r.get('result')} "
                            f"— {r.get('evidence', '')[:80]}"
                        )
            lines.append("")

        summary_path.write_text("\n".join(lines), encoding="utf-8")
        return str(summary_path)


def main():
    """CLI: record a turn or read summaries."""
    import argparse

    ap = argparse.ArgumentParser(description="Provenance recorder")
    ap.add_argument("--record", action="store_true", help="Record a test turn")
    ap.add_argument("--summary", help="Get summary for a delegation ID")
    ap.add_argument(
        "--write-readable", help="Write human-readable summary for delegation ID"
    )
    args = ap.parse_args()

    recorder = ProvenanceRecorder()

    if args.summary:
        summary = recorder.get_summary(args.summary)
        if summary:
            print(json.dumps(summary, indent=2))
        else:
            print(f"No records found for {args.summary}")
    elif args.write_readable:
        path = recorder.write_human_readable(args.write_readable)
        if path:
            print(f"Wrote {path}")
        else:
            print(f"No records found for {args.write_readable}")
    elif args.record:
        record = recorder.record_turn(
            delegation_id="del-test-001",
            from_agent="conceptualizer",
            to_agent="taskmaster",
            delegation_type="MISSION",
            target_tier="thinking",
            assembled_nodes=[
                {
                    "node_id": "system-prompt-orchestrator",
                    "node_type": "SystemPrompt",
                    "token_count": 1200,
                    "cache_hit": True,
                },
                {
                    "node_id": "skill-brainstorming",
                    "node_type": "Skill",
                    "token_count": 400,
                    "cache_hit": False,
                },
            ],
            token_counts={
                "prefix_tokens": 1200,
                "suffix_tokens": 400,
                "total_tokens": 1600,
                "ceiling_tokens": 1800,
                "budget_exceeded": False,
            },
            adapter_params={
                "model": "deepseek-v3.2",
                "thinking": {"type": "enabled"},
                "reasoning_effort": "high",
                "max_tokens": 8192,
                "temperature": 0.0,
            },
            return_envelope={
                "delegation_id": "del-test-001",
                "status": "COMPLETE",
                "acceptance_results": [],
                "steps_used": 3,
            },
            cache_hit=True,
            pruned_nodes=[],
        )
        print(json.dumps(record, indent=2))
    else:
        print("Use --record, --summary, or --write-readable")


if __name__ == "__main__":
    main()
