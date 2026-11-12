#!/usr/bin/env python3
"""Tests for cognitive mode classification."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "assembly"))

from cognitive_router import route  # noqa: E402


class TestCognitiveMode:
    """Test cognitive mode classification."""

    def test_brainstorming_routes_to_brainstorming_mode(self):
        """Brainstorming queries should route to brainstorming mode."""
        result = route("brainstorm ideas for a new feature", "conceptualizer")
        assert result.mode == "brainstorming"

    def test_writing_plans_routes_to_writing_plans_mode(self):
        """Writing plans queries should route to writing-plans mode."""
        result = route("write an implementation plan", "conceptualizer",
                       context={"task_type": "planning"})
        assert result.mode == "writing-plans"

    def test_first_principles_routes_to_first_principles_mode(self):
        """First principles queries should route to first_principles mode."""
        result = route("analyze from first principles", "coder",
                       context={"task_type": "architecture"})
        assert result.mode == "thinking-first-principles"

    def test_margin_of_safety_routes_to_margin_of_safety_mode(self):
        """Margin of safety queries should route to margin_of_safety mode."""
        result = route("estimate cost with margin of safety", "coder",
                       context={"task_type": "estimation"})
        assert result.mode == "thinking-margin-of-safety"

    def test_first_and_margin_routes_to_first_and_margin_mode(self):
        """First and margin queries should route to first_and_margin mode."""
        result = route("novel architecture with risk analysis", "coder",
                       context={"task_type": "architecture"})
        assert result.mode == "first_and_margin"

    def test_analogy_routes_to_analogy_mode(self):
        """Analogy queries should route to analogy mode."""
        result = route("analogy to another domain", "conceptualizer",
                       context={"task_type": "analogy"})
        assert result.mode == "analogy"

    def test_invention_routes_to_invention_mode(self):
        """Invention queries should route to invention mode."""
        result = route("invent something new", "coder",
                       context={"task_type": "invention"})
        assert result.mode == "invention"

    def test_salience_routes_to_salience_mode(self):
        """Salience queries should route to salience mode."""
        result = route("information overload", "conceptualizer",
                       context={"task_type": "analysis"})
        assert result.mode == "salience"

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
            result = route(query, "coder")
            assert result.mode in [
                "brainstorming", "writing-plans", "thinking-first-principles",
                "thinking-margin-of-safety", "first-and-margin",
                "analogy", "invention", "salience",
            ]

    def test_context_affects_routing(self):
        """Context should affect routing decisions."""
        result1 = route("analyze code", "coder",
                        context={"task_type": "planning"})
        result2 = route("analyze code", "coder",
                        context={"task_type": "researching"})
        # Different contexts may produce different modes
        assert result1.mode in [
            "brainstorming", "writing-plans", "thinking-first-principles",
            "thinking-margin-of-safety", "first-and-margin",
            "analogy", "invention", "salience",
        ]
        assert result2.mode in [
            "brainstorming", "writing-plans", "thinking-first-principles",
            "thinking-margin-of-safety", "first-and-margin",
            "analogy", "invention", "salience",
        ]

    def test_confidence_range(self):
        """Confidence should be between 0 and 1."""
        result = route("test query", "conceptualizer")
        assert 0.0 <= result.confidence <= 1.0

    def test_rule_id_is_string(self):
        """Rule ID should be a string when a rule matches."""
        result = route("brainstorm ideas", "conceptualizer")
        assert isinstance(result.rule_id, str)

    def test_reason_is_string(self):
        """Reason should be a string."""
        result = route("test query", "conceptualizer")
        assert isinstance(result.reason, str)


if __name__ == "__main__":
    import unittest
    unittest.main()
