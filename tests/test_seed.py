#!/usr/bin/env python3
"""Tests for seed.py — heading extraction, byte ranges, stable output."""
import json
import hashlib
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEED_PY = ROOT / ".wiki" / "seed.py"
GRAPH_JSON = ROOT / ".context" / "graph.json"


def run_seed():
    subprocess.run([sys.executable, str(SEED_PY)], check=True, capture_output=True)


class TestSeed(unittest.TestCase):
    """Test seed.py behavior."""

    def setUp(self):
        run_seed()

    def test_one_node_per_heading(self):
        """Each Markdown heading should produce exactly one node.

        seed.py deduplicates by ``{file}::{slug(title)}`` (see seed.py's
        ``seen`` set), so a heading title repeated inside the same file
        collapses to one node. The expected count is therefore the number
        of *unique* file::slug pairs, not the raw heading count.
        """
        sys.path.insert(0, str(ROOT / ".wiki"))
        from seed import section_ranges, slug

        graph = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))
        expected_ids = set()
        for md_file in (ROOT / "docs").rglob("*.md"):
            data = md_file.read_bytes()
            if not data or b"\x00" in data[:8192]:
                continue
            rel = str(md_file.relative_to(ROOT))
            for (_start, _end, _level, title) in section_ranges(data):
                expected_ids.add(f"{rel}::{slug(title)}")

        actual_ids = {n["id"] for n in graph["nodes"]}
        self.assertEqual(
            actual_ids,
            expected_ids,
            "graph node ids must match the deduplicated file::slug set",
        )
        self.assertEqual(len(graph["nodes"]), len(actual_ids), "duplicate node id")

    def test_byte_ranges_correctly_slice_heading_body(self):
        """Byte ranges should correctly slice the heading body content."""
        graph = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))
        for node in graph["nodes"]:
            ref = node["content_ref"]
            start, end = node["byte_range"]
            full = (ROOT / ref).read_bytes()
            slice_ = full[start:end]
            # The slice should start with the heading line
            self.assertTrue(
                slice_.lstrip().startswith(b"#"),
                f"Node {node['id']}: slice does not start with heading"
            )
            # If sha256 exists (after build), verify it
            if "sha256" in node:
                self.assertEqual(
                    hashlib.sha256(slice_).hexdigest(),
                    node["sha256"],
                    f"Node {node['id']}: hash mismatch"
                )

    def test_stable_output_across_runs(self):
        """Running seed.py twice should produce identical graph.json."""
        run_seed()
        graph1 = GRAPH_JSON.read_bytes()
        run_seed()
        graph2 = GRAPH_JSON.read_bytes()
        self.assertEqual(graph1, graph2, "graph.json not stable across runs")

    def test_heading_slug_generation(self):
        """Heading slugs should be URL-safe."""
        graph = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))
        for node in graph["nodes"]:
            # Node id format: path::slug
            parts = node["id"].split("::")
            self.assertEqual(len(parts), 2)
            slug = parts[1]
            # Slug should be lowercase, hyphens only
            self.assertTrue(
                all(c.islower() or c.isdigit() or c == "-" for c in slug),
                f"Invalid slug: {slug}"
            )
            self.assertFalse(slug.startswith("-") or slug.endswith("-"))


if __name__ == "__main__":
    unittest.main()
