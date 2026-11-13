#!/usr/bin/env python3
"""Optimize phase of the DAG compiler pipeline (Phases 3–4).

Responsibilities:
- Phase 3 — Optimize: read byte ranges and count tokens for candidate nodes.
- Phase 4 — Execute: enforce per-tier token budget, pruning farthest nodes.

Stdlib only.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

sys_path_inserted = False


def _ensure_path() -> None:
    global sys_path_inserted
    if not sys_path_inserted:
        import sys

        sys.path.insert(0, str(Path(__file__).resolve().parent))
        sys_path_inserted = True


def count_node_tokens(
    graph_node: dict[str, Any], reader, budgeter
) -> dict[str, Any]:
    """Read byte ranges and count tokens for a candidate graph node.

    Returns a dict with node_id, node_type, token_count, edge_distance,
    token_count_method, estimate_error_bound.
    """
    _ensure_path()
    from slicer import SliceOutOfBounds  # noqa: E402

    node_type = graph_node.get("type", "Skill")
    token_budget = graph_node.get("token_budget", 0)
    edge_distance = graph_node.get("metadata", {}).get("edge_distance", 0)

    actual_tokens = token_budget
    content_ref = graph_node.get("content_ref", "")
    content_text = ""

    if node_type == "ContextSlice":
        manifest_node_id = graph_node.get("metadata", {}).get(
            "manifest_node", graph_node["id"]
        )
        try:
            chunk = reader.slicer.slice_node(manifest_node_id)
            content_text = chunk.decode("utf-8", errors="replace")
        except SliceOutOfBounds:
            content_text = ""
    elif node_type == "SystemPrompt":
        try:
            prefix_path = ROOT / content_ref
            if prefix_path.exists():
                content_text = prefix_path.read_text(
                    encoding="utf-8", errors="replace"
                )
        except Exception:
            content_text = ""
    elif node_type == "Skill":
        graph_node_ref = graph_node.get("content_ref", "")
        try:
            skill_path = ROOT / graph_node_ref
            if skill_path.exists():
                content_text = skill_path.read_text(
                    encoding="utf-8", errors="replace"
                )
        except Exception:
            content_text = ""

    if content_text:
        actual_tokens = budgeter.count_tokens(
            content_text, model_id=graph_node.get("metadata", {}).get("model")
        )
    else:
        actual_tokens = token_budget

    return {
        "node_id": graph_node["id"],
        "node_type": node_type,
        "token_count": actual_tokens,
        "edge_distance": edge_distance,
        "token_count_method": budgeter.counter_name(),
        "estimate_error_bound": budgeter.counter_error_bound(),
    }


def enforce_budget(
    nodes_with_tokens: list[dict[str, Any]],
    target_tier: str,
    budgeter,
    root_node_ids: list[str] | None = None,
):
    """Phase 4 — Execute: enforce per-tier token budget.

    Returns (budget_result, ceiling). Raises BLOCKED if over budget.
    """
    _ensure_path()
    from budgeter import BLOCKED  # noqa: E402

    ceiling = budgeter.get_ceiling(target_tier)
    budget_result = budgeter.enforce_budget(
        nodes_with_tokens, target_tier, root_node_ids=root_node_ids
    )

    if not budget_result.within_budget:
        raise BLOCKED(
            budget_result.blocked_reason or "CONTEXT_BUDGET_EXCEEDED",
            budget_result.pruned_nodes,
        )

    return budget_result, ceiling
