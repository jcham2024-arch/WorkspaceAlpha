"""Tests for the retrieval-protocol layer of the prompt graph.

Covers the three things that were broken when this layer was added:

1. The prompt graph carries RetrievalProtocol nodes, and every one is
   reachable by a routes_to edge (otherwise the router can never pick it).
2. `.context/prompt-graph.yaml` is a generated mirror of the JSON and must
   not drift. The YAML previously held a duplicate `edges:` key, so a
   conformant loader kept the last 3 edges and silently dropped 18.
3. The assembler binds only the protocol the router selected, and downgrades
   to VECTOR with a provenance reason when a protocol's agent tier exceeds
   the caller's tier.
"""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "assembly"))

from budgeter import AGENT_TIER_BY_TARGET, AGENT_TIER_ORDER  # noqa: E402
from router import RoutingDecision  # noqa: E402

GRAPH_JSON = ROOT / ".context" / "prompt-graph.json"
GRAPH_YAML = ROOT / ".context" / "prompt-graph.yaml"

EXPECTED_PROTOCOLS = {"DIRECT", "STAIR", "VECTOR", "GRAPH", "PATTERN"}


def load_graph() -> dict:
    return json.loads(GRAPH_JSON.read_text(encoding="utf-8"))


class TestRetrievalProtocolNodes(unittest.TestCase):
    def setUp(self):
        self.graph = load_graph()
        self.protocols = {
            n["metadata"]["protocol"]: n
            for n in self.graph["nodes"]
            if n["type"] == "RetrievalProtocol"
        }

    def test_all_five_protocols_present(self):
        self.assertEqual(
            set(self.protocols),
            EXPECTED_PROTOCOLS,
            "prompt graph must declare one node per retrieval protocol",
        )

    def test_each_protocol_has_a_tool(self):
        for protocol, node in self.protocols.items():
            self.assertIn(
                "tool",
                node["metadata"],
                f"{protocol} node must name the tool that implements it",
            )

    def test_each_protocol_has_an_agent_tier(self):
        for protocol, node in self.protocols.items():
            self.assertIn(
                node.get("tier"),
                AGENT_TIER_ORDER,
                f"{protocol} node tier must be an agent tier, "
                f"got {node.get('tier')!r}",
            )

    def test_worker_forbidden_protocols_are_manager_tier(self):
        """PATTERN and GRAPH must not be reachable by a worker."""
        for protocol in ("PATTERN", "GRAPH"):
            self.assertEqual(
                self.protocols[protocol]["tier"],
                "manager",
                f"{protocol} must be manager tier",
            )

    def test_every_protocol_is_reachable_by_routes_to(self):
        routed = {
            e["to"] for e in self.graph["edges"] if e["type"] == "routes_to"
        }
        for protocol, node in self.protocols.items():
            self.assertIn(
                node["id"],
                routed,
                f"{node['id']} has no inbound routes_to edge — "
                f"the router can never select it",
            )

    def test_no_self_loops_or_duplicate_ids(self):
        ids = [n["id"] for n in self.graph["nodes"]]
        self.assertEqual(len(ids), len(set(ids)), "duplicate node id")
        for edge in self.graph["edges"]:
            self.assertNotEqual(
                edge["from"], edge["to"], f"self-loop on {edge['from']}"
            )


class TestYamlMirrorCoherence(unittest.TestCase):
    """The YAML is generated from the JSON and must not drift."""

    def test_yaml_matches_json(self):
        yaml = pytest_import_yaml()
        mirror = yaml.safe_load(GRAPH_YAML.read_text(encoding="utf-8"))
        graph = load_graph()
        self.assertEqual(
            {n["id"] for n in mirror["nodes"]},
            {n["id"] for n in graph["nodes"]},
            "YAML node set drifted from JSON — run tools/sync_prompt_graph.py",
        )
        self.assertEqual(
            {(e["from"], e["to"], e["type"]) for e in mirror["edges"]},
            {(e["from"], e["to"], e["type"]) for e in graph["edges"]},
            "YAML edge set drifted from JSON — run tools/sync_prompt_graph.py",
        )

    def test_yaml_has_no_duplicate_top_level_keys(self):
        """A duplicate `edges:` key silently discards edges on load."""
        text = GRAPH_YAML.read_text(encoding="utf-8")
        top_level = [
            line.split(":", 1)[0]
            for line in text.splitlines()
            if line and not line[0].isspace() and ":" in line and not line.startswith("#")
        ]
        duplicates = {k for k in top_level if top_level.count(k) > 1}
        self.assertEqual(
            duplicates, set(), f"duplicate top-level keys in YAML: {duplicates}"
        )

    def test_yaml_edge_count_is_complete(self):
        """Regression: the broken YAML exposed only 3 of 21+ edges."""
        yaml = pytest_import_yaml()
        mirror = yaml.safe_load(GRAPH_YAML.read_text(encoding="utf-8"))
        self.assertGreater(
            len(mirror["edges"]),
            10,
            "YAML lost edges — the duplicate-key regression is back",
        )


class TestTierCeilingMapping(unittest.TestCase):
    def test_thinking_maps_to_manager(self):
        self.assertEqual(AGENT_TIER_BY_TARGET["thinking"], "manager")

    def test_production_tiers_map_to_worker(self):
        self.assertEqual(AGENT_TIER_BY_TARGET["low_thinking"], "worker")
        self.assertEqual(AGENT_TIER_BY_TARGET["non_thinking"], "worker")


class TestProtocolBinding(unittest.TestCase):
    """The assembler must bind one protocol, not all five."""

    def setUp(self):
        from assembler import Assembler

        self.assembler = Assembler()

    def _delegation(self, **overrides):
        base = {
            "delegation_id": "test-protocol-binding",
            "from_agent": "conceptualizer",
            "to_agent": "taskmaster",
            "delegation_type": "MISSION",
            "target_tier": "low_thinking",
            "allowed_targets": ["docs/README.md"],
            "task_type": "planning",
            "task": "write a plan for the auth refactor",
            "profile": "conceptualizer",
        }
        base.update(overrides)
        return base

    def test_only_one_protocol_node_is_bound(self):
        result = self.assembler.assemble(self._delegation())
        bound = [
            n["node_id"]
            for n in result["assembled_nodes"]
            if n["node_id"].startswith("proto-")
        ]
        self.assertEqual(
            len(bound), 1, f"expected exactly one protocol node, got {bound}"
        )

    def test_worker_cannot_receive_manager_protocol(self):
        """A worker-tier delegation must not bind PATTERN or GRAPH."""
        forced = RoutingDecision(
            node_id="proto-pattern",
            protocol="PATTERN",
            confidence=0.9,
            rule_id="pattern-match-high-confidence",
            reason="simulated GPM hit",
        )
        original = self.assembler._apply_tier_ceiling
        self.assembler._apply_tier_ceiling = lambda decision, tier: original(
            forced, tier
        )
        try:
            result = self.assembler.assemble(self._delegation())
        finally:
            self.assembler._apply_tier_ceiling = original

        bound = [
            n["node_id"]
            for n in result["assembled_nodes"]
            if n["node_id"].startswith("proto-")
        ]
        self.assertEqual(bound, ["proto-vector"], "PATTERN must downgrade to VECTOR")

    def test_downgrade_is_recorded_in_provenance(self):
        forced = RoutingDecision(
            node_id="proto-graph",
            protocol="GRAPH",
            confidence=0.85,
            rule_id="relational-multihop",
            reason="simulated multihop query",
        )
        original = self.assembler._apply_tier_ceiling
        self.assembler._apply_tier_ceiling = lambda decision, tier: original(
            forced, tier
        )
        try:
            self.assembler.assemble(self._delegation())
        finally:
            self.assembler._apply_tier_ceiling = original

        turns = [
            json.loads(line)
            for line in (ROOT / "provenance" / "turns.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip()
        ]
        routing = turns[-1]["adapter_params"]["routing_decision"]
        self.assertEqual(routing["downgraded_from"], "GRAPH")
        self.assertEqual(routing["required_tier"], "manager")
        self.assertTrue(
            routing["reason"].startswith("tier_ceiling"),
            f"downgrade reason must be recorded, got {routing['reason']!r}",
        )


def pytest_import_yaml():
    try:
        import yaml
    except ImportError:  # pragma: no cover
        raise unittest.SkipTest("PyYAML not installed")
    return yaml


if __name__ == "__main__":
    unittest.main()
