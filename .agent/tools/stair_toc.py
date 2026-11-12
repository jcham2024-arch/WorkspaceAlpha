#!/usr/bin/env python3
"""STAIR Table of Contents construction — pure computation from the graph.

Responsibility: load .context/graph.json (or prompt-graph.yaml) and build a
hierarchical ToC view: file node -> section node(s) -> leaf nodes. No LLM
calls, no I/O beyond reading the graph file. Unit-testable without mocks.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]

GRAPH_JSON_PATH = ROOT / ".context" / "graph.json"
GRAPH_YAML_PATH = ROOT / ".context" / "prompt-graph.yaml"


def load_graph() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return (nodes, edges) from the graph JSON, falling back to YAML.

    Read-only against the graph; never writes it.
    """
    if GRAPH_JSON_PATH.exists():
        with GRAPH_JSON_PATH.open("r", encoding="utf-8") as f:
            graph = json.load(f)
        return graph.get("nodes", []), graph.get("edges", [])
    try:
        import yaml  # type: ignore

        with GRAPH_YAML_PATH.open("r", encoding="utf-8") as f:
            graph = yaml.safe_load(f)
        return graph.get("nodes", []), graph.get("edges", [])
    except ImportError:
        pass
    return [], []


def build_toc(nodes: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a hierarchical Table of Contents from graph nodes.

    Returns {"nodes_by_id", "nodes_by_ref", "root_nodes"}. Pure computation.
    """
    nodes_by_id: dict[str, dict[str, Any]] = {}
    nodes_by_ref: dict[str, list[dict[str, Any]]] = {}
    root_nodes: list[dict[str, Any]] = []

    for node in nodes:
        node_id = node.get("id", "")
        content_ref = node.get("content_ref", "")

        nodes_by_id[node_id] = node

        if content_ref:
            nodes_by_ref.setdefault(content_ref, []).append(node)
        else:
            root_nodes.append(node)

    return {
        "nodes_by_id": nodes_by_id,
        "nodes_by_ref": nodes_by_ref,
        "root_nodes": root_nodes,
    }
