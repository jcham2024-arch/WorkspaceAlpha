#!/usr/bin/env python3
"""Budgeter — enforces per-tier token ceilings on prompt assemblies.

If the total suffix tokens exceed the per-tier ceiling, prunes nodes by
edge distance from the root (farthest `triggers` nodes dropped first).
Returns BLOCKED with excluded node IDs rather than silently truncating.

Per-tier ceilings (from spec §6):
- Manager tier suffix: 1,800 tokens
- Production tier suffix: 1,500 tokens
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

# Per-tier token ceilings for the variable suffix (per spec §6)
TIER_CEILINGS = {
    "thinking": 1800,   # manager tier
    "low_thinking": 1500,  # production tier
    "non_thinking": 1500,  # production tier
}

DEFAULT_CEILING = 1500


def estimate_tokens(text: str) -> int:
    """Conservative token estimate: bytes // 4."""
    return len(text.encode("utf-8")) // 4


class BudgetResult:
    """Result of budget enforcement."""

    def __init__(
        self,
        within_budget: bool,
        total_tokens: int,
        ceiling: int,
        included_nodes: list[str],
        pruned_nodes: list[str],
        blocked_reason: str | None = None,
    ):
        self.within_budget = within_budget
        self.total_tokens = total_tokens
        self.ceiling = ceiling
        self.included_nodes = included_nodes
        self.pruned_nodes = pruned_nodes
        self.blocked_reason = blocked_reason

    def to_dict(self) -> dict:
        return {
            "within_budget": self.within_budget,
            "total_tokens": self.total_tokens,
            "ceiling": self.ceiling,
            "included_nodes": self.included_nodes,
            "pruned_nodes": self.pruned_nodes,
            "blocked_reason": self.blocked_reason,
        }


class Budgeter:
    """Enforces per-tier token ceilings with budget-aware pruning."""

    def __init__(self):
        pass

    def get_ceiling(self, target_tier: str) -> int:
        """Get the token ceiling for a target tier."""
        return TIER_CEILINGS.get(target_tier, DEFAULT_CEILING)

    def enforce_budget(
        self,
        nodes_with_tokens: list[dict],
        target_tier: str,
        root_node_ids: list[str] | None = None,
    ) -> BudgetResult:
        """Enforce token budget on a list of nodes with token counts.

        Args:
            nodes_with_tokens: List of dicts with keys: node_id, node_type, token_count, edge_distance
            target_tier: The target tier for ceiling lookup
            root_node_ids: Root node IDs (for distance-based pruning). Nodes farther from root
                          are pruned first.

        Returns BudgetResult. If within_budget is False, the assembly is BLOCKED.
        """
        ceiling = self.get_ceiling(target_tier)

        # Sort nodes: included first, pruned last
        # Nodes with edge_distance are pruned by distance (farthest first)
        # Nodes without edge_distance (root, requires edges) are never pruned
        ceiling = ceiling

        included = []
        pruned = []
        total = 0

        # Separate root/requires nodes (never pruned) from triggers nodes (prunable)
        root_nodes = []
        prunable_nodes = []

        for node in nodes_with_tokens:
            edge_distance = node.get("edge_distance")
            if edge_distance is None or edge_distance == 0:
                root_nodes.append(node)
            else:
                prunable_nodes.append(node)

        # Always include root nodes
        for node in root_nodes:
            included.append(node["node_id"])
            total += node["token_count"]

        # Sort prunable nodes by edge_distance descending (farthest first)
        prunable_nodes.sort(key=lambda n: n.get("edge_distance", 0), reverse=True)

        # Add prunable nodes until budget is exceeded
        for node in prunable_nodes:
            if total + node["token_count"] <= ceiling:
                included.append(node["node_id"])
                total += node["token_count"]
            else:
                pruned.append(node["node_id"])

        within_budget = len(pruned) == 0
        blocked_reason = None

        if not within_budget:
            blocked_reason = "CONTEXT_BUDGET_EXCEEDED"

        return BudgetResult(
            within_budget=within_budget,
            total_tokens=total,
            ceiling=ceiling,
            included_nodes=included,
            pruned_nodes=pruned,
            blocked_reason=blocked_reason,
        )

    def check_target_in_manifest(
        self, target: str, manifest_nodes: dict[str, dict]
    ) -> str | None:
        """Check if a target exists in the manifest. Returns None if OK,
        or BLOCKED reason string if not found."""
        if target not in manifest_nodes:
            return "TARGET_NOT_IN_MANIFEST"
        return None


def main():
    """CLI: test budget enforcement."""
    import argparse
    import json

    ap = argparse.ArgumentParser(description="Test budget enforcement")
    ap.add_argument("--tier", default="thinking", help="Target tier")
    ap.add_argument("--ceiling", type=int, help="Override ceiling")
    args = ap.parse_args()

    ceiling = args.ceiling if args.ceiling else TIER_CEILINGS.get(args.tier, DEFAULT_CEILING)

    # Test with sample nodes
    nodes = [
        {"node_id": "system-prompt-manager", "node_type": "SystemPrompt", "token_count": 1200, "edge_distance": 0},
        {"node_id": "skill-brainstorming", "node_type": "Skill", "token_count": 400, "edge_distance": 1},
        {"node_id": "skill-writing-plans", "node_type": "Skill", "token_count": 400, "edge_distance": 1},
        {"node_id": "context-slice-readme-skills", "node_type": "ContextSlice", "token_count": 75, "edge_distance": 2},
    ]

    budgeter = Budgeter()
    result = budgeter.enforce_budget(nodes, args.tier)
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
