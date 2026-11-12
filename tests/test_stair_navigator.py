#!/usr/bin/env python3
"""Tests for stair_navigator module."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".agent" / "tools"))

from stair_navigator import StairNavigator  # noqa: E402


class TestStairNavigator:
    """Test stair_navigator module."""

    def setUp(self):
        self.navigator = StairNavigator()

    def test_navigate_returns_result(self):
        """navigate() should return a result dict."""
        result = self.navigator.navigate("test query")
        assert isinstance(result, dict)
        assert "node_id" in result
        assert "path" in result
        assert "confidence" in result

    def test_navigate_empty_query(self):
        """Empty query should return empty result."""
        result = self.navigator.navigate("")
        assert result["node_id"] is None
        assert result["path"] == []
        assert result["confidence"] == 0.0


if __name__ == "__main__":
    import unittest
    unittest.main()
