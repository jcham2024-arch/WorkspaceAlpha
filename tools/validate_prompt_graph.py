#!/usr/bin/env python3
"""Validate .context/prompt-graph.yaml against .context/prompt-graph.schema.json.

Since jsonschema may not be available, this performs structural validation:
- Top-level keys: version, nodes, edges
- Node fields: id, type, content_ref (required); tier, token_budget, metadata (optional)
- Edge fields: from, to, type (required); condition, note (optional)
- Node types valid: SystemPrompt, Skill, Envelope, ContextSlice, Adapter, OutputContract
- Edge types valid: requires, triggers, routes_to, adapts, provenance_of
- All edge from/to references resolve to node ids
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:
    import yaml
except ImportError:
    print("FAIL: PyYAML not installed. Run: pip install PyYAML")
    sys.exit(1)


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def main() -> None:
    graph_path = ROOT / ".context" / "prompt-graph.yaml"
    schema_path = ROOT / "schemas" / "prompt-graph.schema.json"

    if not graph_path.exists():
        fail(f"missing {graph_path}")
    if not schema_path.exists():
        fail(f"missing {schema_path}")

    with graph_path.open("r", encoding="utf-8") as f:
        graph = yaml.safe_load(f)

    with schema_path.open("r", encoding="utf-8") as f:
        schema = json.load(f)

    # Validate top-level
    for field in ["version", "nodes", "edges"]:
        if field not in graph:
            fail(f"missing top-level field: {field}")

    if graph["version"] != "1.0.0":
        fail(f"unsupported graph version: {graph['version']}")

    # Validate node types and edges
    valid_node_types = {"SystemPrompt", "Skill", "Envelope", "ContextSlice", "Adapter", "OutputContract"}
    valid_edge_types = {"requires", "triggers", "routes_to", "adapts", "provenance_of"}

    node_ids = set()
    for i, node in enumerate(graph["nodes"]):
        for field in ["id", "type", "content_ref"]:
            if field not in node:
                fail(f"node {i} missing required field: {field}")
        if node.get("type") not in valid_node_types:
            fail(f"node {node.get('id', i)} has invalid type: {node.get('type')}")
        node_ids.add(node["id"])

    # Validate edges
    for i, edge in enumerate(graph["edges"]):
        for field in ["from", "to", "type"]:
            if field not in edge:
                fail(f"edge {i} missing required field: {field}")
        if edge.get("type") not in valid_edge_types:
            fail(f"edge {i} has invalid type: {edge.get('type')}")
        if edge.get("from") not in node_ids:
            fail(f"edge {i} from references unknown node: {edge.get('from')}")
        if edge.get("to") not in node_ids:
            fail(f"edge {i} to references unknown node: {edge.get('to')}")

    print(f"PASS: prompt-graph.yaml valid ({len(graph['nodes'])} nodes, {len(graph['edges'])} edges)")


if __name__ == "__main__":
    main()
