#!/usr/bin/env python3
"""Tests for pattern_retriever module."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".agent" / "tools"))

from pattern_retriever import PatternRetriever  # noqa: E402


class TestPatternRetriever:
    """Test pattern_retriever module."""

    def setUp(self):
        self.retriever = PatternRetriever()

    def test_retrieve_returns_none_when_empty(self):
        """Empty pattern store should return None."""
        result = self.retriever.retrieve("test query", role="conceptualizer")
        assert result is None

    def test_worker_role_denied(self):
        """Worker role should be denied access to pattern retriever."""
        # First add a pattern so there's something to retrieve
        self.retriever.patterns = [
            {
                "pattern_id": "test-1",
                "skeleton": ["TYPE:TestFix"],
                "type_signature": "TYPE:Java",
                "similarity_score": 0.9,
            }
        ]
        result = self.retriever.retrieve("test query", role="worker")
        assert result is None

    def test_manager_role_returns_pattern(self):
        """Manager role should retrieve pattern."""
        self.retriever.patterns = [
            {
                "pattern_id": "test-1",
                "skeleton": ["TYPE:Java", "SYMPTOM:test_failure"],
                "type_signature": "TYPE:Java",
                "similarity_score": 0.9,
            }
        ]
        result = self.retriever.retrieve(
            "test query about Java test failure", role="manager"
        )
        assert result is not None
        assert result["pattern_id"] == "test-1"


if __name__ == "__main__":
    import unittest
    unittest.main()
