#!/usr/bin/env python3
"""Deliberately bad navigator used to prove the validate.py gate fires.

Each function below violates one FIX_STAIR_LOOP_II.md §1 invariant. The gate
checks in validate.py must flag this file. Never import it.
"""
from __future__ import annotations


def navigate(query, *, manifest=None):
    """Violates: while loop, keyword fallback, inline dispatch."""
    nodes = [{"id": "a"}, {"id": "b"}]
    dispatcher = None

    while True:  # VIOLATION: while loop — prediction must be single-shot
        result = dispatcher.dispatch(model="x", target_tier="thinking")
        break

    # VIOLATION: keyword fallback — a second prediction attempt
    query_lower = query.lower()
    if not result.get("node_id"):
        for node in nodes:
            if query_lower in node.get("summary", ""):
                return node

    try:
        return result
    except Exception:  # VIOLATION: broad except
        return None
