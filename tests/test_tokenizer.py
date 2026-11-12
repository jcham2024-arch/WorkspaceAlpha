#!/usr/bin/env python3
"""Tests for tokenizer module."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "assembly"))

from tokenizer import TokenCounter, HeuristicCounter, get_counter  # noqa: E402


class TestTokenizer:
    """Test tokenizer counter."""

    def test_heuristic_counter(self):
        """Heuristic counter counts bytes // 4."""
        counter = HeuristicCounter()
        text = "Hello, World!"
        expected = len(text.encode("utf-8")) // 4
        assert counter.count(text) == expected

    def test_heuristic_rejected_for_enforcement(self):
        """Heuristic counter rejected when enforce_budget=True."""
        counter = HeuristicCounter()
        try:
            counter.count("test", enforce_budget=True)
            assert False, "Should have raised ValueError"
        except ValueError as exc:
            assert "TOKEN_COUNTER_UNAVAILABLE" in str(exc)

    def test_get_counter_heuristic(self):
        """Get heuristic counter."""
        counter = get_counter("heuristic")
        assert isinstance(counter, HeuristicCounter)

    def test_get_counter_unknown(self):
        """Unknown counter type raises ValueError."""
        try:
            get_counter("nonexistent")
            assert False, "Should have raised ValueError"
        except ValueError as exc:
            assert "Unknown token counter type" in str(exc)


if __name__ == "__main__":
    import unittest
    unittest.main()
