#!/usr/bin/env python3
"""Generic adapter — fallback for unknown models.

Generic adapter provides basic dispatch for unknown models:
- No thinking mode
- Lower token floor (1024)
- Markdown formatting
"""
from __future__ import annotations

from adapters.base import ModelAdapter, DispatchResult, ValidationResult, CapabilityManifest


class GenericAdapter(ModelAdapter):
    """Generic adapter for unknown models."""

    def __init__(self):
        self.model = "generic"

    def build_dispatch(
        self,
        target_tier: str,
        max_tokens: int | None = None,
        temperature: float = 0.0,
        extra_params: dict[str, Any] | None = None,
    ) -> DispatchResult:
        """Build dispatch parameters for generic model."""
        min_tokens = 1024
        if max_tokens is not None and max_tokens < min_tokens:
            raise ValueError(
                f"BUDGET_FLOOR_VIOLATION: generic tier requires max_tokens >= {min_tokens}, got {max_tokens}"
            )
        if max_tokens is None:
            max_tokens = min_tokens

        dispatch = {
            "model": self.model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "thinking": {"type": "disabled"},
            "reasoning_effort": None,
        }

        if extra_params:
            dispatch.update(extra_params)

        return DispatchResult(
            dispatch=dispatch,
            model=self.model,
            tier=target_tier,
            max_tokens=max_tokens,
            temperature=temperature,
            thinking={"type": "disabled"},
            reasoning_effort=None,
        )

    def validate_dispatch(self, dispatch: dict[str, Any]) -> str | None:
        """Validate dispatch dict."""
        max_tokens = dispatch.get("max_tokens", 0)
        if max_tokens < 1024:
            return f"BUDGET_FLOOR_VIOLATION: generic tier requires max_tokens >= 1024, got {max_tokens}"
        if dispatch.get("thinking", {}).get("type") == "enabled":
            return "REASONING_EFFORT_INVALID: generic tier does not support thinking mode"
        return None

    def capability_manifest(self) -> CapabilityManifest:
        """Return capability manifest."""
        return CapabilityManifest(
            model_id="generic",
            provider="generic",
            context_window=4096,
            max_tokens_floor=1024,
            production_allowed=False,
            reasoning_modes=["non_thinking"],
            format_preferences={
                "frozen_prefix": "markdown_headings",
                "variable_suffix": "markdown_headings",
            },
            conformance_suite="factory/conformance/generic.yaml",
        )

    def count_tokens(self, text: str, model_id: str | None = None) -> int:
        """Count tokens using heuristic."""
        return len(text.encode("utf-8")) // 4


def main():
    """CLI: test generic adapter."""
    import json

    adapter = GenericAdapter()
    dispatch = adapter.build_dispatch("thinking", max_tokens=1024)
    print(json.dumps(dispatch, indent=2))


if __name__ == "__main__":
    main()
