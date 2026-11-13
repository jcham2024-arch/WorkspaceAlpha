#!/usr/bin/env python3
"""Assembler — DAG compiler pipeline (Plan → Bind → Optimize → Execute → Feedback).
Stdlib only. Never writes .context/manifest.json or wiki/.
"""
from __future__ import annotations

import hashlib, json, sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from budgeter import BLOCKED, Budgeter  # noqa: E402
from manifest_reader import ManifestReader  # noqa: E402
from slicer import Slicer  # noqa: E402
from tokenizer import TokenCounter  # noqa: E402
from provenance.recorder import ProvenanceRecorder  # noqa: E402
from telemetry.otel_genai import OTelGenAIRecorder  # noqa: E402
import plan, optimize, execute  # noqa: E402


class Assembler:
    def __init__(self, token_counter: TokenCounter | None = None):
        self.reader = ManifestReader()
        self.slicer = Slicer()
        self.budgeter = Budgeter(token_counter=token_counter)
        self._token_counter = token_counter
        self.provenance_recorder = ProvenanceRecorder()
        self.otel_recorder = OTelGenAIRecorder()

    def _apply_tier_ceiling(self, decision: Any, target_tier: str):
        return plan.apply_tier_ceiling(decision, target_tier, self.reader)

    def assemble(self, delegation: dict[str, Any]) -> dict[str, Any]:
        target_tier = delegation.get("target_tier", "low_thinking")
        allowed_targets = delegation.get("allowed_targets", [])
        protocol_node_id, routing_decision = plan.route_protocol(
            delegation, self.reader
        )
        protocol_node_id, routing_decision = self._apply_tier_ceiling(
            routing_decision, target_tier
        )
        manifest_node_ids = plan.resolve_scope(delegation, self.reader)
        plan.check_targets(allowed_targets, self.reader, self.budgeter) if not manifest_node_ids and allowed_targets else None
        envelope_node_ids = plan.find_envelope_nodes(
            delegation.get("delegation_type", ""), self.reader
        )
        required_nodes = self.reader.walk_requires(envelope_node_ids)
        triggered_nodes = self.reader.walk_triggers(
            envelope_node_ids, {"task_type": delegation.get("task_type", "")}
        )
        routed_nodes = self.reader.walk_routes_to(envelope_node_ids)
        candidate_ids = plan.bind_candidates(
            envelope_node_ids, required_nodes, triggered_nodes, routed_nodes, protocol_node_id
        )
        nodes_with_tokens = []
        for node_id in candidate_ids:
            graph_node = self.reader.get_graph_node(node_id)
            if graph_node is None:
                continue
            nodes_with_tokens.append(
                optimize.count_node_tokens(graph_node, self.reader, self.budgeter)
            )
        budget_result, ceiling = optimize.enforce_budget(
            nodes_with_tokens, target_tier, self.budgeter, root_node_ids=envelope_node_ids
        )
        prefix_parts: list[str] = []
        suffix_parts: list[str] = []
        assembled_nodes: list[dict[str, Any]] = []
        prefix_tokens = 0
        suffix_tokens = 0
        included = set(budget_result.included_nodes)
        for node in nodes_with_tokens:
            if node["node_id"] not in included:
                continue
            content = execute.render_node(node["node_id"], node["node_type"], self.reader)
            if node["node_type"] == "SystemPrompt":
                prefix_parts.append(content)
                prefix_tokens += node["token_count"]
            else:
                suffix_parts.append(content)
                suffix_tokens += node["token_count"]
            assembled_nodes.append(
                {
                    "node_id": node["node_id"],
                    "node_type": node["node_type"],
                    "token_count": node["token_count"],
                    "cache_hit": node["node_type"] == "SystemPrompt",
                    "token_count_method": node.get("token_count_method", "heuristic"),
                    "estimate_error_bound": node.get("estimate_error_bound", 0.2),
                }
            )
        retrieval_record = execute.run_retrieval(
            protocol_node_id, routing_decision, delegation,
            suffix_tokens, target_tier, self.reader, self.budgeter
        )
        if retrieval_record["text"]:
            variable_text = retrieval_record["text"]
            suffix_parts = (
                [variable_text] if not suffix_parts else [*suffix_parts, variable_text]
            )
            suffix_tokens += retrieval_record["tokens"]
            assembled_nodes.append(
                {
                    "node_id": f"retrieval:{retrieval_record['protocol'].lower()}",
                    "node_type": "RetrievalResult",
                    "token_count": retrieval_record["tokens"],
                    "cache_hit": False,
                    "token_count_method": "heuristic",
                    "estimate_error_bound": 0.2,
                }
            )
        frozen_prefix = "\n".join(prefix_parts)
        variable_suffix = "\n".join(suffix_parts)
        adapter_params = delegation.get("adapter_params", {})
        cache_input = frozen_prefix + json.dumps(adapter_params, sort_keys=True)
        cache_key = hashlib.sha256(cache_input.encode("utf-8")).hexdigest()
        cache_hit = all(
            n.get("cache_hit", False)
            for n in nodes_with_tokens
            if n["node_type"] == "SystemPrompt"
        )
        provenance_params = execute.build_provenance_params(
            delegation, adapter_params, routing_decision, retrieval_record
        )
        execute.record_provenance(
            delegation,
            assembled_nodes,
            {
                "prefix_tokens": prefix_tokens,
                "suffix_tokens": suffix_tokens,
                "total_tokens": prefix_tokens + suffix_tokens,
                "ceiling_tokens": ceiling,
                "budget_exceeded": (prefix_tokens + suffix_tokens) > ceiling,
            },
            provenance_params,
            delegation.get("return_envelope"),
            cache_hit,
            cache_key,
            budget_result.pruned_nodes,
        )
        execute.record_otel(
            delegation,
            adapter_params,
            prefix_tokens,
            suffix_tokens,
            budget_result,
            cache_key,
        )
        return {
            "blocked": False,
            "frozen_prefix": frozen_prefix,
            "variable_suffix": variable_suffix,
            "cache_key": cache_key,
            "assembled_nodes": assembled_nodes,
            "token_counts": {
                "prefix_tokens": prefix_tokens,
                "suffix_tokens": suffix_tokens,
                "total_tokens": prefix_tokens + suffix_tokens,
                "ceiling_tokens": ceiling,
                "budget_exceeded": (prefix_tokens + suffix_tokens) > ceiling,
            },
            "pruned_nodes": budget_result.pruned_nodes,
            "adapter_params": adapter_params,
            "retrieval": {
                k: v for k, v in retrieval_record.items() if k != "text"
            },
        }


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser(
        description="Assemble a two-zone prompt from a delegation JSON file"
    )
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
                {
                    "blocked": True,
                    "reason": exc.reason,
                    "excluded_nodes": exc.excluded_nodes,
                },
                indent=2,
            )
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
