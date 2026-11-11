#!/usr/bin/env python3
"""Golden-file tests for harness-adapter contract.

Compares AGENTS.md and manifest.json against golden copies. A deliberate
change to either file fails the test until the golden file is updated.
"""
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GOLDEN_DIR = ROOT / "tests" / "fixtures" / "golden"


class TestGoldenFiles(unittest.TestCase):
    """Golden-file tests to detect contract drift."""

    def test_agents_md_matches_golden(self):
        """AGENTS.md must match golden copy."""
        current = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        golden = (GOLDEN_DIR / "AGENTS.md").read_text(encoding="utf-8")
        self.assertEqual(current, golden,
                         "AGENTS.md drifted from golden. Update tests/fixtures/golden/AGENTS.md if intentional.")

    def test_manifest_matches_golden(self):
        """manifest.json must match golden copy."""
        current = json.loads((ROOT / ".context" / "manifest.json").read_text(encoding="utf-8"))
        golden = json.loads((GOLDEN_DIR / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(current, golden,
                         "manifest.json drifted from golden. Update tests/fixtures/golden/manifest.json if intentional.")

    def test_manifest_has_contract_version(self):
        """manifest.json must contain contract_version field."""
        m = json.loads((ROOT / ".context" / "manifest.json").read_text(encoding="utf-8"))
        self.assertIn("contract_version", m, "manifest missing contract_version")
        self.assertEqual(m["contract_version"], "1.0.0")


if __name__ == "__main__":
    unittest.main()
