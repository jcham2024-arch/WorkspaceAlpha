#!/usr/bin/env python3
"""Tests for adapter dispatch."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "adapters"))

from dispatch import AdapterDispatch  # noqa: E402


class TestAdapterDispatch:
    """Test adapter dispatch."""

    def setUp(self):
        self.dispatch = AdapterDispatch()

    def test_deepseek_dispatch(self):
        """Dispatch to DeepSeek V3.2 works."""
        result = self.dispatch.dispatch(
            model="deepseek-v3.2",
            target_tier="thinking",
            max_tokens=8192,
        )
        assert result["model"] == "deepseek-v3.2-thinking"
        assert result["thinking"] == {"type": "enabled"}
        assert result["reasoning_effort"] == "high"
        assert result["max_tokens"] == 8192

    def test_nemotron_dispatch(self):
        """Dispatch to Nemotron 3.5 works."""
        result = self.dispatch.dispatch(
            model="nemotron-3.5",
            target_tier="thinking",
            max_tokens=16384,
        )
        assert result["model"] == "nvidia/nemotron-3.5-super-vl-120b-a12b"
        assert result["enable_thinking"] is True

    def test_unknown_model_raises(self):
        """Unknown model raises ValueError."""
        try:
            self.dispatch.dispatch(
                model="unknown-model",
                target_tier="thinking",
                max_tokens=8192,
            )
            assert False, "Should have raised ValueError"
        except ValueError as exc:
            assert "Unknown model adapter" in str(exc)

    def test_production_unknown_model_blocked(self):
        """Production tier with unknown model is blocked."""
        try:
            self.dispatch.dispatch_with_fallback(
                model="unknown-model",
                target_tier="thinking",
                max_tokens=8192,
                delegation_type="EXECUTION",
                authority="EXECUTE",
            )
            assert False, "Should have raised ValueError"
        except ValueError as exc:
            assert "NO_ADAPTER_FOR_PRODUCTION_TIER" in str(exc)

    def test_non_production_unknown_model_generic(self):
        """Non-production tier with unknown model routes to generic."""
        result = self.dispatch.dispatch_with_fallback(
            model="unknown-model",
            target_tier="non_thinking",
            max_tokens=1024,
            delegation_type="MISSION",
            authority="ANALYZE",
        )
        assert result["resolved_adapter"] == "generic"
        assert result["fallback_used"] is True
        assert result["requested_model"] == "unknown-model"


if __name__ == "__main__":
    import unittest
    unittest.main()
