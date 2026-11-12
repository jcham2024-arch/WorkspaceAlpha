#!/usr/bin/env python3
"""Cognitive Router — classifies tasks into cognitive modes.

Reads `.context/cognitive-modes.json` and evaluates rules in order.
The first matching rule determines the cognitive mode. Falls back to
the default mode if no rule matches.

Routing decision is deterministic: same query + role always yields the
same mode. No LLM calls are made during routing; rule matching is purely
string/pattern based.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / ".context" / "cognitive-modes.json"


class CognitiveRouter:
    """Result of routing a task to a cognitive mode."""

    def __init__(
        self,
        mode: str,
        confidence: float,
        rule_id: str | None = None,
        reason: str | None = None,
    ):
        self.mode = mode
        self.confidence = confidence
        self.rule_id = rule_id
        self.reason = reason or ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "confidence": self.confidence,
            "rule_id": self.rule_id,
            "reason": self.reason,
        }


def _matches_condition(query: str, context: dict[str, Any], match: dict[str, Any]) -> bool:
    """Evaluate a single match condition against query + context."""
    for key, expected in match.items():
        if key == "query_mentions":
            if not expected:
                continue
            query_lower = query.lower()
            if not any(term.lower() in query_lower for term in expected):
                return False
        elif key == "task_type":
            if expected:
                task_type = context.get("task_type", "")
                if task_type not in expected:
                    return False
        elif key == "role":
            if expected:
                role = context.get("role", "")
                if isinstance(expected, list):
                    if role not in expected:
                        return False
                elif role != expected:
                    return False
        else:
            # Unknown match key — fail closed
            return False
    return True


def route(
    query: str,
    *,
    profile: str = "conceptualizer",
    context: dict[str, Any] | None = None,
) -> CognitiveMode:
    """Route a task to a cognitive mode.

    Args:
        query: The user query string.
        profile: The agent profile (conceptualizer, taskmaster, coder,
            researcher, reviewer, etc.).
        context: Additional context (task_type, domain, allowed_targets,
            target_tier, etc.).

    Returns:
        CognitiveMode with mode, confidence, rule_id, and reason.

    Raises:
        FileNotFoundError: If cognitive-modes.json does not exist.
    """
    context = context or {}

    # Load rules
    if not RULES_PATH.exists():
        raise FileNotFoundError(f"Cognitive modes not found: {RULES_PATH}")

    with RULES_PATH.open("r", encoding="utf-8") as f:
        rules_config = json.load(f)

    modes = rules_config.get("modes", {})
    default_mode = rules_config.get("default_mode", "first_principles")
    rules = rules_config.get("rules", [])

    # Evaluate rules in order
    for rule in rules:
        match = rule.get("match", {})
        if _matches_condition(query, context, match):
            mode = rule.get("mode", default_mode)
            rule_id = rule.get("id", "unknown")
            reason = f"Matched rule '{rule_id}': {match}"

            return CognitiveMode(
                mode=mode,
                confidence=1.0,
                rule_id=rule_id,
                reason=reason,
            )

    # No rule matched — use default mode
    mode = default_mode
    return CognitiveMode(
        mode=mode,
        confidence=0.5,  # Low confidence for default fallback
        rule_id="default",
        reason=f"No rule matched; defaulting to {mode}",
    )


def main():
    """CLI: test the cognitive router."""
    import argparse

    ap = argparse.ArgumentParser(description="Cognitive router test")
    ap.add_argument("query", help="Query to route")
    ap.add_argument(
        "--profile",
        default="conceptualizer",
        help="Agent profile name (conceptualizer, taskmaster, coder, researcher, reviewer)",
    )
    ap.add_argument(
        "--target-tier",
        default="thinking",
        help="Target tier (thinking, low_thinking, non_thinking)",
    )
    args = ap.parse_args()

    context = {
        "delegation_type": getattr(args, "delegation_type", ""),
        "target_tier": args.target_tier,
        "allowed_targets": args.allowed_targets if hasattr(args, "allowed_targets") else [],
    }

    decision = route(args.query, profile=args.profile, context=context)
    print(json.dumps(decision.to_dict(), indent=2))


if __name__ == "__main__":
    main()
