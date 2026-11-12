#!/usr/bin/env python3
"""Assembler — orchestrates the DAG compiler pipeline (Plan → Bind → Optimize → Execute → Feedback).

Reads the prompt graph and manifest, resolves scope from a delegation envelope,
assembles a two-zone prompt (frozen prefix + variable suffix), enforces token
budgets, and returns the assembled prompt plus provenance metadata.

Stdlib only. Never writes .context/manifest.json or wiki/.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

# Add assembly directory to path for sibling imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manifest_reader import ManifestReader  # noqa: E402
from slicer import Slicer, SliceOutOfBounds  # noqa: E402
from budgeter import Budgeter, TIER_CEILINGS, AGENT_TIER_BY_TARGET, AGENT_TIER_ORDER  # noqa: E402
from tokenizer import TokenCounter  # noqa: E402
from provenance.recorder import ProvenanceRecorder  # noqa: E402
from telemetry.otel_genai import OTelGenAIRecorder  # noqa: E402
from router import route  # noqa: E402
from router import RoutingDecision  # noqa: E402


class BLOCKED(Exception):
    """Raised when assembly is blocked (budget exceeded or target not in manifest)."""

    def __init__(self, reason: str, excluded_nodes: list[str] | None = None):
        self.reason = reason
        self.excluded_nodes = excluded_nodes or []
        super().__init__(reason)


class Assembler:
    """Two-zone prompt assembler with budget enforcement and cache-keyed rendering."""

    def __init__(self, token_counter: TokenCounter | None = None):
        self.reader = ManifestReader()
        self.slicer = Slicer()
        self.budgeter = Budgeter(token_counter=token_counter)
        self._token_counter = token_counter
        self.provenance_recorder = ProvenanceRecorder()
        self.otel_recorder = OTelGenAIRecorder()

    def assemble(
        self,
        delegation: dict[str, Any],
    ) -> dict[str, Any]:
        """Assemble a two-zone prompt from a delegation envelope.

        Args:
            delegation: Dict with delegation envelope fields:
              - delegation_id, from_agent, to_agent, delegation_type, target_tier,
                authority, allowed_targets, forbidden_targets, return_schema, return_format

        Returns:
            Dict with:
              - frozen_prefix: str (SystemPrompt content)
              - variable_suffix: str (assembled task envelope)
              - cache_key: str (SHA-256 of prefix + adapter params)
              - assembled_nodes: list[dict] with node_id, node_type, token_count,
                cache_hit, token_count_method, estimate_error_bound
              - token_counts: dict with prefix_tokens, suffix_tokens, total_tokens,
                ceiling_tokens, budget_exceeded
              - pruned_nodes: list[str]
              - blocked: bool (False if successful)

        Raises:
            BLOCKED: If target not in manifest or budget exceeded.
        """
        delegation_id = delegation.get("delegation_id", "unknown")
        target_tier = delegation.get("target_tier", "low_thinking")
        allowed_targets = delegation.get("allowed_targets", [])
        task_type = delegation.get("task_type", "")
        delegation_type = delegation.get("delegation_type", "")

        # Phase 0 — Route: determine protocol via router
        from router import route as route_query

        routing_decision = route_query(
            query=delegation.get("task", ""),
            profile=delegation.get("profile", "conceptualizer"),
            context={
                "delegation_type": delegation_type,
                "target_tier": target_tier,
                "allowed_targets": allowed_targets,
            },
        )
        protocol_node_id, routing_decision = self._apply_tier_ceiling(
            routing_decision, target_tier
        )

        # Phase 1 — Plan: resolve scope from delegation envelope
        scope = {
            "task_type": task_type,
            "domain": delegation.get("domain", ""),
            "target_tier": target_tier,
        }

        # Resolve manifest nodes matching allowed_targets
        manifest_node_ids = self.reader.resolve_scope(
            task_type=task_type,
            domain=scope["domain"],
            allowed_targets=allowed_targets if allowed_targets else None,
            target_tier=target_tier,
        )

        if not manifest_node_ids and allowed_targets:
            # Check if any of the allowed targets exist in manifest
            for target in allowed_targets:
                reason = self.budgeter.check_target_in_manifest(
                    target, self.reader._nodes
                )
                if reason:
                    raise BLOCKED(reason)

        # Phase 2 — Bind: walk graph edges from envelope nodes
        # Start from envelope nodes, walk requires/triggers/routes_to
        envelope_node_ids = self._find_envelope_nodes(delegation_type)

        # Walk requires transitively
        required_nodes = self.reader.walk_requires(envelope_node_ids)

        # Walk triggers with scope matching
        triggered_nodes = self.reader.walk_triggers(envelope_node_ids, scope)

        # Walk routes_to
        routed_nodes = self.reader.walk_routes_to(envelope_node_ids)

        # Combine all candidate nodes (deduplicated)
        candidate_ids = list(
            dict.fromkeys(
                envelope_node_ids + required_nodes + triggered_nodes + routed_nodes
            )
        )

        # Keep only the protocol the router selected. The other proto-*
        # nodes are alternatives reachable from the same envelopes; binding
        # all five would put every retrieval strategy into one prompt, which
        # both blows the budget and defeats the point of routing.
        candidate_ids = [
            node_id
            for node_id in candidate_ids
            if not node_id.startswith("proto-") or node_id == protocol_node_id
        ]

        # Add the selected protocol node as first candidate
        if protocol_node_id and protocol_node_id not in candidate_ids:
            candidate_ids.insert(0, protocol_node_id)

        # Phase 3 — Optimize: read byte ranges and count tokens
        nodes_with_tokens = []
        for node_id in candidate_ids:
            graph_node = self.reader.get_graph_node(node_id)
            if graph_node is None:
                continue

            node_type = graph_node.get("type", "Skill")
            token_budget = graph_node.get("token_budget", 0)
            edge_distance = graph_node.get("metadata", {}).get("edge_distance", 0)

            # Count tokens using the configured TokenCounter
            actual_tokens = token_budget
            content_ref = graph_node.get("content_ref", "")
            content_text = ""

            if node_type == "ContextSlice":
                # Read exact bytes from manifest
                manifest_node_id = graph_node.get(
                    "metadata", {}
                ).get("manifest_node", node_id)
                try:
                    chunk = self.slicer.slice_node(manifest_node_id)
                    content_text = chunk.decode("utf-8", errors="replace")
                except SliceOutOfBounds:
                    content_text = ""
            elif node_type == "SystemPrompt":
                # Read frozen prefix file
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
                actual_tokens = self.budgeter.count_tokens(
                    content_text, model_id=graph_node.get("metadata", {}).get("model")
                )
            else:
                actual_tokens = token_budget

            nodes_with_tokens.append(
                {
                    "node_id": node_id,
                    "node_type": node_type,
                    "token_count": actual_tokens,
                    "edge_distance": edge_distance,
                    "token_count_method": (
                        self.budgeter._counter.__class__.__name__
                        if self.budgeter._counter
                        else "heuristic"
                    ),
                    "estimate_error_bound": (
                        0.0 if self.budgeter._counter is not None else 0.2
                    ),
                }
            )

        # Phase 4 — Execute: enforce budget
        ceiling = self.budgeter.get_ceiling(target_tier)
        budget_result = self.budgeter.enforce_budget(
            nodes_with_tokens, target_tier, root_node_ids=envelope_node_ids
        )

        if not budget_result.within_budget:
            raise BLOCKED(
                budget_result.blocked_reason or "CONTEXT_BUDGET_EXCEEDED",
                budget_result.pruned_nodes,
            )

        # Phase 5 — Render: build two-zone prompt
        prefix_parts = []
        suffix_parts = []
        assembled_nodes = []
        prefix_tokens = 0
        suffix_tokens = 0

        for node in nodes_with_tokens:
            if node["node_id"] not in budget_result.included_nodes:
                continue

            node_type = node["node_type"]
            node_id = node["node_id"]
            token_count = node["token_count"]

            # Get content
            content = self._render_node(node_id, node_type)

            if node_type == "SystemPrompt":
                prefix_parts.append(content)
                prefix_tokens += token_count
            else:
                suffix_parts.append(content)
                suffix_tokens += token_count

            assembled_nodes.append(
                {
                    "node_id": node_id,
                    "node_type": node_type,
                    "token_count": token_count,
                    "cache_hit": node_type == "SystemPrompt",
                    "token_count_method": node.get(
                        "token_count_method", "heuristic"
                    ),
                    "estimate_error_bound": node.get(
                        "estimate_error_bound", 0.2
                    ),
                }
            )

        frozen_prefix = "\n".join(prefix_parts)
        variable_suffix = "\n".join(suffix_parts)

        # Compute cache key: SHA-256 of prefix + adapter params
        adapter_params = delegation.get("adapter_params", {})
        cache_input = frozen_prefix + json.dumps(adapter_params, sort_keys=True)
        cache_key = hashlib.sha256(cache_input.encode("utf-8")).hexdigest()
        cache_hit = all(n.get("cache_hit", False) for n in nodes_with_tokens if n["node_type"] == "SystemPrompt")

        # Phase 6 — Record provenance and OTel spans
        assembled_nodes_list = []
        for n in nodes_with_tokens:
            if n["node_id"] not in budget_result.included_nodes:
                continue
            graph_node = self.reader.get_graph_node(n["node_id"])
            byte_range = None
            if graph_node:
                byte_range = graph_node.get("byte_range")
            assembled_nodes_list.append(
                {
                    "node_id": n["node_id"],
                    "node_type": n["node_type"],
                    "token_count": n["token_count"],
                    "cache_hit": n.get("cache_hit", False),
                    "byte_range": byte_range,
                }
            )

        # Record provenance (Record A — no raw prompt text)
        routing_record = {
            "protocol": routing_decision.protocol,
            "node_id": protocol_node_id,
            "confidence": routing_decision.confidence,
            "rule_id": routing_decision.rule_id,
            "reason": routing_decision.reason,
        }
        downgraded_from = getattr(routing_decision, "downgraded_from", None)
        if downgraded_from:
            routing_record["downgraded_from"] = downgraded_from
            routing_record["required_tier"] = getattr(
                routing_decision, "required_tier", None
            )
            routing_record["tier_ceiling"] = target_tier

        provenance_params = {
            **adapter_params,
            "routing_decision": routing_record,
        }
        self.provenance_recorder.record_turn(
            delegation_id=delegation_id,
            from_agent=delegation.get("from_agent", "unknown"),
            to_agent=delegation.get("to_agent", "unknown"),
            delegation_type=delegation.get("delegation_type", ""),
            target_tier=target_tier,
            assembled_nodes=assembled_nodes_list,
            token_counts=budget_result.to_dict(),
            adapter_params=provenance_params,
            return_envelope=delegation.get("return_envelope"),
            cache_hit=cache_hit,
            cache_key=cache_key,
            pruned_nodes=budget_result.pruned_nodes,
        )

        # Record OTel spans
        self.otel_recorder.record_chat_span(
            span_id=f"span-{delegation_id}-chat",
            trace_id=delegation.get("trace_id", delegation_id),
            model_name=adapter_params.get("model", "unknown"),
            provider=adapter_params.get("model", "deepseek-v3.2").split("-")[0],
            input_tokens=prefix_tokens,
            output_tokens=suffix_tokens,
            finish_reason="stop" if not budget_result.to_dict().get("budget_exceeded", False) else "length",
            temperature=adapter_params.get("temperature"),
            max_tokens=adapter_params.get("max_tokens"),
            system_prompt_hash=cache_key,
            request_ref=f"req-{delegation_id}",
            response_ref=f"resp-{delegation_id}",
            duration_ms=0.0,
            status="ok",
        )

        return {
            "blocked": False,
            "frozen_prefix": frozen_prefix,
            "variable_suffix": variable_suffix,
            "cache_key": cache_key,
            "assembled_nodes": assembled_nodes_list,
            "token_counts": {
                "prefix_tokens": prefix_tokens,
                "suffix_tokens": suffix_tokens,
                "total_tokens": budget_result.to_dict().get("total_tokens", prefix_tokens + suffix_tokens),
                "ceiling_tokens": ceiling,
                "budget_exceeded": budget_result.blocked_reason is not None,
            },
            "pruned_nodes": budget_result.pruned_nodes,
            "adapter_params": adapter_params,
        }

    def _find_envelope_nodes(self, delegation_type: str) -> list[str]:
        """Find envelope node IDs matching the delegation type."""
        self.reader._load_graph()
        result = []
        for node_id, node in self.reader._graph_nodes.items():
            if node.get("type") == "Envelope":
                metadata = node.get("metadata", {})
                if metadata.get("delegation_type") == delegation_type:
                    result.append(node_id)
        return result

    def _apply_tier_ceiling(self, decision, target_tier: str):
        """Downgrade a protocol whose agent tier exceeds the caller's tier.

        A worker-tier caller cannot run a manager-only protocol such as
        PATTERN or GRAPH. Per the retrieval directive §8, the downgrade is
        to VECTOR and is recorded in provenance with reason
        ``tier_ceiling``. Returns (protocol_node_id, decision).

        ``RoutingDecision`` carries no tier of its own, so the required tier
        is read from the graph node the router selected.
        """
        node = self.reader.get_graph_node(decision.node_id)
        required = (node or {}).get("tier")
        caller = AGENT_TIER_BY_TARGET.get(target_tier)

        # An unmapped tier means we cannot prove the caller is allowed, so do
        # not downgrade — routing rules already ran and the ceiling is a
        # separate safety net, not the primary gate.
        if required not in AGENT_TIER_ORDER or caller not in AGENT_TIER_ORDER:
            return decision.node_id, decision
        if AGENT_TIER_ORDER[required] <= AGENT_TIER_ORDER[caller]:
            return decision.node_id, decision

        fallback = self.reader.get_graph_node("proto-vector")
        if fallback is None:
            # No safe fallback exists. Failing closed is correct: a
            # worker must not silently receive a manager-only protocol.
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

    def _render_node(self, node_id: str, node_type: str) -> str:
        """Render a node's content for inclusion in the prompt."""
        if node_type == "SystemPrompt":
            graph_node = self.reader.get_graph_node(node_id)
            if graph_node:
                content_ref = graph_node.get("content_ref", "")
                try:
                    path = ROOT / content_ref
                    if path.exists():
                        return path.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    pass
            return f"<!-- SystemPrompt {node_id} content unavailable -->"

        elif node_type == "Skill":
            graph_node = self.reader.get_graph_node(node_id)
            if graph_node:
                content_ref = graph_node.get("content_ref", "")
                try:
                    path = ROOT / content_ref
                    if path.exists():
                        return path.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    pass
            return f"<!-- Skill {node_id} content unavailable -->"

        elif node_type == "Envelope":
            graph_node = self.reader.get_graph_node(node_id)
            if graph_node:
                metadata = graph_node.get("metadata", {})
                return f"<!-- Envelope: {metadata.get('delegation_type', 'unknown')} -- authority: {metadata.get('authority', 'unknown')} -->"
            return f"<!-- Envelope {node_id} -->"

        elif node_type == "ContextSlice":
            graph_node = self.reader.get_graph_node(node_id)
            if graph_node:
                manifest_node_id = graph_node.get(
                    "metadata", {}
                ).get("manifest_node", node_id)
                try:
                    return self.slicer.slice_node_text(manifest_node_id)
                except SliceOutOfBounds as exc:
                    return f"<!-- ContextSlice {node_id}: {exc} -->"
            return f"<!-- ContextSlice {node_id} unavailable -->"

        elif node_type == "Adapter":
            graph_node = self.reader.get_graph_node(node_id)
            if graph_node:
                metadata = graph_node.get("metadata", {})
                model = metadata.get("model", "unknown")
                return f"<!-- Adapter: {model} -->"
            return f"<!-- Adapter {node_id} -->"

        elif node_type == "OutputContract":
            graph_node = self.reader.get_graph_node(node_id)
            if graph_node:
                content_ref = graph_node.get("content_ref", "")
                return f"<!-- OutputContract: {content_ref} -->"
            return f"<!-- OutputContract {node_id} -->"

        return f"<!-- Unknown node type {node_type}: {node_id} -->"


def main():
    """CLI: assemble a prompt from a delegation JSON file."""
    import argparse

    ap = argparse.ArgumentParser(description="Assemble a two-zone prompt from a delegation")
    ap.add_argument("delegation_file", help="Path to delegation JSON file")
    args = ap.parse_args()

    with open(args.delegation_file, "r", encoding="utf-8") as f:
        delegation = json.load(f)

    assembler = Assembler()
    try:
        result = assembler.assemble(delegation)
        print(json.dumps(result, indent=2))
    except BLOCKED as exc:
        print(
            json.dumps(
                {"blocked": True, "reason": exc.reason, "excluded_nodes": exc.excluded_nodes},
                indent=2,
            )
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
