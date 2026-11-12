#!/usr/bin/env python3
"""STAIR Navigator — Structure-Aware Index Retrieval using the graph as a ToC.

Orchestrates: load graph -> build ToC -> single-shot manager-tier prediction
(adapters.navigator.dispatch_prediction) -> validate against manifest ->
hydrate leaf by byte range. Returns a LeafPrediction.
Predicts exactly once. Never retries, never loops, never dispatches LLM calls
inline. Low confidence / failed validation returns a None-node prediction; the
router decides fallback (single switch to VECTOR).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "adapters"))
sys.path.insert(0, str(ROOT / ".agent" / "tools"))
from adapters.navigator import (  # noqa: E402
    NavigatorTimeout,
    dispatch_prediction,
)
from stair_toc import build_toc, load_graph  # noqa: E402
from stair_validate import (  # noqa: E402
    HydrationError,
    ManifestDriftError,
    hydrate,
    validate_prediction,
)

MANIFEST_PATH = ROOT / ".context" / "manifest.json"

CONFIDENCE_THRESHOLD = 0.5


class LeafPrediction:
    """Result of navigating the graph for a query."""

    def __init__(self, node_id, path, confidence, byte_range=None,
                 content_ref=None, content=None):
        self.node_id = node_id
        self.path = path
        self.confidence = confidence
        self.byte_range = byte_range
        self.content_ref = content_ref
        self.content = content

    def to_dict(self):
        return {
            "node_id": self.node_id, "path": self.path,
            "confidence": self.confidence, "byte_range": self.byte_range,
            "content_ref": self.content_ref, "content": self.content,
        }


def _load_manifest():
    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def navigate(query, *, manifest=None, graph=None, max_depth=6):
    """Navigate the graph for a query. Single prediction; no retry; no loop.

    Raises NavigatorTimeout, NavigatorDispatchError, ManifestDriftError,
    HydrationError — the caller (router) handles them. Never catches here.
    """
    if graph is None:
        nodes, _ = load_graph()
    else:
        nodes = graph.get("nodes", [])
    if not nodes:
        return LeafPrediction(None, [], 0.0)

    toc = build_toc(nodes)
    if manifest is None:
        manifest = _load_manifest()

    # Exactly one prediction call.
    prediction = dispatch_prediction(query, toc, max_depth=max_depth)
    if prediction is None:
        return LeafPrediction(None, [], 0.0)

    # Low confidence -> None-node result, never a retry.
    if prediction.get("confidence", 0.0) < CONFIDENCE_THRESHOLD:
        return LeafPrediction(None, [], prediction.get("confidence", 0.0))

    # Single validation; drift is a hard error.
    validated = validate_prediction(prediction, manifest, nodes)
    if validated is None:
        return LeafPrediction(None, [], prediction.get("confidence", 0.0))

    content = hydrate(validated)
    return LeafPrediction(
        validated["id"], validated.get("path", [validated["id"]]),
        prediction.get("confidence", 0.0), validated.get("byte_range"),
        validated.get("content_ref"), content,
    )
