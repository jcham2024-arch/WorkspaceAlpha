#!/usr/bin/env python3
"""Tests for provenance recorder."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "provenance"))

from recorder import ProvenanceRecorder  # noqa: E402


class TestProvenanceRecorder(unittest.TestCase):
    """Test provenance recorder."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.recorder = ProvenanceRecorder(Path(self.tmpdir))

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir)

    def test_record_and_retrieve(self):
        """Record a turn and retrieve it."""
        record = self.recorder.record_turn(
            delegation_id="del-test-001",
            from_agent="conceptualizer",
            to_agent="taskmaster",
            delegation_type="MISSION",
            target_tier="thinking",
            assembled_nodes=[
                {"node_id": "system-prompt-orchestrator", "node_type": "SystemPrompt", "token_count": 1200, "cache_hit": True},
                {"node_id": "skill-brainstorming", "node_type": "Skill", "token_count": 400, "cache_hit": False},
            ],
            token_counts={"prefix_tokens": 1200, "suffix_tokens": 400, "total_tokens": 1600, "ceiling_tokens": 1800, "budget_exceeded": False},
            adapter_params={"model": "deepseek-v3.2", "thinking": {"type": "enabled"}, "reasoning_effort": "high", "max_tokens": 8192, "temperature": 0.0},
            return_envelope={"delegation_id": "del-test-001", "status": "COMPLETE", "acceptance_results": [], "steps_used": 3},
            cache_hit=True,
            pruned_nodes=[],
        )

        self.assertEqual(record["delegation_id"], "del-test-001")
        self.assertEqual(record["from_agent"], "conceptualizer")
        self.assertEqual(record["to_agent"], "taskmaster")
        self.assertEqual(record["target_tier"], "thinking")
        self.assertEqual(record["cache_hit"], True)

    def test_get_summary(self):
        """Get summary for a delegation."""
        self.recorder.record_turn(
            delegation_id="del-test-002",
            from_agent="conceptualizer",
            to_agent="taskmaster",
            delegation_type="EXECUTION",
            target_tier="low_thinking",
            assembled_nodes=[],
            token_counts={"prefix_tokens": 500, "suffix_tokens": 300, "total_tokens": 800, "ceiling_tokens": 1500, "budget_exceeded": False},
            adapter_params={"model": "nemotron-3.5", "thinking": {"type": "disabled"}, "reasoning_effort": None, "max_tokens": 16384, "temperature": 0.6},
            return_envelope={"delegation_id": "del-test-002", "status": "COMPLETE", "acceptance_results": [], "steps_used": 2},
            cache_hit=False,
            pruned_nodes=[],
        )

        summary = self.recorder.get_summary("del-test-002")
        self.assertIsNotNone(summary)
        self.assertEqual(summary["delegation_id"], "del-test-002")
        self.assertEqual(summary["from_agent"], "conceptualizer")
        self.assertEqual(summary["to_agent"], "taskmaster")
        self.assertEqual(summary["final_status"], "COMPLETE")

    def test_get_turns_nonexistent(self):
        """Get turns for nonexistent delegation returns empty."""
        records = self.recorder.get_turns(delegation_id="del-nonexistent")
        self.assertEqual(records, [])

    def test_debug_trace_not_recorded_by_default(self):
        """Debug trace is not recorded unless sampled."""
        self.recorder.record_turn(
            delegation_id="del-test-003",
            from_agent="conceptualizer",
            to_agent="taskmaster",
            delegation_type="MISSION",
            target_tier="thinking",
            assembled_nodes=[],
            token_counts={"prefix_tokens": 100, "suffix_tokens": 50, "total_tokens": 150, "ceiling_tokens": 1800, "budget_exceeded": False},
            adapter_params={"model": "deepseek-v3.2", "thinking": {"type": "enabled"}, "reasoning_effort": "high", "max_tokens": 8192, "temperature": 0.0},
            return_envelope={"delegation_id": "del-test-003", "status": "COMPLETE", "acceptance_results": [], "steps_used": 1},
            cache_hit=False,
            pruned_nodes=[],
            sampled=False,  # Not sampled
        )

        traces = self.recorder.get_debug_traces(delegation_id="del-test-003")
        self.assertEqual(len(traces), 0)

    def test_debug_trace_recorded_when_sampled(self):
        """Debug trace is recorded when sampled."""
        self.recorder.record_turn(
            delegation_id="del-test-004",
            from_agent="conceptualizer",
            to_agent="taskmaster",
            delegation_type="MISSION",
            target_tier="thinking",
            assembled_nodes=[],
            token_counts={"prefix_tokens": 100, "suffix_tokens": 50, "total_tokens": 150, "ceiling_tokens": 1800, "budget_exceeded": False},
            adapter_params={"model": "deepseek-v3.2", "thinking": {"type": "enabled"}, "reasoning_effort": "high", "max_tokens": 8192, "temperature": 0.0},
            return_envelope={"delegation_id": "del-test-004", "status": "COMPLETE", "acceptance_results": [], "steps_used": 1},
            cache_hit=False,
            pruned_nodes=[],
            redacted_prompt="[REDACTED:SECRET] is the key",
            model_response="I cannot help with that request",
            sampled=True,
            sample_rate=1.0,
        )

        traces = self.recorder.get_debug_traces(delegation_id="del-test-004")
        self.assertEqual(len(traces), 1)
        self.assertEqual(traces[0]["redacted_prompt"], "[REDACTED:SECRET] is the key")
        self.assertEqual(traces[0]["model_response"], "I cannot help with that request")


if __name__ == "__main__":
    unittest.main()
