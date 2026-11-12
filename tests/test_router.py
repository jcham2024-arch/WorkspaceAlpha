#!/usr/bin/env python3
"""Tests for the router module."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "assembly"))

from router import route, RoutingDecision  # noqa: E402


class TestRouter:
    """Test the router module."""

    def test_brainstorming_query_routes_to_brainstorming_skill(self):
        """Query about brainstorming should route to skill-brainstorming via DIRECT protocol."""
        result = route(
            query="I need to brainstorm ideas for a new feature",
            profile="conceptualizer",
            context={"task_type": "brainstorming", "allowed_targets": []},
        )
        assert result.protocol == "DIRECT"
        assert result.node_id == "skill-brainstorming"
        assert result.confidence == 1.0

    def test_writing_plans_query_routes_to_writing_plans_skill(self):
        """Query about writing plans should route to skill-writing-plans via DIRECT protocol."""
        result = self.dispatch_query("I need to write an implementation plan", "conceptualizer", {"task_type": "planning", "allowed_targets": []})
        assert result.protocol == "DIRECT"
        assert result.node_id == "skill-writing-plans"

    def test_thinking_first_principles_query_routes_to_thinking_first_principles_skill(self):
        """Query about first principles should route to thinking-first-principles skill via DIRECT protocol."""
        result = self.dispatch_query(
            "analyze this problem from first principles", "conceptualizer",
            {"task_type": "reasoning", "allowed_targets": []}
        )
        assert result.protocol == "DIRECT"
        assert result.node_id == "skill-thinking-first-principles"

    def test_unknown_query_defaults_to_vector(self):
        """Query with no matching rule should default to VECTOR protocol."""
        result = self.dispatch_query(
            "some random query with no matching keywords", "conceptualizer",
            {"task_type": "general", "allowed_targets": []}
        )
        assert result.protocol == "VECTOR"
        assert result.node_id == "proto-vector"
        assert result.confidence == 0.5
        assert result.rule_id == "default"

    def test_role_based_pattern_routing(self):
        """Pattern protocol should only be available to manager-tier roles."""
        # Manager role with pattern match should route to PATTERN
        result = self.dispatch_query(
            "refactor this code", "taskmaster",
            {"role": "taskmaster", "gpm_top1_score_gte": 0.9, "allowed_targets": []}
        )
        assert result.protocol == "PATTERN"
        assert result.node_id == "proto-pattern"

        # Worker role with pattern match should NOT route to PATTERN (should fall back to VECTOR)
        result = self.dispatch_query(
            "refactor this code", "coder",
            {"role": "coder", "gpm_top1_score_gte": 0.9, "allowed_targets": []}
        )
        assert result.protocol != "PATTERN"

    def test_rule_order_matters(self):
        """First matching rule should win."""
        # brainstorming query matches both brainstorming and writing-plans rules potentially,
        # but brainstorming rule comes first
        result = self.dispatch_query(
            "brainstorm ideas for a new feature", "conceptualizer",
            {"task_type": "brainstorming", "allowed_targets": []}
        )
        assert result.protocol == "DIRECT"
        assert result.node_id == "skill-brainstorming"

    def dispatch_query(self, query: str, profile: str, context: dict) -> RoutingDecision:
        """Helper to dispatch a query through the router."""
        from router import route
        return route(query, profile=profile, context=context)


if __name__ == "__main__":
    import unittest
    unittest.main()
