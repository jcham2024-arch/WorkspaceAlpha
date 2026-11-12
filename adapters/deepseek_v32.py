#!/usr/bin/env python3
"""DeepSeek V3.2 adapter — dispatch configuration for DeepSeek V3.2 thinking model.

DeepSeek V3.2 is a reasoning-native model with a 128K context window. The `thinking`
parameter is disabled by default and must be explicitly set.

Manager tier (thinking):
  - thinking: {"type": "enabled"}
  - reasoning_effort: "high" or "max"
  - max_tokens: >= 8192 (reasoning trace consumes completion tokens)
  - temperature: 0.0

Production tier (non-thinking):
  - thinking: {"type": "disabled"}
  - max_tokens: >= 1024
  - temperature: 0.0
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

# Per-tier token floors (from spec §4.2)
MANAGER_MIN_TOKENS = 8192
PRODUCTION_MIN_TOKENS = 1024


class DeepSeekV32Adapter:
    """Adapter for DeepSeek V3.2 thinking model dispatch."""

    def __init__(self):
        self.model = "deepseek-v3.2-thinking"

    def build_dispatch(
        self,
        target_tier: str,
        max_tokens: int | None = None,
        temperature: float = 0.0,
        extra_params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build dispatch parameters for DeepSeek V3.2.

        Args:
            target_tier: "thinking" (manager), "low_thinking" or "non_thinking" (production)
            max_tokens: Requested max_tokens (must meet tier floor)
            temperature: Temperature (ignored in thinking mode)
            extra_params: Additional parameters to merge

        Returns:
            Dispatch dict with model, thinking, reasoning_effort, max_tokens, temperature

        Raises:
            ValueError: If max_tokens is below the tier floor
        """
        is_manager = target_tier == "thinking"

        # Validate token floor
        min_tokens = MANAGER_MIN_TOKENS if is_manager else PRODUCTION_MIN_TOKENS
        if max_tokens is not None and max_tokens < min_tokens:
            raise ValueError(
                f"BUDGET_FLOOR_VIOLATION: {target_tier} tier requires "
                f"max_tokens >= {min_tokens}, got {max_tokens}"
            )

        # Set default max_tokens if not provided
        if max_tokens is None:
            max_tokens = min_tokens

        dispatch = {
            "model": self.model,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if is_manager:
            # Manager tier: thinking enabled
            dispatch["thinking"] = {"type": "enabled"}
            dispatch["reasoning_effort"] = "high"
        else:
            # Production tier: thinking disabled
            dispatch["thinking"] = {"type": "disabled"}
            dispatch["reasoning_effort"] = None

        if extra_params:
            dispatch.update(extra_params)

        return dispatch

    def validate_dispatch(self, dispatch: dict[str, Any]) -> str | None:
        """Validate a dispatch dict. Returns None if OK, or BLOCKED reason string."""
        thinking = dispatch.get("thinking", {})
        if isinstance(thinking, dict):
            thinking_type = thinking.get("type")
        else:
            thinking_type = thinking

        max_tokens = dispatch.get("max_tokens", 0)
        reasoning_effort = dispatch.get("reasoning_effort")

        if thinking_type == "enabled":
            if max_tokens < MANAGER_MIN_TOKENS:
                return (
                    f"BUDGET_FLOOR_VIOLATION: manager tier requires max_tokens >= "
                    f"{MANAGER_MIN_TOKENS}, got {max_tokens}"
                )
            if reasoning_effort not in ("high", "max"):
                return (
                    f"REASONING_EFFORT_INVALID: manager tier requires reasoning_effort "
                    f"'high' or 'max', got {reasoning_effort}"
                )
        elif thinking_type == "disabled":
            if max_tokens < PRODUCTION_MIN_TOKENS:
                return (
                    f"BUDGET_FLOOR_VIOLATION: production tier requires max_tokens >= "
                    f"{PRODUCTION_MIN_TOKENS}, got {max_tokens}"
                )

        return None

    def capability_manifest(self) -> dict[str, Any]:
        """Return capability manifest for this adapter."""
        return {
            "model_id": "deepseek-v3.2-thinking",
            "provider": "deepseek",
            "context_window": 131072,
            "max_tokens_floor": MANAGER_MIN_TOKENS,
            "production_allowed": True,
            "reasoning_modes": ["thinking", "non_thinking"],
            "format_preferences": {
                "frozen_prefix": "xml_semantic_tags",
                "variable_suffix": "markdown_headings",
            },
            "conformance_suite": "factory/conformance/deepseek-v3.2.yaml",
        }

    def count_tokens(self, text: str, model_id: str | None = None) -> int:
        """Count tokens using a heuristic estimator (bytes // 4).

        Note: This is a heuristic estimate, not a precise token count.
        For accurate token counting, use tiktoken with cl100k_base encoding.
        """
        return len(text.encode("utf-8")) // 4


def main():
    """CLI: test DeepSeek V3.2 adapter dispatch."""
    import argparse
    import json

    ap = argparse.ArgumentParser(description="DeepSeek V3.2 adapter test")
    ap.add_argument("--tier", default="thinking", help="Target tier: thinking, low_thinking, non_thinking")
    ap.add_argument("--max-tokens", type=int, default=None, help="Max tokens")
    args = ap.parse_args()

    adapter = DeepSeekV32Adapter()
    try:
        dispatch = adapter.build_dispatch(args.tier, args.max_tokens)
        print(json.dumps(dispatch, indent=2))
    except ValueError as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
