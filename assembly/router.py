#!/usr/bin/env python3
# wa:allow-long-file
"""Router — selects the protocol (retrieval strategy) for a delegation.

Reads `.context/routing.rules.json` and evaluates rules in file order.
The first matching rule determines the protocol. Falls back to the
default protocol if no rule matches.

Routing decision is deterministic: same query + role always yields the
same protocol. No LLM calls are made during routing; rule matching is
purely string/pattern based.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / ".context" / "routing.rules.json"

class RoutingDecision:
    """Result of routing a delegation to a protocol."""

    def __init__(
        self,
        node_id: str,
        protocol: str,
        confidence: float,
        rule_id: str | None = None,
        reason: str | None = None,
    ):
        self.node_id = node_id
        self.protocol = protocol
        self.confidence = confidence
        self.rule_id = rule_id
        self.reason = reason or ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "protocol": self.protocol,
            "confidence": self.confidence,
            "rule_id": self.rule_id,
            "reason": self.reason,
        }

def _matches_condition(query: str, context: dict[str, Any], match: dict[str, Any]) -> bool:
    """Evaluate a single match condition against query + context."""
    for key, expected in match.items():
        if key == "query_mentions_path":
            if not expected:
                continue
            # Check if any allowed_targets path appears in query
            allowed = context.get("allowed_targets", [])
            if not any(t in query for t in allowed):
                return False
        elif key == "query_mentions_section_heading":
            if not expected:
                continue
            # Heuristic: check if query looks like it references a section heading
            heading_words = ["section", "chapter", "part", "heading"]
            if not any(w in query.lower() for w in heading_words):
                # Also check if query looks like a path with slashes
                if "/" not in query and "\\" not in query:
                    return False
        elif key == "query_has_multiple_entities":
            if not expected:
                continue
            # Heuristic: multiple capitalized words or quoted phrases suggest multiple entities
            words = re.findall(r"[A-Z][a-z]+", query)
            quoted = re.findall(r'"([^"]+)"', query)
            if len(words) + len(quoted) < 2:
                return False
        elif key == "query_asks_relationship":
            if not expected:
                continue
            relation_words = ["with", "and", "vs", "versus", "compare", "relationship", "connect", "link"]
            if not any(w in query.lower() for w in relation_words):
                return False
        elif key == "query_is_skill_invocation":
            if not expected:
                continue
            # Check if query looks like a skill invocation (imperative verb)
            imperative_verbs = ["run", "execute", "run", "invoke", "call", "do", "make", "create"]
            if not any(w in query.lower().split() for w in imperative_verbs):
                return False
        elif key == "role":
            # Role-based matching
            role = context.get("role", "")
            if expected:
                if isinstance(expected, list):
                    if role not in expected:
                        return False
                elif role != expected:
                    return False
        elif key == "gpm_top1_score_gte":
            # Cannot evaluate at route time; score not yet known
            # Assume match (will be evaluated later)
            pass
        else:
            # Unknown match key - fail closed
            return False
    return True

def route(
    query: str,
    *,
    profile: str = "conceptualizer",
    context: dict[str, Any] | None = None,
) -> RoutingDecision:
    """Route a delegation to a protocol.

    Args:
        query: The user query string.
        profile: The agent profile name (used for role-based matching).
        context: Additional context (delegation_type, target_tier, allowed_targets, etc.)

    Returns:
        RoutingDecision with node_id, protocol, confidence, rule_id, and reason.
    """
    context = context or {}

    # Load rules
    if not RULES_PATH.exists():
        raise FileNotFoundError(f"Routing rules not found: {RULES_PATH}")

    with RULES_PATH.open("r", encoding="utf-8") as f:
        rules_config = json.load(f)

    default_protocol = rules_config.get("default", "VECTOR")
    rules = rules_config.get("rules", [])

    # Evaluate rules in order
    for rule in rules:
        match = rule.get("match", {})
        if _matches_condition(query, context, match):
            protocol = rule.get("protocol", default_protocol)
            rule_id = rule.get("id", "unknown")
            reason = f"Matched rule '{rule_id}': {match}"

            # Map protocol to protocol node ID
            protocol_to_node = {
                "DIRECT": "proto-direct",
                "STAIR": "proto-stair",
                "VECTOR": "proto-vector",
                "GRAPH": "proto-graph",
                "PATTERN": "proto-pattern",
            }

            node_id = protocol_to_node.get(protocol)
            if not node_id:
                # Unknown protocol - fall back to default
                node_id = protocol_to_node.get(default_protocol, "proto-vector")
                protocol = default_protocol

            return RoutingDecision(
                node_id=node_id,
                protocol=protocol,
                confidence=1.0,
                rule_id=rule_id,
                reason=reason,
            )

    # No rule matched - use default protocol
    protocol = default_protocol
    protocol_to_node = {
        "DIRECT": "proto-direct",
        "STAIR": "proto-stair",
        "VECTOR": "proto-vector",
        "GRAPH": "proto-graph",
        "PATTERN": "proto-pattern",
    }
    node_id = protocol_to_node.get(protocol, "proto-vector")

    return RoutingDecision(
        node_id=node_id,
        protocol=protocol,
        confidence=0.5,  # Low confidence for default fallback
        rule_id="default",
        reason=f"No rule matched; defaulting to {protocol}",
    )

def main():
    """CLI: test the router."""
    import argparse

    ap = argparse.ArgumentParser(description="Router test")
    ap.add_argument("query", help="Query to route")
    ap.add_argument(
        "--profile", default="conceptualizer", help="Agent profile name"
    )
    ap.add_argument(
        "--delegation-type", default="MISSION", help="Delegation type"
    )
    ap.add_argument(
        "--target-tier", default="thinking", help="Target tier"
    )
    ap.add_argument(
        "--allowed-targets", nargs="*", default=[], help="Allowed target files"
    )
    args = ap.parse_args()

    context = {
        "delegation_type": args.delegation_type,
        "target_tier": args.target_tier,
        "allowed_targets": args.allowed_targets,
    }

    decision = route(args.query, profile=args.profile, context=context)
    print(json.dumps(decision.to_dict(), indent=2))

if __name__ == "__main__":
    main()
