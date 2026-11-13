#!/usr/bin/env python3
"""Plan phase of the DAG compiler pipeline (Phases 0–2).

Responsibilities:
- Phase 0 — Route: determine the retrieval protocol via the router.
- Phase 1 — Plan: resolve scope from the delegation envelope.
- Phase 2 — Bind: walk graph edges from envelope nodes and bind the selected
  protocol node.

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


def route_protocol(delegation: dict[str, Any], reader) -> tuple[str, Any]:
    """Phase 0 — Route: determine protocol via the router.

    Returns (protocol_node_id, routing_decision).
    """
    _ensure_path()
    from router import route as route_query  # noqa: E402

    routing_decision = route_query(
        query=delegation.get("task", ""),
        profile=delegation.get("profile", "conceptualizer"),
        context={
            "delegation_type": delegation.get("delegation_type", ""),
            "target_tier": delegation.get("target_tier", "low_thinking"),
            "allowed_targets": delegation.get("allowed_targets", []),
        },
    )
    return routing_decision.node_id, routing_decision


def apply_tier_ceiling(decision: Any, target_tier: str, reader) -> tuple[str, Any]:
    """Downgrade a protocol whose agent tier exceeds the caller's tier.

    A worker-tier caller cannot run a manager-only protocol such as PATTERN
    or GRAPH. Per the retrieval directive §8, the downgrade is to VECTOR and
    is recorded in provenance with reason ``tier_ceiling``.

    Returns (protocol_node_id, decision).
    """
    _ensure_path()
    from router import RoutingDecision  # noqa: E402
    from budgeter import AGENT_TIER_BY_TARGET, AGENT_TIER_ORDER, BLOCKED  # noqa: E402

    node = reader.get_graph_node(decision.node_id)
    required = (node or {}).get("tier")
    caller = AGENT_TIER_BY_TARGET.get(target_tier)

    if required not in AGENT_TIER_ORDER or caller not in AGENT_TIER_ORDER:
        return decision.node_id, decision
    if AGENT_TIER_ORDER[required] <= AGENT_TIER_ORDER[caller]:
        return decision.node_id, decision

    fallback = reader.get_graph_node("proto-vector")
    if fallback is None:
        raise BLOCKED(
            f"TIER_CEILING: protocol {decision.protocol} requires "
            f"{required} tier but caller is {target_tier}, and no "
            f"proto-vector fallback node exists"
        )

    downgraded = RoutingDecision(
        node_id="proto-vector",
        protocol="VECTOR",
        confidence=decision.confidence,
        rule_id=decision.rule_id,
        reason=(
            f"tier_ceiling: {decision.protocol} requires {required} but "
            f"caller is {target_tier}; downgraded to VECTOR"
        ),
    )
    downgraded.downgraded_from = decision.protocol
    downgraded.required_tier = required
    return downgraded.node_id, downgraded


def resolve_scope(delegation: dict[str, Any], reader) -> list[str]:
    """Phase 1 — Plan: resolve scope from the delegation envelope.

    Returns a list of manifest node IDs matching allowed_targets.
    """
    task_type = delegation.get("task_type", "")
    domain = delegation.get("domain", "")
    target_tier = delegation.get("target_tier", "low_thinking")
    allowed_targets = delegation.get("allowed_targets", [])

    return reader.resolve_scope(
        task_type=task_type,
        domain=domain,
        allowed_targets=allowed_targets if allowed_targets else None,
        target_tier=target_tier,
    )


def check_targets(allowed_targets: list[str], reader, budgeter) -> None:
    """Check that allowed targets exist in the manifest.

    Raises BLOCKED if any target is missing.
    """
    _ensure_path()
    from budgeter import BLOCKED  # noqa: E402

    for target in allowed_targets:
        reason = budgeter.check_target_in_manifest(target, reader.all_nodes())
        if reason:
            raise BLOCKED(reason)


def find_envelope_nodes(delegation_type: str, reader) -> list[str]:
    """Find envelope node IDs matching the delegation type."""
    result = []
    for node_id, node in reader.all_graph_nodes().items():
        if node.get("type") == "Envelope":
            metadata = node.get("metadata", {})
            if metadata.get("delegation_type") == delegation_type:
                result.append(node_id)
    return result


def bind_candidates(
    envelope_node_ids: list[str],
    required_nodes: list[str],
    triggered_nodes: list[str],
    routed_nodes: list[str],
    protocol_node_id: str,
) -> list[str]:
    """Phase 2 — Bind: combine and filter candidate node IDs.

    Only the protocol node selected by the router is bound; the other
    proto-* nodes are alternatives reachable from the same envelopes.
    Binding all five would put every retrieval strategy into one prompt,
    blowing the budget and defeating the point of routing.
    """
    candidate_ids = list(
        dict.fromkeys(
            envelope_node_ids + required_nodes + triggered_nodes + routed_nodes
        )
    )

    candidate_ids = [
        node_id
        for node_id in candidate_ids
        if not node_id.startswith("proto-") or node_id == protocol_node_id
    ]

    if protocol_node_id and protocol_node_id not in candidate_ids:
        candidate_ids.insert(0, protocol_node_id)

    return candidate_ids
