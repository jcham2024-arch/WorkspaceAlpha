"""Execute phase: render, retrieve, provenance + OTel."""
# wa:allow-long-file
# wa:allow-long-file
from __future__ import annotations

from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
_path_done = False

def _ensure_path() -> None:
    global _path_done
    if not _path_done:
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        _path_done = True

def render_node(node_id: str, node_type: str, reader) -> str:
    _ensure_path()
    graph_node = reader.get_graph_node(node_id)
    if graph_node is None:
        return f"<!-- Unknown node type {node_type}: {node_id} -->"

    content_ref = graph_node.get("content_ref", "")

    if node_type == "SystemPrompt":
        try:
            p = ROOT / content_ref
            if p.exists():
                return p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            pass
        return f"<!-- SystemPrompt {node_id} content unavailable -->"

    if node_type == "Skill":
        try:
            p = ROOT / content_ref
            if p.exists():
                return p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            pass
        return f"<!-- Skill {node_id} content unavailable -->"

    if node_type == "Envelope":
        meta = graph_node.get("metadata", {})
        return f"<!-- Envelope: {meta.get('delegation_type', 'unknown')} -- authority: {meta.get('authority', 'unknown')} -->"

    if node_type == "ContextSlice":
        try:
            return reader.slicer.slice_node_text(content_ref)
        except Exception:
            return f"<!-- ContextSlice {node_id}: slice unavailable -->"

    if node_type == "Adapter":
        meta = graph_node.get("metadata", {})
        return f"<!-- Adapter: {meta.get('model', 'unknown')} -->"

    if node_type == "OutputContract":
        return f"<!-- OutputContract: {content_ref} -->"

    if node_type == "RetrievalProtocol":
        meta = graph_node.get("metadata", {})
        return f"<!-- RetrievalProtocol: {meta.get('protocol', 'UNKNOWN')} (node {node_id}, tool {meta.get('tool', 'unspecified')}) -->"

    return f"<!-- Unknown node type {node_type}: {node_id} -->"

def run_retrieval(
    protocol_node_id: str,
    decision: Any,
    delegation: dict[str, Any],
    suffix_tokens: int,
    target_tier: str,
    reader,
    budgeter,
) -> dict[str, Any]:
    _ensure_path()
    from retrieval import execute as execute_retrieval

    node = reader.get_graph_node(protocol_node_id)
    if node is None or node.get("type") != "RetrievalProtocol":
        return {
            "protocol": decision.protocol,
            "status": "unavailable",
            "tokens": 0,
            "text": "",
            "units": [],
            "reason": f"no RetrievalProtocol node for {protocol_node_id}",
            "truncated": False,
        }

    meta = node.get("metadata", {})
    protocol = meta.get("protocol", decision.protocol)
    ceiling = budgeter.get_ceiling(target_tier)
    remaining = max(ceiling - suffix_tokens, 0)
    budget = min(int(node.get("token_budget") or 0) or remaining, remaining)

    if budget <= 0:
        return {
            "protocol": protocol,
            "status": "empty",
            "tokens": 0,
            "text": "",
            "units": [],
            "reason": f"no token headroom: {suffix_tokens} of {ceiling} already used",
            "truncated": False,
        }

    if protocol == "DIRECT":
        return {
            "protocol": protocol,
            "status": "ok",
            "tokens": 0,
            "text": "",
            "units": [],
            "reason": "DIRECT: skill node execution, no retrieval performed",
            "truncated": False,
        }

    result = execute_retrieval(
        protocol,
        delegation.get("task", ""),
        meta=meta,
        role=delegation.get("profile", "taskmaster"),
        max_tokens=budget,
    )
    return {
        "protocol": protocol,
        "status": result.status,
        "tokens": result.tokens,
        "text": result.text if result.status == "ok" else "",
        "units": [u.to_dict() for u in result.units],
        "reason": result.reason,
        "truncated": result.truncated,
    }

def build_provenance_params(
    delegation: dict[str, Any],
    adapter_params: dict[str, Any],
    routing_decision: Any,
    retrieval_record: dict[str, Any],
) -> dict[str, Any]:
    routing_record = {
        "protocol": routing_decision.protocol,
        "node_id": routing_decision.node_id,
        "confidence": routing_decision.confidence,
        "rule_id": routing_decision.rule_id,
        "reason": routing_decision.reason,
    }
    df = getattr(routing_decision, "downgraded_from", None)
    if df:
        routing_record["downgraded_from"] = df
        routing_record["required_tier"] = getattr(
            routing_decision, "required_tier", None
        )
        routing_record["tier_ceiling"] = delegation.get("target_tier")

    return {
        **adapter_params,
        "routing_decision": routing_record,
        "retrieval": {k: v for k, v in retrieval_record.items() if k != "text"},
    }

def record_provenance(
    delegation: dict[str, Any],
    assembled_nodes: list[dict[str, Any]],
    token_counts: dict[str, Any],
    adapter_params: dict[str, Any],
    return_envelope: dict[str, Any] | None,
    cache_hit: bool,
    cache_key: str | None,
    pruned_nodes: list[str],
) -> None:
    _ensure_path()
    from provenance.recorder import ProvenanceRecorder

    recorder = ProvenanceRecorder()
    recorder.record_turn(
        delegation_id=delegation.get("delegation_id", "unknown"),
        from_agent=delegation.get("from_agent", "unknown"),
        to_agent=delegation.get("to_agent", "unknown"),
        delegation_type=delegation.get("delegation_type", ""),
        target_tier=delegation.get("target_tier", ""),
        assembled_nodes=assembled_nodes,
        token_counts=token_counts,
        adapter_params=adapter_params,
        return_envelope=return_envelope,
        cache_hit=cache_hit,
        cache_key=cache_key,
        pruned_nodes=pruned_nodes,
    )

def record_otel(
    delegation: dict[str, Any],
    adapter_params: dict[str, Any],
    prefix_tokens: int,
    suffix_tokens: int,
    budget_result: Any,
    cache_key: str,
) -> None:
    _ensure_path()
    from telemetry.otel_genai import OTelGenAIRecorder

    recorder = OTelGenAIRecorder()
    tc = budget_result.to_dict()
    recorder.record_chat_span(
        span_id=f"span-{delegation.get('delegation_id', 'unknown')}-chat",
        trace_id=delegation.get("trace_id", delegation.get("delegation_id", "unknown")),
        model_name=adapter_params.get("model", "deepseek-v3.2"),
        provider=adapter_params.get("model", "deepseek-v3.2").split("-")[0],
        input_tokens=prefix_tokens,
        output_tokens=suffix_tokens,
        finish_reason=(
            "stop" if not tc.get("budget_exceeded", False) else "length"
        ),
        temperature=adapter_params.get("temperature"),
        max_tokens=adapter_params.get("max_tokens"),
        system_prompt_hash=cache_key,
        request_ref=f"req-{delegation.get('delegation_id', 'unknown')}",
        response_ref=f"resp-{delegation.get('delegation_id', 'unknown')}",
        duration_ms=0.0,
        status="ok",
    )
