#!/usr/bin/env python3
"""Tests for cognitive_router module."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "assembly"))

from cognitive_router import CognitiveRouter  # noqa: E402


class TestCognitiveRouter:
    """Test the cognitive router."""

    def setup_method(self):
        self.router = CognitiveRouter()

    def test_router_returns_valid_mode(self):
        """router() should return a valid cognitive mode."""
        result = self.router.route("How do I debug this Python code?")
        assert result.mode in [
            "retrieval", "first_principles", "margin_of_safety",
            "first_and_margin", "analogy", "invention", "salience"
        ]

    def test_brainstorming_query_routes_to_brainstorming(self):
        """Brainstorming queries should route to brainstorming mode."""
        result = self.router.route("brainstorm ideas for a new feature", "conceptualizer")
        assert result.mode == "brainstorming"

    def test_writing_plans_query_routes_to_writing_plans(self):
        """Writing plans queries should route to writing-plans mode."""
        result = self.router.route("write an implementation plan", "conceptualizer",
                                   context={"task_type": "planning"})
        assert result.mode == "writing-plans"

    def test_first_principles_query_routes_to_first_principles(self):
        """First principles queries should route to first_principles mode."""
        result = self.router.route("analyze from first principles", "coder",
                                   context={"task_type": "architecture"})
        assert result.mode == "thinking-first-principles"

    def test_router_returns_valid_mode_for_all_queries(self):
        """Router should always return a valid mode for any query."""
        test_queries = [
            "brainstorm ideas",
            "write a plan",
            "analyze from first principles",
            "estimate cost with margin of safety",
            "analogy to another domain",
            "invent something new",
            "find relevant information",
            "unknown query type",
        ]
        for query in test_queries:
            result = self.router.route(query, "coder")
            assert result.mode in [
                "brainstorming", "writing-plans", "thinking-first-principles",
                "thinking-margin-of-safety", "first-and-margin",
                "analogy", "invention", "salience",
            ]

    def test_context_affects_routing(self):
        """Context should affect routing decisions."""
        result1 = self.router.route("analyze code", "coder",
                                    context={"task_type": "planning"})
        result2 = self.router.route("analyze code", "coder",
                                    context={"task_type": "researching"})
        assert result1.mode != result_mode or result2.mode in [
            "thinking-first-principles", "analysis",
        ]

    def test_confidence_range(self):
        """Confidence should be between 0 and 1."""
        result = self.router.route("test query", "conceptualizer")
        assert 0.0 <= result.confidence <= 1.0

    def test_rule_id_is_string(self):
        """Rule ID should be a string when a rule matches."""
        result = self.router.route("brainstorm ideas", "conceptualizer")
        assert isinstance(result.rule_id, str)

    def test_reason_is_string(self):
        """Reason should be a string."""
        result = self.router.route("test query", "conceptualizer")
        assert isinstance(result.reason, str)


if __name__ == "__main__":
    import unittest
    unittest.main()
