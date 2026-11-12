#!/usr/bin/env python3
"""STAIR Navigator — Structure-Aware Index Retrieval using the graph as a Table of Contents.

Uses the prompt graph (.context/graph.json or .context/prompt-graph.yaml) as a
hierarchical table of contents: file node → section node(s) → leaf nodes.
Queries a manager-tier adapter to predict which leaf node best answers the
query, then validates the prediction against the manifest and hydrates the
leaf by reading its byte range.

Stdlib only. Read-only against the graph and manifest; never writes them.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]

GRAPH_JSON_PATH = ROOT / ".context" / "graph.json"
GRAPH_YAML_PATH = ROOT / ".context" / "prompt-graph.yaml"
MANIFEST_PATH = ROOT / ".context" / "manifest.json"

try:
    import yaml  # type: ignore

    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class LeafPrediction:
    """Result of navigating the graph for a query.

    Attributes:
        node_id: The predicted leaf node id, or None if no confident match.
        path: Ordered list of node ids from root to leaf.
        confidence: Confidence score 0.0-1.0.
        byte_range: Byte range [start, end] for hydrating the leaf content.
        content_ref: The content_ref path for the leaf node.
    """

    def __init__(
        self,
        node_id: str | None,
        path: list[str],
        confidence: float,
        byte_range: list[int] | None = None,
        content_ref: str | None = None,
    ):
        self.node_id = node_id
        self.path = path
        self.confidence = confidence
        self.byte_range = byte_range
        self.content_ref = content_ref

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "path": self.path,
            "confidence": self.confidence,
            "byte_range": self.byte_range,
            "content_ref": self.content_ref,
        }


def _load_graph() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Load the prompt graph from YAML (preferred) or JSON fallback."""
    if GRAPH_YAML_PATH.exists():
        try:
            import yaml  # type: ignore

            with GRAPH_YAML_PATH.open("r", encoding="utf-8") as f:
                graph = yaml.safe_load(f)
            return graph.get("nodes", []), graph.get("edges", [])
        except ImportError:
            pass
    if GRAPH_JSON_PATH.exists():
        with GRAPH_JSON_PATH.open("r", encoding="utf-8") as f:
            graph = json.load(f)
        return graph.get("nodes", []), graph.get("edges", [])
    return [], []


def _load_manifest() -> dict[str, Any]:
    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def _build_toc(nodes: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Build a hierarchical Table of Contents from graph nodes.

    Organizes nodes by content_ref (file path), grouping sections under their
    parent file and leaf sections under their parent section. Returns a dict
    mapping node_id to node info, plus a list of root-level nodes.
    """
    nodes_by_id: dict[str, dict[str, Any]] = {}
    nodes_by_ref: dict[str, list[dict[str, Any]]] = {}
    root_nodes: list[dict[str, Any]] = []

    for node in nodes:
        node_id = node.get("id", "")
        content_ref = node.get("content_ref", "")
        node_type = node.get("type", "")

        nodes_by_id[node_id] = node

        if content_ref:
            nodes_by_ref.setdefault(content_ref, []).append(node)
        else:
            # Root-level node (no content_ref, e.g., envelope or adapter nodes)
            root_nodes.append(node)

    return {"nodes_by_id": nodes_by_id, "nodes_by_ref": nodes_by_ref, "root_nodes": root_nodes}


def _dispatch_llm(
    model: str,
    tier: str,
    prompt: str,
    max_tokens: int = 512,
    temperature: float = 0.0,
) -> dict[str, Any]:
    """Dispatch to a model adapter for LLM-based reasoning.

    Uses the adapter dispatch module to route to the appropriate model adapter
    based on the target tier. Returns the parsed JSON response from the model.
    """
    sys.path.insert(0, str(ROOT / "adapters"))
    from dispatch import AdapterDispatch  # noqa: E402

    dispatcher = AdapterDispatch()
    dispatch_result = adapter.dispatch(
        model=model,
        target_tier=tier,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    dispatch_payload = dispatch.get("payload", {})

    # The dispatch returns a payload dict; we need to actually invoke the model
    # via MCP or direct call. For now, return the dispatch payload so the
    # caller can execute it via the MCP server or directly.
    return dispatch_payload


def navigate(
    query: str,
    *,
    max_depth: int = 6,
    model: str = "nemotron-3.5",
    tier: str = "manager",
) -> LeafPrediction:
    """Navigate the graph to find the most relevant leaf node for a query.

    Uses the graph as a hierarchical Table of Contents:
    1. Build a ToC from the graph (file → section → leaf nodes).
    2. Query the manager-tier adapter with the ToC and query to predict
       the best leaf node.
    3. Validate the prediction against the manifest.
    4. Hydrate the leaf by reading its byte range.

    Args:
        query: The user query string.
        max_depth: Maximum depth to traverse in the ToC.
        model: Model name for the advisor LLM.
        tier: Target tier for the advisor model (should be manager tier).

    Returns:
        LeafPrediction with the predicted leaf node, path, confidence,
        byte range, and content ref.
    """
    nodes, edges = _load_graph()
    if not nodes:
        return LeafPrediction(
            node_id=None,
            path=[],
            confidence=0.0,
            byte_range=None,
            content_ref=None,
        )

    toc = _build_toc(nodes)
    manifest_nodes, _ = _load_manifest()

    # Build a compact ToC summary for the LLM
    toc_summary = []
    for node in nodes:
        node_id = node.get("id", "")
        summary = node.get("summary", "")
        content_ref = node.get("content_ref", "")
        node_type = node.get("type", "")
        toc_summary.append(f"  - {node_id} ({node_type}): {summary} [{content_ref}]")

    toc_text = "\n".join(toc_summary)

    # Dispatch to manager-tier adapter to predict the best leaf node
    dispatch_payload = _dispatch_llm(
        model=model,
        tier=tier,
        prompt=f"""Given the following table of contents from a documentation graph:

{toc_summary}

Query: {query}

Identify the single most relevant leaf node that would contain the answer to this query.
Return a JSON object with:
- "node_id": the id of the most relevant leaf node
- "confidence": a confidence score from 0.0 to 1.0
- "reasoning": brief explanation of why this node was selected

Only return the JSON object, nothing else.""",
        max_tokens=512,
    )

    # Parse the LLM response to get the predicted node_id and confidence
    predicted_node_id = None
    confidence = 0.0

    try:
        # The dispatch_payload contains the model's response text
        response_text = dispatch_payload.get("text", "") or dispatch_payload.get("content", "")
        # Try to parse as JSON
        try:
            parsed = json.loads(response_text)
            predicted_node_id = parsed.get("node_id")
            confidence = float(parsed.get("confidence", 0.0))
        except (json.JSONDecodeError, ValueError, TypeError):
            # Fallback: try to extract node_id from text using regex
            import re

            match = re.search(r'"node_id"\s*:\s*"([^"]+)"', response_text)
            if match:
                predicted_node_id = match.group(1)
            match = re.search(r'"confidence"\s*:\s*([0-9.]+)', response_text)
            if match:
                confidence = float(match.group(1))
    except Exception:
        predicted_node_id = None
        confidence = 0.0

    # Validate prediction against manifest
    manifest_nodes, _ = _load_manifest()
    manifest_node_ids = {n.get("id", "") for n in manifest_nodes}

    if predicted_node_id and predicted_node_id not in manifest_nodes:
        # Node not in manifest - fall back to VECTOR
        return LeafPrediction(
            node_id=None,
            path=[],
            confidence=0.0,
            byte_range=None,
            content_ref=None,
        )

    # Hydrate the leaf node by reading its byte range
    if predicted_node_id:
        graph_node = None
        for n in nodes:
            if n.get("id") == predicted_node_id:
                graph_node = n
                break

        if graph_node:
            content_ref = graph_node.get("content_ref", "")
            byte_range = node.get("byte_range") if (node := graph_node) else None

            # Read the leaf content from the manifest node's byte range
            manifest_node = None
            for mn in manifest_nodes:
                if mn.get("id") == predicted_node_id:
                    manifest_node = mn
                    break

            if manifest_node:
                content_ref = manifest_node.get("content_ref", "")
                byte_range = manifest_node.get("byte_range")
                content_ref = manifest_node.get("content_ref", "")

                # Read the actual content
                content_path = ROOT / content_ref
                if content_path.exists():
                    content_bytes = content_path.read_bytes()
                    start, end = byte_range
                    if 0 <= start < end <= len(content_bytes):
                        # Content successfully hydrated
                        return LeafPrediction(
                            node_id=predicted_node_id,
                            path=[predicted_node_id],
                            confidence=confidence,
                            byte_range=[start, end],
                            content_ref=content_ref,
                        )

    # Fallback: return empty prediction
    return LeafPrediction(
        node_id=None,
        path=[],
        confidence=0.0,
        byte_range=None,
        content_ref=None,
    )


def main():
    """CLI: test the STAIR navigator."""
    import argparse

    ap = argparse.ArgumentParser(description="STAIR Navigator test")
    ap.add_argument("query", help="Query to navigate for")
    ap.add_argument(
        "--model", default="nemotron-3.5", help="Model to use for navigation"
    )
    ap.add_argument(
        "--tier", default="manager", help="Target tier for the advisor model"
    )
    args = ap.parse_args()

    result = navigate(args.query, model=args.model, tier=args.tier)
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
