#!/usr/bin/env python3
"""Manifest reader — loads .context/manifest.json and walks the DAG.

Read-only consumer of the manifest. Provides scope-based node selection
for the DAG compiler pipeline.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / ".context" / "manifest.json"
PROMPT_GRAPH_PATH = ROOT / ".context" / "prompt-graph.json"


class ManifestReader:
    """Reads the manifest and prompt graph, resolves scope to node sets."""

    def __init__(self):
        self._manifest = None
        self._nodes = None
        self._edges = None
        self._graph = None
        self._graph_nodes = None
        self._graph_edges = None

    def _load_manifest(self):
        if self._manifest is None:
            if not MANIFEST_PATH.exists():
                raise FileNotFoundError(
                    f"missing {MANIFEST_PATH.relative_to(Path(__file__).resolve().parents[2])} — run python3 build.py first"
                )
            with MANIFEST_PATH.open("r", encoding="utf-8") as f:
                self._manifest = json.load(f)
            self._nodes = {n["id"]: n for n in self._manifest.get("nodes", [])}
            self._edges = self._manifest.get("edges", [])
        return self._manifest, self._nodes, self._edges

    def _load_graph(self):
        if self._graph is None:
            if not PROMPT_GRAPH_PATH.exists():
                raise FileNotFoundError(
                    f"missing {PROMPT_GRAPH_PATH.relative_to(Path(__file__).resolve().parents[2])} — run Phase 2 graph population"
                )
            with PROMPT_GRAPH_PATH.open("r", encoding="utf-8") as f:
                self._graph = json.load(f)
            self._graph_nodes = {n["id"]: n for n in self._graph.get("nodes", [])}
            self._graph_edges = self._graph.get("edges", [])
        return self._graph, self._graph_nodes, self._graph_edges

    def get_node(self, node_id: str) -> dict | None:
        """Get a manifest node by ID."""
        self._load_manifest()
        return self._nodes.get(node_id)

    def all_nodes(self) -> dict[str, dict]:
        """Return all manifest nodes keyed by node ID."""
        self._load_manifest()
        return self._nodes

    def all_graph_nodes(self) -> dict[str, dict]:
        """Return all prompt-graph nodes keyed by node ID."""
        self._load_graph()
        return self._graph_nodes

    def get_graph_node(self, node_id: str) -> dict | None:
        """Get a prompt graph node by ID."""
        self._load_graph()
        return self._graph_nodes.get(node_id)

    def resolve_scope(
        self,
        task_type: str | None = None,
        domain: str | None = None,
        allowed_targets: list[str] | None = None,
        target_tier: str | None = None,
    ) -> list[str]:
        """Resolve scope to a list of manifest node IDs.

        Selection rules:
        - If allowed_targets is provided, only nodes whose content_ref is in that list are selected.
        - If task_type is provided, nodes whose summary or tags match are preferred.
        - If target_tier is provided, nodes from tiers matching that tier are prioritized.
        """
        self._load_manifest()
        selected = []

        for node_id, node in self._nodes.items():
            content_ref = node.get("content_ref", "")

            # Hard filter: allowed_targets
            if allowed_targets is not None:
                if content_ref not in allowed_targets:
                    continue

            selected.append(node_id)

        return selected

    def get_graph_edges_from(self, node_id: str) -> list[dict]:
        """Get all graph edges originating from a node ID."""
        self._load_graph()
        return [e for e in self._graph_edges if e.get("from") == node_id]

    def get_graph_edges_to(self, node_id: str) -> list[dict]:
        """Get all graph edges targeting a node ID."""
        self._load_graph()
        return [e for e in self._graph_edges if e.get("to") == node_id]

    def walk_requires(self, start_node_ids: list[str]) -> list[str]:
        """Walk `requires` edges transitively from start nodes, returning all reachable node IDs."""
        self._load_graph()
        visited = set()
        stack = list(start_node_ids)
        while stack:
            cur = stack.pop()
            if cur in visited:
                continue
            visited.add(cur)
            for edge in self.get_graph_edges_from(cur):
                if edge.get("type") == "requires":
                    target = edge.get("to")
                    if target and target not in visited:
                        stack.append(target)
        return sorted(visited)

    def walk_triggers(self, start_node_ids: list[str], scope: dict) -> list[str]:
        """Walk `triggers` edges, including only targets whose trigger_condition matches scope."""
        self._load_graph()
        included = set()
        stack = list(start_node_ids)
        while stack:
            cur = stack.pop()
            if cur in included:
                continue
            included.add(cur)
            for edge in self.get_graph_edges_from(cur):
                if edge.get("type") == "triggers":
                    target = edge.get("to")
                    condition = edge.get("condition", "")
                    if target and self._condition_matches(condition, scope):
                        stack.append(target)
        return sorted(included)

    def walk_routes_to(self, start_node_ids: list[str]) -> list[str]:
        """Walk `routes_to` edges from start nodes."""
        self._load_graph()
        targets = set()
        for start in start_node_ids:
            for edge in self.get_graph_edges_from(start):
                if edge.get("type") == "routes_to":
                    target = edge.get("to")
                    if target:
                        targets.add(target)
        return sorted(targets)

    def _condition_matches(self, condition: str, scope: dict) -> bool:
        """Evaluate a YAML predicate condition against scope.

        Simple predicate language: "key in [val1, val2]" or "key==val" or "key!=val".
        Empty condition always matches.
        """
        if not condition or not condition.strip():
            return True
        condition = condition.strip()

        # Handle "key in [val1, val2]"
        in_match = __import__("re").match(
            r"^(\w+)\s+in\s*\[(.*)\]$", condition
        )
        if in_match:
            key = in_match.group(1)
            values_str = in_match.group(2)
            values = [v.strip().strip('"').strip("'") for v in values_str.split(",")]
            scope_val = scope.get(key, "")
            return scope_val in values

        # Handle "key==val" or "key!=val"
        eq_match = __import__("re").match(r"^(\w+)\s*(!=|==)\s*(.+)$", condition)
        if eq_match:
            key = eq_match.group(1)
            op = eq_match.group(2)
            val = eq_match.group(3).strip().strip('"').strip("'")
            scope_val = scope.get(key, "")
            if op == "==":
                return scope_val == val
            elif op == "!=":
                return scope_val != val

        # Unknown condition — fail closed
        return False


def main():
    """CLI: resolve scope and print matching node IDs."""
    import argparse

    ap = argparse.ArgumentParser(description="Resolve manifest scope to node IDs")
    ap.add_argument("--task-type", help="Task type filter")
    ap.add_argument("--domain", help="Domain filter")
    ap.add_argument("--allowed-targets", nargs="*", help="Allowed content_refs")
    ap.add_argument("--target-tier", help="Target tier filter")
    args = ap.parse_args()

    reader = ManifestReader()
    result = reader.resolve_scope(
        task_type=args.task_type,
        domain=args.domain,
        allowed_targets=args.allowed_targets,
        target_tier=args.target_tier,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
