#!/usr/bin/env python3
"""Nemotron 3.5 adapter — dispatch configuration for NVIDIA Nemotron 3.5 Super VL.

Nemotron 3.5 reasoning effort levels:
  - high: enable_thinking: true alone
  - medium: enable_thinking: true + medium_effort: true
  - low: enable_thinking: false (or unset)

Per spec constraints:
  - reasoning_effort must be set (never unset)
  - max_tokens floor: 16384 (reasoning trace + plan output share this budget)
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

# Per-tier token floor (from spec constraints)
MAX_TOKENS_FLOOR = 16384


class Nemotron35Adapter:
    """Adapter for Nemotron 3.5 Super VL model dispatch."""

    def __init__(self):
        self.model = "nvidia/nemotron-3.5-super-vl-120b-a12b"

    def build_dispatch(
        self,
        target_tier: str,
        max_tokens: int | None = None,
        temperature: float = 0.6,
        extra_params: dict | None = None,
    ) -> dict[str, Any]:
        """Build dispatch parameters for Nemotron 3.5.

        Args:
            target_tier: "thinking" (manager), "low_thinking" or "non_thinking" (production)
            max_tokens: Requested max_tokens (must meet floor of 16384)
            temperature: Temperature for planning (default 0.6)
            extra_params: Additional parameters to merge

        Returns:
            Dispatch dict with model, enable_thinking, medium_effort, max_tokens, temperature

        Raises:
            ValueError: If max_tokens is below the floor
        """
        # Validate token floor
        if max_tokens is not None and max_tokens < MAX_TOKENS_FLOOR:
            raise ValueError(
                f"BUDGET_FLOOR_VIOLATION: Nemotron 3.5 requires max_tokens >= {MAX_TOKENS_FLOOR}, got {max_tokens}"
            )

        # Set default max_tokens if not provided
        if max_tokens is None:
            max_tokens = MAX_TOKENS_FLOOR

        # Reasoning effort mapping per spec constraints
        # high -> enable_thinking: true alone
        # medium -> enable_thinking: true + medium_effort: true
        # low -> enable_thinking: false
        is_manager = target_tier == "thinking"

        if is_manager:
            enable_thinking = True
            medium_effort = None
            reasoning_effort = "high"
        else:
            # Production tier: can use medium effort for lighter reasoning
            enable_thinking = True
            medium_effort = True
            reasoning_effort = "medium"

        dispatch = {
            "model": self.model,
            "enable_thinking": enable_thinking,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "reasoning_effort": reasoning_effort,
        }

        if medium_effort is not None:
            dispatch["medium_effort"] = medium_effort

        if extra_params:
            dispatch.update(extra_params)

        return dispatch

    def validate_dispatch(self, dispatch: dict[str, Any]) -> str | None:
        """Validate a dispatch dict. Returns None if OK, or BLOCKED reason string."""
        max_tokens = dispatch.get("max_tokens", 0)
        enable_thinking = dispatch.get("enable_thinking")

        if max_tokens < MAX_TOKENS_FLOOR:
            return f"BUDGET_FLOOR_VIOLATION: Nemotron 3.5 requires max_tokens >= {MAX_TOKENS_FLOOR}, got {max_tokens}"

        if enable_thinking is not True:
            return "REASONING_EFFORT_INVALID: Nemotron 3.5 requires enable_thinking: true"

        return None


def main():
    """CLI: test Nemotron 3.5 adapter dispatch."""
    import argparse
    import json

    ap = argparse.ArgumentParser(description="Nemotron 3.5 adapter test")
    ap.add_argument("--tier", default="thinking", help="Target tier: thinking, low_thinking, non_thinking")
    ap.add_argument("--max-tokens", type=int, default=None, help="Max tokens")
    args = ap.parse_args()

    adapter = Nemotron35Adapter()
    try:
        dispatch = adapter.build_dispatch(args.tier, args.max_tokens)
        print(json.dumps(dispatch, indent=2))
    except ValueError as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
