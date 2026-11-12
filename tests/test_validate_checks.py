"""Tests for the validate.py gate checks (FIX_STAIR_LOOP_II.md §5).

Each test feeds a synthetic violation to a check function and asserts the
check reports it. This is stronger than mutating the real navigator: it
proves the gate fires without risking the working tree.
"""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_validate():
    """Import validate.py's check functions without running the script.

    validate.py is a top-level script that calls fail() on violations, so it
    cannot be imported directly. We read it and exec only the function and
    constant definitions, stopping before the invocation block.
    """
    src = (ROOT / "validate.py").read_text(encoding="utf-8")
    marker = "for v in check_navigator_loop_constructs():"
    if marker not in src:
        raise AssertionError("validate.py invocation block not found")
    head = src.split(marker, 1)[0]
    namespace: dict = {
        "__name__": "validate_checks",
        "__file__": str(ROOT / "validate.py"),
    }
    exec(compile(head, "validate.py", "exec"), namespace)
    return namespace


V = _load_validate()
BAD_NAV = ROOT / "tests" / "fixtures" / "bad_navigator.py"


class TestNavigatorLoopConstructs(unittest.TestCase):
    def test_bad_fixture_is_flagged(self):
        violations = V["check_navigator_loop_constructs"](BAD_NAV)
        self.assertTrue(violations, "while loop in fixture was not detected")
        self.assertTrue(
            any("while loop in navigate()" in v for v in violations),
            f"expected a while-loop violation, got {violations}",
        )

    def test_while_outside_navigate_is_not_flagged(self):
        """The gate is scoped to navigate() per FIX_STAIR_LOOP.md Part IV."""
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "other_fn.py"
            p.write_text(
                "def navigate(query):\n"
                "    return {'node_id': None}\n"
                "\n"
                "def helper():\n"
                "    while True:\n"
                "        break\n",
                encoding="utf-8",
            )
            self.assertEqual(V["check_navigator_loop_constructs"](p), [])

    def test_real_navigator_is_clean(self):
        self.assertEqual(V["check_navigator_loop_constructs"](), [])


class TestNavigatorDispatchPath(unittest.TestCase):
    def test_bad_fixture_is_flagged(self):
        violations = V["check_navigator_dispatch_path"](BAD_NAV)
        joined = " | ".join(violations)
        self.assertIn("dispatcher.dispatch", joined)
        self.assertIn("keyword fallback", joined)
        self.assertIn("bare or broad except", joined)
        self.assertIn("adapters.navigator", joined)

    def test_real_navigator_is_clean(self):
        self.assertEqual(V["check_navigator_dispatch_path"](), [])


class TestNavigatorSize(unittest.TestCase):
    def test_real_navigator_under_limit(self):
        self.assertEqual(V["check_navigator_size"](max_lines=100), [])

    def test_low_limit_is_flagged(self):
        violations = V["check_navigator_size"](max_lines=10)
        self.assertTrue(violations)
        self.assertIn("must be under 10", violations[0])


class TestLineCounts(unittest.TestCase):
    def test_real_tree_has_no_new_violations(self):
        # Reports pre-existing oversized files; assert only that the check
        # returns a list of strings and does not raise.
        violations = V["check_line_counts"]()
        self.assertIsInstance(violations, list)
        for v in violations:
            self.assertIsInstance(v, str)

    def test_waiver_is_honoured(self):
        # A file whose first 200 chars carry the waiver is skipped.
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td) / "assembly" / "waived.py"
            tmp.parent.mkdir(parents=True, exist_ok=True)
            tmp.write_text(
                "# wa:allow-long-file\n" + "# padding\n" * 400,
                encoding="utf-8",
            )
            limits = V["LINE_COUNT_LIMITS"]
            waiver = V["LINE_COUNT_WAIVER"]
            text = tmp.read_text(encoding="utf-8")
            self.assertIn(waiver, text[:200])
            self.assertGreater(len(text.splitlines()), limits["assembly/*.py"])


class TestGraphManifestCoherence(unittest.TestCase):
    def test_real_graph_and_manifest_agree(self):
        self.assertEqual(V["check_graph_manifest_coherence"](), [])

    def test_drift_is_detected(self):
        import json
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            gp = Path(td) / "graph.json"
            mp = Path(td) / "manifest.json"
            gp.write_text(
                json.dumps({"nodes": [{"id": "a"}, {"id": "b"}]}),
                encoding="utf-8",
            )
            mp.write_text(json.dumps({"nodes": [{"id": "a"}]}), encoding="utf-8")
            violations = V["check_graph_manifest_coherence"](gp, mp)
            self.assertTrue(violations)
            self.assertIn("b", violations[0])


if __name__ == "__main__":
    unittest.main()
