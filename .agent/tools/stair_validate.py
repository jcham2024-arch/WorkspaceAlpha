#!/usr/bin/env python3
"""STAIR prediction validation and leaf hydration — pure, unit-testable.

Responsibilities:
- validate_prediction(): check a predicted node_id against the manifest and
  graph; raise ManifestDriftError on structural drift.
- hydrate(): read a leaf's byte range in byte mode and decode explicitly.

No LLM calls. I/O is limited to reading the content file. Every function is
unit-testable without mocks.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


class ManifestDriftError(Exception):
    """The manifest no longer reflects the graph — hard error, never retry."""


class HydrationError(Exception):
    """A leaf byte range could not be decoded as UTF-8 — build-time bug."""


def _find_node(node_id: str, manifest: dict[str, Any]) -> dict[str, Any] | None:
    for node in manifest.get("nodes", []):
        if node.get("id") == node_id:
            return node
    return None


def validate_prediction(
    prediction: dict[str, Any],
    manifest: dict[str, Any],
    graph_nodes: list[dict[str, Any]],
) -> dict[str, Any] | None:
    """Validate a predicted leaf against the manifest.

    Returns the validated node dict, or None if the prediction is empty /
    unknown (not an error — the caller decides fallback).

    Raises ManifestDriftError if the graph and manifest disagree about which
    node ids exist — the session must fail loudly rather than fall back onto
    a stale structure.
    """
    predicted_node_id = prediction.get("node_id")
    if not predicted_node_id:
        return None

    manifest_ids = {n.get("id", "") for n in manifest.get("nodes", [])}
    graph_ids = {n.get("id", "") for n in graph_nodes}

    missing_from_manifest = graph_ids - manifest_ids
    if missing_from_manifest:
        raise ManifestDriftError(
            "manifest/graph drift: nodes in graph.json but not manifest.json: "
            + ", ".join(sorted(missing_from_manifest))
            + " — run build.py then validate.py"
        )

    if predicted_node_id not in manifest_ids:
        return None

    validated = _find_node(predicted_node_id, manifest)
    return validated


def hydrate(validated: dict[str, Any]) -> str:
    """Read a leaf's byte range in byte mode and decode as UTF-8.

    Uses seek+read (not read-all-then-slice) so large files stay cheap, and
    decodes explicitly so a misaligned byte range raises HydrationError
    instead of silently returning wrong content.
    """
    content_ref = validated.get("content_ref", "")
    start, end = validated.get("byte_range", [0, 0])

    content_path = ROOT / content_ref
    if not content_path.exists():
        raise HydrationError(f"content_ref not found: {content_ref}")

    with content_path.open("rb") as f:
        f.seek(start)
        raw = f.read(end - start)

    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HydrationError(
            f"byte range [{start}:{end}] in {content_ref} does not align "
            f"with UTF-8 character boundaries: {exc}"
        ) from exc
