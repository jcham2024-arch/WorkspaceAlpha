#!/usr/bin/env python3
"""Adapter dispatch — selects the model adapter by target_tier and attaches
envelope frontmatter (not sent to model) alongside the two-zone prompt.

Stdlib only. Never writes .context/manifest.json or wiki/.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

# Add adapters directory to path for sibling imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from deepseek_v32 import DeepSeekV32Adapter  # noqa: E402
from nemotron_35 import Nemotron35Adapter  # noqa: E402


class AdapterDispatch:
    """Dispatches to the correct model adapter based on target_tier."""

    def __init__(self):
        self._adapters = {
            "deepseek-v3.2": DeepSeekV32Adapter(),
            "nemotron-3.5": Nemotron35Adapter(),
        }

    def get_adapter(self, model: str):
        """Get an adapter by model name. Raises ValueError if not found."""
        if model not in self._adapters:
            raise ValueError(f"Unknown model adapter: {model}")
        return self._adapters[model]

    def dispatch(
        self,
        model: str,
        target_tier: str,
        max_tokens: int | None = None,
        temperature: float = 0.0,
        extra_params: dict | None = None,
    ) -> dict[str, Any]:
        """Build dispatch parameters for a model and tier.

        Args:
            model: Model name ("deepseek-v3.2" or "nemotron-3.5")
            target_tier: Target tier ("thinking", "low_thinking", "non_thinking")
            max_tokens: Requested max_tokens
            temperature: Temperature
            extra_params: Additional parameters

        Returns:
            Dispatch dict

        Raises:
            ValueError: If model unknown or budget floor violated
        """
        adapter = self.get_adapter(model)
        return adapter.build_dispatch(
            target_tier=target_tier,
            max_tokens=max_tokens,
            temperature=temperature,
            extra_params=extra_params,
        )

    def validate_dispatch(
        self, model: str, dispatch: dict[str, Any]
    ) -> str | None:
        """Validate a dispatch dict for a model. Returns None if OK, or BLOCKED reason."""
        adapter = self.get_adapter(model)
        return adapter.validate_dispatch(dispatch)


def main():
    """CLI: test adapter dispatch."""
    import argparse
    import json

    ap = argparse.ArgumentParser(description="Adapter dispatch test")
    ap.add_argument("--model", default="deepseek-v3.2", help="Model: deepseek-v3.2, nemotron-3.5")
    ap.add_argument("--tier", default="thinking", help="Target tier")
    ap.add_argument("--max-tokens", type=int, default=None, help="Max tokens")
    args = ap.parse_args()

    dispatch = AdapterDispatch()
    try:
        result = dispatch.dispatch(
            model=args.model,
            target_tier=args.tier,
            max_tokens=args.max_tokens,
        )
        print(json.dumps(result, indent=2))
    except ValueError as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
