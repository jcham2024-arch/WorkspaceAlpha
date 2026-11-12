"""Regression tests for the STAIR navigator single-prediction contract.

These tests are the ratchet: they would have caught the loop before it was
observed. Run with: python -m unittest tests.stair.<module>
"""
from __future__ import annotations

import os
import sys
import time
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".agent" / "tools"))
sys.path.insert(0, str(ROOT / "adapters"))

from adapters.navigator import NavigatorTimeout  # noqa: E402
from stair_navigator import navigate  # noqa: E402
from stair_validate import ManifestDriftError, hydrate  # noqa: E402

LEAF_FIXTURE = ROOT / "tests" / "fixtures" / "stair" / "leaf.txt"
MULTIBYTE_FIXTURE = ROOT / "tests" / "fixtures" / "stair" / "multibyte.md"


class TestSinglePrediction(unittest.TestCase):
    """Test 1 — low confidence returns None-node in exactly one dispatch call."""

    def test_low_confidence_returns_without_retry(self):
        manifest = {
            "nodes": [
                {
                    "id": "some-node",
                    "content_ref": str(LEAF_FIXTURE),
                    "byte_range": [0, 10],
                }
            ]
        }
        with patch("stair_navigator.dispatch_prediction") as mock_dispatch:
            mock_dispatch.return_value = {
                "node_id": "some-node",
                "confidence": 0.3,
            }
            result = navigate("query", manifest=manifest)
            self.assertIsNone(result.node_id)
            self.assertEqual(mock_dispatch.call_count, 1)


class TestManifestDrift(unittest.TestCase):
    """Test 2 — manifest drift raises ManifestDriftError, never loops."""

    def test_manifest_drift_raises(self):
        graph = {"nodes": [{"id": "a"}, {"id": "b"}]}
        manifest = {"nodes": [{"id": "a"}]}  # missing 'b'
        with patch("stair_navigator.dispatch_prediction") as mock_dispatch:
            mock_dispatch.return_value = {"node_id": "b", "confidence": 0.9}
            with self.assertRaises(ManifestDriftError) as ctx:
                navigate("query", manifest=manifest, graph=graph)
            self.assertIn("b", str(ctx.exception))
        self.assertEqual(mock_dispatch.call_count, 1)


class TestMultibyteHydration(unittest.TestCase):
    """Test 3 — byte-range hydration is byte-correct with multibyte UTF-8."""

    def test_hydrate_multibyte(self):
        content = "caf\u00e9\u2014na\u00efve\u2014r\u00e9sum\u00e9".encode("utf-8")
        node = {
            "content_ref": str(MULTIBYTE_FIXTURE),
            "byte_range": [9, len(content)],
        }
        result = hydrate(node)
        self.assertEqual(result.encode("utf-8"), content[9:])


class TestAdapterTimeout(unittest.TestCase):
    """Test 4 — adapter timeout raises NavigatorTimeout without retry."""

    def test_adapter_timeout_raises_without_retry(self):
        import adapters.navigator as anav

        saved_timeout = anav.TIMEOUT_SECONDS
        anav.TIMEOUT_SECONDS = 0.3
        calls = []

        def slow_dispatch(*a, **kw):
            calls.append(1)
            time.sleep(2)
            return {}

        try:
            with patch("adapters.navigator.AdapterDispatch.dispatch", slow_dispatch):
                with self.assertRaises(NavigatorTimeout):
                    anav.dispatch_prediction("q", {}, max_depth=6)
        finally:
            anav.TIMEOUT_SECONDS = saved_timeout

        self.assertEqual(len(calls), 1)


class TestNoRetryStatic(unittest.TestCase):
    """Test 5 — static check: no while loops or recursion in navigator."""

    def test_no_while_or_recursion_in_navigator(self):
        import ast

        src = (ROOT / ".agent" / "tools" / "stair_navigator.py").read_text()
        tree = ast.parse(src)
        for node in ast.walk(tree):
            self.assertNotIsInstance(node, ast.While)
            if isinstance(node, ast.FunctionDef) and node.name == "navigate":
                for inner in ast.walk(node):
                    if isinstance(inner, ast.Call):
                        if (
                            isinstance(inner.func, ast.Name)
                            and inner.func.id == "navigate"
                        ):
                            self.fail("navigate() calls itself — recursive")


class TestWallClockCap(unittest.TestCase):
    """Test 6 — a wedged dispatch is capped by the wall clock, not completed."""

    def test_navigate_wall_clock_cap(self):
        import adapters.navigator as anav

        saved_timeout = anav.TIMEOUT_SECONDS
        anav.TIMEOUT_SECONDS = 0.3

        def slow_dispatch(*a, **kw):
            time.sleep(2)
            return {}

        try:
            with patch("adapters.navigator.AdapterDispatch.dispatch", slow_dispatch):
                manifest = {"nodes": []}
                start = time.monotonic()
                with self.assertRaises(NavigatorTimeout):
                    navigate("query", manifest=manifest)
                elapsed = time.monotonic() - start
        finally:
            anav.TIMEOUT_SECONDS = saved_timeout

        self.assertLess(elapsed, 5)


if __name__ == "__main__":
    unittest.main()
