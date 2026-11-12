#!/usr/bin/env python3
"""Tests for the stair_navigator public contract.

Fixed per FIX_STAIR_LOOP.md: navigate() returns a LeafPrediction, not a dict.
The earlier version asserted `isinstance(result, dict)` against a function that
returns LeafPrediction, which only passed because the test called .to_dict()
first — hiding the type it claimed to check.
"""

import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".agent" / "tools"))

from stair_navigator import LeafPrediction, navigate  # noqa: E402


class TestStairNavigator(unittest.TestCase):
    def test_navigate_returns_leaf_prediction(self):
        """navigate() returns a LeafPrediction, not a dict."""
        result = navigate("test query")
        self.assertIsInstance(result, LeafPrediction)
        self.assertNotIsInstance(result, dict)

    def test_result_exposes_contract_fields(self):
        """The LeafPrediction carries the fields the assembler needs."""
        result = navigate("test query")
        for field in ("node_id", "path", "confidence", "byte_range", "content_ref"):
            self.assertTrue(
                hasattr(result, field), f"LeafPrediction missing '{field}'"
            )
        payload = result.to_dict()
        for field in ("node_id", "path", "confidence"):
            self.assertIn(field, payload)

    def test_navigate_empty_query(self):
        """An empty query returns a None-node prediction, bounded."""
        result = navigate("")
        self.assertIsNone(result.node_id)
        self.assertEqual(result.path, [])
        self.assertEqual(result.confidence, 0.0)

    def test_navigate_is_bounded(self):
        """A real call completes well inside the wall-clock cap."""
        start = time.monotonic()
        navigate("According to ADR-004, what was the decision?")
        elapsed = time.monotonic() - start
        self.assertLess(
            elapsed, 20, f"navigate() took {elapsed:.2f}s — cap not working"
        )


if __name__ == "__main__":
    unittest.main()
