#!/usr/bin/env python3
"""Tests for model adapters (DeepSeek V3.2 and Nemotron 3.5).

Tests thinking mode, token floors, and dispatch validation.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTERS_DIR = ROOT / "adapters"
sys.path.insert(0, str(ADAPTERS_DIR))

from deepseek_v32 import DeepSeekV32Adapter  # noqa: E402
from nemotron_35 import Nemotron35Adapter  # noqa: E402


class TestDeepSeekAdapter(unittest.TestCase):
    """Test DeepSeek V3.2 adapter dispatch configuration."""

    def setUp(self):
        self.adapter = DeepSeekV32Adapter()

    def test_manager_thinking_enabled(self):
        """Manager tier (thinking) should have thinking.enabled."""
        dispatch = self.adapter.build_dispatch("thinking", max_tokens=8192)
        self.assertEqual(dispatch["model"], "deepseek-v3.2-thinking")
        self.assertEqual(dispatch["thinking"], {"type": "enabled"})
        self.assertEqual(dispatch["reasoning_effort"], "high")
        self.assertEqual(dispatch["max_tokens"], 8192)
        self.assertEqual(dispatch["temperature"], 0.0)

    def test_production_thinking_disabled(self):
        """Production tier should have thinking.disabled."""
        dispatch = self.adapter.build_dispatch("low_thinking", max_tokens=1024)
        self.assertEqual(dispatch["thinking"], {"type": "disabled"})
        self.assertEqual(dispatch["reasoning_effort"], None)
        self.assertEqual(dispatch["max_tokens"], 1024)
        self.assertEqual(dispatch["temperature"], 0.0)

    def test_manager_min_token_floor(self):
        """Manager tier max_tokens must be >= 8192."""
        with self.assertRaises(ValueError) as ctx:
            self.adapter.build_dispatch("thinking", max_tokens=4096)
        self.assertIn("BUDGET_FLOOR_VIOLATION", str(ctx.exception))

    def test_production_min_token_floor(self):
        """Production tier max_tokens must be >= 1024."""
        with self.assertRaises(ValueError) as ctx:
            self.adapter.build_dispatch("low_thinking", max_tokens=512)
        self.assertIn("BUDGET_FLOOR_VIOLATION", str(ctx.exception))

    def test_manager_default_max_tokens(self):
        """Manager tier defaults to 8192 max_tokens."""
        dispatch = self.adapter.build_dispatch("thinking")
        self.assertEqual(dispatch["max_tokens"], 8192)

    def test_production_default_max_tokens(self):
        """Production tier defaults to 1024 max_tokens."""
        dispatch = self.adapter.build_dispatch("low_thinking")
        self.assertEqual(dispatch["max_tokens"], 1024)

    def test_validate_dispatch_manager_valid(self):
        """Valid manager dispatch should pass validation."""
        dispatch = self.adapter.build_dispatch("thinking", max_tokens=8192)
        self.assertIsNone(self.adapter.validate_dispatch(dispatch))

    def test_validate_dispatch_manager_invalid(self):
        """Invalid manager dispatch (too few tokens) should be rejected."""
        dispatch = {
            "model": "deepseek-v3.2-thinking",
            "thinking": {"type": "enabled"},
            "reasoning_effort": "high",
            "max_tokens": 4096,
            "temperature": 0.0,
        }
        reason = self.adapter.validate_dispatch(dispatch)
        self.assertIsNotNone(reason)
        self.assertIn("BUDGET_FLOOR_VIOLATION", reason)

    def test_validate_dispatch_production_invalid(self):
        """Invalid production dispatch (too few tokens) should be rejected."""
        dispatch = {
            "model": "deepseek-v3.2-thinking",
            "thinking": {"type": "disabled"},
            "reasoning_effort": None,
            "max_tokens": 512,
            "temperature": 0.0,
        }
        reason = self.adapter.validate_dispatch(dispatch)
        self.assertIsNotNone(reason)
        self.assertIn("BUDGET_FLOOR_VIOLATION", reason)


class TestNemotronAdapter(unittest.TestCase):
    """Test Nemotron 3.5 adapter dispatch configuration."""

    def setUp(self):
        self.adapter = Nemotron35Adapter()

    def test_manager_high_effort(self):
        """Manager tier (thinking) should have enable_thinking: true, no medium_effort."""
        dispatch = self.adapter.build_dispatch("thinking", max_tokens=16384)
        self.assertEqual(dispatch["model"], "nvidia/nemotron-3.5-super-vl-120b-a12b")
        self.assertEqual(dispatch["enable_thinking"], True)
        self.assertIsNone(dispatch.get("medium_effort"))
        self.assertEqual(dispatch["reasoning_effort"], "high")
        self.assertEqual(dispatch["max_tokens"], 16384)

    def test_production_medium_effort(self):
        """Production tier should have enable_thinking: true + medium_effort: true."""
        dispatch = self.adapter.build_dispatch("low_thinking", max_tokens=16384)
        self.assertEqual(dispatch["enable_thinking"], True)
        self.assertEqual(dispatch["medium_effort"], True)
        self.assertEqual(dispatch["reasoning_effort"], "medium")
        self.assertEqual(dispatch["max_tokens"], 16384)

    def test_max_tokens_floor(self):
        """Nemotron 3.5 requires max_tokens >= 16384."""
        with self.assertRaises(ValueError) as ctx:
            self.adapter.build_dispatch("thinking", max_tokens=8192)
        self.assertIn("BUDGET_FLOOR_VIOLATION", str(ctx.exception))

    def test_default_max_tokens_is_floor(self):
        """Default max_tokens should be 16384."""
        dispatch = self.adapter.build_dispatch("thinking")
        self.assertEqual(dispatch["max_tokens"], 16384)

    def test_validate_dispatch_valid(self):
        """Valid dispatch should pass validation."""
        dispatch = self.adapter.build_dispatch("thinking", max_tokens=16384)
        self.assertIsNone(self.adapter.validate_dispatch(dispatch))

    def test_validate_dispatch_invalid_floor(self):
        """Dispatch below floor should be rejected."""
        dispatch = {
            "model": "nvidia/nemotron-3.5-super-vl-120b-a12b",
            "enable_thinking": True,
            "max_tokens": 8192,
            "temperature": 0.6,
            "reasoning_effort": "high",
        }
        reason = self.adapter.validate_dispatch(dispatch)
        self.assertIsNotNone(reason)
        self.assertIn("BUDGET_FLOOR_VIOLATION", reason)

    def test_validate_dispatch_invalid_thinking(self):
        """Dispatch with enable_thinking: false should be rejected."""
        dispatch = {
            "model": "nvidia/nemotron-3.5-super-vl-120b-a12b",
            "enable_thinking": False,
            "max_tokens": 16384,
            "temperature": 0.6,
            "reasoning_effort": "high",
        }
        reason = self.adapter.validate_dispatch(dispatch)
        self.assertIsNotNone(reason)
        self.assertIn("REASONING_EFFORT_INVALID", reason)


class TestAdapterDispatch(unittest.TestCase):
    """Test the adapter dispatch selector."""

    def setUp(self):
        from adapters.dispatch import AdapterDispatch

        self.dispatch = AdapterDispatch()

    def test_deepseek_dispatch(self):
        """Dispatch to DeepSeek V3.2 should work."""
        result = self.dispatch.dispatch(
            model="deepseek-v3.2",
            target_tier="thinking",
            max_tokens=8192,
        )
        self.assertEqual(result["model"], "deepseek-v3.2-thinking")
        self.assertEqual(result["thinking"], {"type": "enabled"})

    def test_nemotron_dispatch(self):
        """Dispatch to Nemotron 3.5 should work."""
        result = self.dispatch.dispatch(
            model="nemotron-3.5",
            target_tier="thinking",
            max_tokens=16384,
        )
        self.assertEqual(result["model"], "nvidia/nemotron-3.5-super-vl-120b-a12b")
        self.assertEqual(result["enable_thinking"], True)

    def test_unknown_model_raises(self):
        """Unknown model should raise ValueError."""
        with self.assertRaises(ValueError):
            self.dispatch.dispatch(
                model="unknown-model",
                target_tier="thinking",
                max_tokens=8192,
            )

    def test_validate_dispatch_deepseek(self):
        """Validate DeepSeek dispatch."""
        dispatch = self.dispatch.dispatch(
            model="deepseek-v3.2",
            target_tier="thinking",
            max_tokens=8192,
        )
        reason = self.dispatch.validate_dispatch("deepseek-v3.2", dispatch)
        self.assertIsNone(reason)

    def test_validate_dispatch_nemotron(self):
        """Validate Nemotron dispatch."""
        dispatch = self.dispatch.dispatch(
            model="nemotron-3.5",
            target_tier="thinking",
            max_tokens=16384,
        )
        reason = self.dispatch.validate_dispatch("nemotron-3.5", dispatch)
        self.assertIsNone(reason)


if __name__ == "__main__":
    unittest.main()
