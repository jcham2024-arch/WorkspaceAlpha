"""Single-prediction contract tests for stair_navigator (FIX_STAIR_LOOP_II §1).

These encode the invariants from FIX_STAIR_LOOP_II.md §1:
  1. navigate() makes exactly one dispatch call per invocation.
  2. No dispatch when the graph is empty.
  3. A prediction that fails manifest validation returns node_id=None with
     exactly one dispatch — no retry, no second prediction attempt.
  4. No while loop inside navigate().
  5. No keyword-scan fallback.
  6. No inline dispatcher.dispatch() call bypassing the dispatch module.

Written for unittest (pytest is not installed in this environment). The
directive's mocker.patch targets are translated to unittest.mock.patch
against the current seams: stair_navigator.dispatch_prediction,
stair_navigator._load_manifest, stair_toc.load_graph.
"""
from __future__ import annotations

import ast
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".agent" / "tools"))
sys.path.insert(0, str(ROOT / "adapters"))

from stair_navigator import LeafPrediction, navigate  # noqa: E402

NAV_SRC = (ROOT / ".agent" / "tools" / "stair_navigator.py").read_text()


class TestSinglePredictionContract(unittest.TestCase):
    """navigate() must dispatch exactly once per call."""

    def test_dispatch_called_exactly_once(self):
        """A single navigate() call results in exactly one dispatch call."""
        graph = {"nodes": [{"id": "some-node", "summary": "s"}]}
        manifest = {
            "nodes": [
                {
                    "id": "some-node",
                    "content_ref": "docs/README.md",
                    "byte_range": [0, 202],
                }
            ]
        }
        with patch("stair_navigator.dispatch_prediction") as dispatch_spy, patch(
            "stair_navigator._load_manifest", return_value=manifest
        ):
            dispatch_spy.return_value = {"node_id": "some-node", "confidence": 0.9}
            result = navigate("test query", graph=graph)

            self.assertEqual(
                dispatch_spy.call_count,
                1,
                f"Expected exactly 1 dispatch, got {dispatch_spy.call_count}. "
                "navigate() must be single-prediction.",
            )
        self.assertEqual(result.node_id, "some-node")

    def test_no_dispatch_when_graph_empty(self):
        """Empty graph returns None without dispatching."""
        with patch("stair_navigator.dispatch_prediction") as dispatch_spy:
            result = navigate("test query", graph={"nodes": []})
            self.assertIsNone(result.node_id)
            self.assertEqual(dispatch_spy.call_count, 0)

    def test_prediction_not_in_manifest_returns_none_no_retry(self):
        """Predicted node not in manifest -> None, one dispatch, no fallback."""
        graph = {"nodes": [{"id": "real-node"}, {"id": "other-node"}]}
        manifest = {"nodes": [{"id": "real-node"}, {"id": "other-node"}]}
        with patch("stair_navigator.dispatch_prediction") as dispatch_spy, patch(
            "stair_navigator._load_manifest", return_value=manifest
        ):
            dispatch_spy.return_value = {"node_id": "ghost-node", "confidence": 0.9}
            result = navigate("test query", graph=graph)

            self.assertIsNone(result.node_id)
            self.assertEqual(
                dispatch_spy.call_count,
                1,
                "A prediction that fails validation must not trigger a second "
                "prediction attempt.",
            )

    def test_low_confidence_returns_none_single_dispatch(self):
        """Below-threshold confidence returns None after one dispatch."""
        graph = {"nodes": [{"id": "some-node"}]}
        manifest = {"nodes": [{"id": "some-node"}]}
        with patch("stair_navigator.dispatch_prediction") as dispatch_spy, patch(
            "stair_navigator._load_manifest", return_value=manifest
        ):
            dispatch_spy.return_value = {"node_id": "some-node", "confidence": 0.3}
            result = navigate("test query", graph=graph)
            self.assertIsNone(result.node_id)
            self.assertEqual(dispatch_spy.call_count, 1)


    def test_empty_query_returns_none_bounded(self):
        """Empty graph or empty query returns None, bounded, no dispatch."""
        import time

        with patch("stair_navigator.dispatch_prediction") as dispatch_spy:
            start = time.monotonic()
            result = navigate("", graph={"nodes": []})
            elapsed = time.monotonic() - start
            self.assertIsNone(result.node_id)
            self.assertEqual(dispatch_spy.call_count, 0)
            self.assertLess(
                elapsed, 5, f"empty-query path took {elapsed:.2f}s — not bounded"
            )


class TestNoLoopConstructs(unittest.TestCase):
    """Static checks: the navigator must not contain loop constructs."""

    def test_no_while_in_navigate(self):
        tree = ast.parse(NAV_SRC)
        found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "navigate":
                found = True
                for inner in ast.walk(node):
                    self.assertNotIsInstance(
                        inner,
                        ast.While,
                        "navigate() contains a while loop — prediction must be "
                        "single-shot",
                    )
        self.assertTrue(found, "navigate() not found in stair_navigator.py")

    def test_no_while_anywhere_in_navigator(self):
        """The whole module is loop-free, not just navigate()."""
        tree = ast.parse(NAV_SRC)
        for node in ast.walk(tree):
            self.assertNotIsInstance(
                node, ast.While, "while loop in stair_navigator.py"
            )

    def test_no_keyword_fallback(self):
        """The keyword scan fallback must be removed, not just made conditional.

        Uses the two precise patterns from FIX_STAIR_LOOP.md Part IV.
        """
        self.assertNotIn(
            "query_lower",
            NAV_SRC,
            "Keyword fallback still present in stair_navigator.py",
        )
        self.assertNotIn(
            "query.lower()",
            NAV_SRC,
            "Keyword fallback still present in stair_navigator.py",
        )

    def test_no_linear_node_scan_in_navigate(self):
        """navigate() must not iterate over nodes to re-predict."""
        tree = ast.parse(NAV_SRC)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "navigate":
                for inner in ast.walk(node):
                    if isinstance(inner, ast.For):
                        raise AssertionError(
                            "navigate() contains a for loop over nodes — that is "
                            "the second prediction attempt (keyword scan)"
                        )

    def test_dispatch_is_the_only_dispatch_path(self):
        """The inline dispatcher.dispatch() call must be removed."""
        self.assertNotIn(
            "dispatcher.dispatch",
            NAV_SRC,
            "Inline dispatcher.dispatch() call present — route through the "
            "dispatch module only",
        )

    def test_dispatch_is_imported_not_inlined(self):
        """Dispatch must come from adapters.navigator, not be defined here."""
        self.assertIn("adapters.navigator", NAV_SRC)
        self.assertNotIn("def _dispatch_llm", NAV_SRC)

    def test_timeout_infrastructure_present(self):
        """The wall-clock cap must exist in the dispatch path."""
        nav_path = ROOT / "adapters" / "navigator.py"
        src = nav_path.read_text()
        self.assertIn("NavigatorTimeout", src)
        self.assertTrue(
            "SIGALRM" in src or "setitimer" in src or "alarm" in src,
            "No wall-clock timeout mechanism found in adapters/navigator.py",
        )


if __name__ == "__main__":
    unittest.main()
