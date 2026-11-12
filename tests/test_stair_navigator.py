#!/usr/bin/env python3
"""Tests for stair_navigator module."""

import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".agent" / "tools"))

from stair_navigator import navigate  # noqa: E402


class TestStairNavigator(unittest.TestCase):

    def test_navigate_returns_result(self):
        """navigate() should return a LeafPrediction with expected fields."""
        result = navigate("test query").to_dict()
        assert isinstance(result, dict)
        assert "node_id" in result
        assert "path" in result
        assert "confidence" in result

    def test_navigate_empty_query(self):
        """Empty query should return empty result."""
        result = navigate("").to_dict()
        assert result["node_id"] is None
        assert result["path"] == []
        assert result["confidence"] == 0.0


if __name__ == "__main__":
    import unittest
    unittest.main()
