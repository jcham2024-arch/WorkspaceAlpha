#!/usr/bin/env python3
"""Tests for build.py — DAG validation, manifest generation, wiki output."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_PY = ROOT / ".wiki" / "build.py"
SEED_PY = ROOT / ".wiki" / "seed.py"
GRAPH_JSON = ROOT / ".context" / "graph.json"
MANIFEST_JSON = ROOT / ".context" / "manifest.json"
WIKI_HTML = ROOT / ".wiki" / "index.html"


def run_seed():
    subprocess.run([sys.executable, str(SEED_PY)], check=True, capture_output=True)


def run_build():
    subprocess.run([sys.executable, str(BUILD_PY)], check=True, capture_output=True)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_graph(graph: dict) -> None:
    """Validate DAG (copied from build.py)."""
    ids = [n["id"] for n in graph["nodes"]]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate node id")
    id_set = set(ids)
    adj = {i: [] for i in ids}
    for e in graph.get("edges", []):
        f, t = e.get("from"), e.get("to")
        if f not in id_set or t not in id_set:
            raise SystemExit(f"edge references unknown node: {e}")
        if f == t:
            raise SystemExit(f"self-loop: {e}")
        adj[f].append(t)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {i: WHITE for i in ids}
    def dfs(u):
        color[u] = GRAY
        for v in adj[u]:
            if color[v] == GRAY:
                raise SystemExit(f"cycle detected through {u} -> {v}")
            if color[v] == WHITE:
                dfs(v)
        color[u] = BLACK
    for i in ids:
        if color[i] == WHITE:
            dfs(i)


class TestBuildValidation(unittest.TestCase):
    """Test that build.py validates the DAG correctly."""

    def setUp(self):
        # Ensure clean state by running seed+build
        run_seed()
        run_build()

    def test_acyclic_graph_passes(self):
        """An acyclic graph should pass validation."""
        # If we get here, setUp passed, so graph is acyclic
        graph = load_json(GRAPH_JSON)
        self.assertIn("nodes", graph)
        self.assertIn("edges", graph)

    def test_cycle_fixture_raises(self):
        """A graph with a cycle should raise an error."""
        graph = {
            "version": 1,
            "nodes": [
                {"id": "a", "type": "doc", "summary": "A", "content_ref": "docs/a.md", "byte_range": [0, 10]},
                {"id": "b", "type": "doc", "summary": "B", "content_ref": "docs/b.md", "byte_range": [0, 10]},
            ],
            "edges": [
                {"from": "a", "to": "b"},
                {"from": "b", "to": "a"},  # cycle
            ],
        }
        with self.assertRaises(SystemExit) as cm:
            validate_graph(graph)
        self.assertIn("cycle detected", str(cm.exception))

    def test_referential_integrity_violation_raises(self):
        """An edge referencing unknown node should raise."""
        graph = {
            "version": 1,
            "nodes": [{"id": "a", "type": "doc", "summary": "A", "content_ref": "docs/a.md", "byte_range": [0, 10]}],
            "edges": [{"from": "a", "to": "nonexistent"}],
        }
        with self.assertRaises(SystemExit) as cm:
            validate_graph(graph)
        self.assertIn("edge references unknown node", str(cm.exception))

    def test_duplicate_node_id_raises(self):
        """Duplicate node IDs should raise."""
        graph = {
            "version": 1,
            "nodes": [
                {"id": "a", "type": "doc", "summary": "A", "content_ref": "docs/a.md", "byte_range": [0, 10]},
                {"id": "a", "type": "doc", "summary": "A2", "content_ref": "docs/b.md", "byte_range": [0, 10]},
            ],
            "edges": [],
        }
        with self.assertRaises(SystemExit) as cm:
            validate_graph(graph)
        self.assertIn("duplicate node id", str(cm.exception))

    def test_manifest_idempotent(self):
        """manifest.json should be byte-identical across two consecutive runs."""
        run_build()
        manifest1 = MANIFEST_JSON.read_bytes()
        run_build()
        manifest2 = MANIFEST_JSON.read_bytes()
        self.assertEqual(manifest1, manifest2, "manifest.json not idempotent")

    def test_wiki_generated(self):
        """Wiki HTML should be generated and non-trivial."""
        self.assertTrue(WIKI_HTML.exists())
        content = WIKI_HTML.read_text(encoding="utf-8")
        self.assertIn("<html", content.lower())
        self.assertIn("<script", content.lower())
        self.assertGreater(len(content), 500)


if __name__ == "__main__":
    unittest.main()
