#!/usr/bin/env python3
"""Graph Traverser — bounded graph traversal over the prompt DAG.

Traverses `.context/prompt-graph.json` edges (requires, triggers, routes_to,
adapts, provenance_of) from starting nodes, up to max_hops depth and
max_nodes total. Returns a bounded subgraph of related nodes.

Manager-tier only: workers must not use this. Workers should use
direct tool calls or the vector retriever instead.

Stdlib only. Read-only against the graph.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
GRAPH_PATH = ROOT / ".context" / "prompt-graph.json"
MANIFEST_PATH = ROOT / ".context" / "manifest.json"

# Manager-tier roles that are allowed to use graph traversal
MANAGER_ROLES = frozenset(
    {"taskmaster", "conceptualizer", "research-manager", "coding-manager", "review-manager"}
)

# Worker roles that are NOT allowed to use graph traversal
WORKER_ROLES = frozenset({"coder", "researcher", "reviewer"})


class GraphTraverser:
    """Traverses the prompt DAG from starting nodes.

    Performs bounded breadth-first traversal over graph edges, returning
    all reachable nodes within max_hops depth and max_nodes total count.
    """

    def __init__(self):
        self.graph: dict[str, Any] = {}
        self.nodes_by_id: dict[str, dict[str, Any]] = {}
        self.adjacency: dict[str, list[dict[str, Any]]] = {}

    def _load_graph(self) -> None:
        if self.graph:
            return
        if GRAPH_PATH.exists():
            with GRAPH_PATH.open("r", encoding="utf-8") as f:
                self.graph = json.load(f)
        else:
            self.graph = {"nodes": [], "edges": []}

        self.nodes_by_id = {n.get("id", ""): n for n in self.graph.get("nodes", [])}
        self.adjacency = {}
        for e in self.graph.get("edges", []):
            src = e.get("from", "")
            self.adjacency.setdefault(src, []).append(e)

    def traverse(
        self,
        start_node_ids: list[str],
        *,
        max_hops: int = 3,
        max_nodes: int = 8,
        role: str = "taskmaster",
    ) -> dict[str, Any]:
        """Traverse the graph from starting nodes.

        Args:
            start_node_ids: Starting node IDs.
            max_hops: Maximum traversal depth (default 3).
            max_nodes: Maximum total nodes to return (default 8).
            role: Role of the caller. Manager-tier roles only.

        Returns:
            Dict with "nodes" (list of node dicts) and "edges" (list of
            edge dicts) representing the traversed subgraph.

        Raises:
            PermissionError: If the role is not a manager-tier role.
        """
        if role not in MANAGER_ROLES:
            raise PermissionError(
                f"Graph traversal is restricted to manager-tier roles. "
                f"Role '{role}' is not authorized. Workers must use direct "
                f"tool calls or the vector retriever instead."
            )

        self._load_graph()

        if not start_node_ids:
            return {"nodes": [], "edges": []}

        # BFS traversal
        visited: set[str] = set()
        queue: list[tuple[str, int]] = []  # (node_id, depth)
        visited_nodes: dict[str, dict[str, Any]] = {}
        visited_edges: list[dict[str, Any]] = []

        for start_id in start_node_ids:
            if start_id not in self.nodes_by_id:
                continue
            queue.append((start_id, 0))

        while queue:
            current_id, depth = queue.pop(0)

            if current_id in visited:
                continue
            visited.add(current_id)
            visited_nodes[current_id] = self.nodes_by_id.get(current_id, {})

            if len(visited_nodes) >= max_nodes:
                break

            if depth >= max_hops:
                continue

            for edge in self.adjacency.get(current_id, []):
                target = edge.get("to", "")
                if target not in visited and target in self.nodes_by_id:
                    visited_edges.append(edge)
                    queue.append((target, depth + 1))

        return {
            "nodes": list(visited_nodes.values()),
            "edges": visited_edges,
            "start_nodes": start_node_ids,
            "max_hops": max_hops,
            "max_nodes": max_nodes,
            "role": role,
        }


def main():
    """CLI: test graph traversal."""
    import argparse
    import json

    ap = argparse.ArgumentParser(description="Graph traverser test")
    ap.add_argument("node_ids", nargs="+", help="Starting node ID(s)")
    ap.add_argument(
        "--role", default="taskmaster", help="Role making the request"
    )
    ap.add_argument(
        "--max-hops", type=int, default=3, help="Max traversal depth"
    )
    ap.add_argument(
        "--max-nodes", type=int, default=8, help="Max total nodes"
    )
    args = ap.parse_args()

    traverser = GraphTraverser()
    try:
        result = traverser.traverse(
            args.node_ids,
            role=args.role,
            max_hops=args.max_hops,
            max_nodes=args.max_nodes,
        )
        print(json.dumps(result, indent=2))
    except PermissionError as exc:
        print(f"DENIED: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
