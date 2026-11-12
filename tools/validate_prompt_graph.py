#!/usr/bin/env python3
"""Validate the prompt graph.

Validates `.context/prompt-graph.json` — the file every runtime consumer
reads (assembly/manifest_reader.py, .agent/tools/graph_traverser.py,
wiki/views/generator.py). It also checks that the human-readable mirror
`.context/prompt-graph.yaml` has not drifted, because the YAML previously
carried a duplicate `edges:` key: a conformant loader silently kept the last
3 edges and discarded the first 18, while this validator reported PASS on the
stale copy.

Checks:
- Top-level keys: version, nodes, edges
- Node fields: id, type required; content_ref required except for
  RetrievalProtocol nodes, which are routed to by metadata.tool
- Node types and edge types within the allowed enums
- All edge from/to references resolve to node ids
- Every RetrievalProtocol node declares metadata.protocol
- No duplicate node ids or duplicate edges
- YAML mirror agrees with JSON on node ids and edge triples
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

JSON_PATH = ROOT / ".context" / "prompt-graph.json"
YAML_PATH = ROOT / ".context" / "prompt-graph.yaml"
SCHEMA_PATH = ROOT / "schemas" / "prompt-graph.schema.json"

VALID_NODE_TYPES = {
    "SystemPrompt",
    "Skill",
    "Envelope",
    "ContextSlice",
    "Adapter",
    "OutputContract",
    "RetrievalProtocol",
}
VALID_EDGE_TYPES = {"requires", "triggers", "routes_to", "adapts", "provenance_of"}
# Two tier vocabularies coexist in the graph:
#   - skill lifecycle tiers for most node types
#   - agent tiers for RetrievalProtocol nodes (who may run the protocol)
VALID_TIERS = {
    "core", "curated", "experimental", "quarantine",
    "orchestrator", "manager", "worker",
}
KNOWN_PROTOCOLS = {"DIRECT", "STAIR", "VECTOR", "GRAPH", "PATTERN"}

# Types that carry their content inline rather than by reference.
NO_CONTENT_REF_TYPES = {"RetrievalProtocol"}


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def signature(graph: dict) -> tuple:
    return (
        tuple(sorted(n["id"] for n in graph["nodes"])),
        tuple(sorted((e["from"], e["to"], e["type"]) for e in graph["edges"])),
    )


def check_schema_enum() -> None:
    """The JSON Schema must list every type the validator accepts."""
    if not SCHEMA_PATH.exists():
        fail(f"missing {SCHEMA_PATH.relative_to(ROOT)}")
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        node_enum = set(
            schema["properties"]["nodes"]["items"]["properties"]["type"]["enum"]
        )
        edge_enum = set(
            schema["properties"]["edges"]["items"]["properties"]["type"]["enum"]
        )
    except KeyError as exc:
        fail(f"schema is missing a type enum: {exc}")
    if node_enum != VALID_NODE_TYPES:
        fail(f"schema node enum {sorted(node_enum)} != validator {sorted(VALID_NODE_TYPES)}")
    if edge_enum != VALID_EDGE_TYPES:
        fail(f"schema edge enum {sorted(edge_enum)} != validator {sorted(VALID_EDGE_TYPES)}")


def check_graph(graph: dict) -> None:
    for field in ("version", "nodes", "edges"):
        if field not in graph:
            fail(f"missing top-level field: {field}")
    if graph["version"] != "1.0.0":
        fail(f"unsupported graph version: {graph['version']}")

    node_ids: set[str] = set()
    for index, node in enumerate(graph["nodes"]):
        for field in ("id", "type"):
            if field not in node:
                fail(f"node {index} missing required field: {field}")

        node_type = node["type"]
        if node_type not in VALID_NODE_TYPES:
            fail(f"node {node.get('id', index)} has invalid type: {node_type}")

        if node_type not in NO_CONTENT_REF_TYPES and not node.get("content_ref"):
            fail(f"node {node['id']} of type {node_type} requires content_ref")

        if node_type == "RetrievalProtocol":
            protocol = node.get("metadata", {}).get("protocol")
            if not protocol:
                fail(f"RetrievalProtocol node {node['id']} requires metadata.protocol")
            if protocol not in KNOWN_PROTOCOLS:
                fail(
                    f"RetrievalProtocol node {node['id']} has unknown protocol "
                    f"{protocol!r} (expected one of {sorted(KNOWN_PROTOCOLS)})"
                )

        tier = node.get("tier")
        if tier is not None and tier not in VALID_TIERS:
            fail(f"node {node['id']} has invalid tier {tier!r}")

        budget = node.get("token_budget")
        if budget is not None and (not isinstance(budget, int) or budget < 0):
            fail(f"node {node['id']} has invalid token_budget {budget!r}")

        if node["id"] in node_ids:
            fail(f"duplicate node id: {node['id']}")
        node_ids.add(node["id"])

    edge_keys: set[tuple] = set()
    for index, edge in enumerate(graph["edges"]):
        for field in ("from", "to", "type"):
            if field not in edge:
                fail(f"edge {index} missing required field: {field}")
        if edge["type"] not in VALID_EDGE_TYPES:
            fail(f"edge {index} has invalid type: {edge['type']}")
        if edge["from"] not in node_ids:
            fail(f"edge {index} from references unknown node: {edge['from']}")
        if edge["to"] not in node_ids:
            fail(f"edge {index} to references unknown node: {edge['to']}")
        if edge["from"] == edge["to"]:
            fail(f"edge {index} is a self-loop: {edge['from']}")
        key = (edge["from"], edge["to"], edge["type"])
        if key in edge_keys:
            fail(f"duplicate edge: {key}")
        edge_keys.add(key)

    # Every protocol node must be reachable from an envelope via routes_to.
    routed = {e["to"] for e in graph["edges"] if e["type"] == "routes_to"}
    for node in graph["nodes"]:
        if node["type"] == "RetrievalProtocol" and node["id"] not in routed:
            fail(
                f"RetrievalProtocol node {node['id']} has no inbound routes_to edge — "
                f"the router can never select it"
            )


def check_yaml_mirror(graph: dict) -> None:
    if not YAML_PATH.exists():
        fail(f"missing {YAML_PATH.relative_to(ROOT)}")
    try:
        import yaml
    except ImportError:
        print("FAIL: PyYAML not installed. Run: pip install PyYAML")
        sys.exit(1)
    mirror = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))
    if signature(mirror) != signature(graph):
        fail(
            "prompt-graph.yaml has drifted from prompt-graph.json — "
            "run: python3 tools/sync_prompt_graph.py"
        )


def main() -> None:
    if not JSON_PATH.exists():
        fail(f"missing {JSON_PATH.relative_to(ROOT)}")

    check_schema_enum()

    graph = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    check_graph(graph)
    check_yaml_mirror(graph)

    protocols = [n["id"] for n in graph["nodes"] if n["type"] == "RetrievalProtocol"]
    print(
        f"PASS: prompt-graph.json valid ({len(graph['nodes'])} nodes, "
        f"{len(graph['edges'])} edges, protocols: {', '.join(sorted(protocols))})"
    )


if __name__ == "__main__":
    main()
