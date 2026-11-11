#!/usr/bin/env python3
"""Wiki Generator — generates three human-readable views from provenance
records and the prompt DAG.

Views:
  1. Conversation — delegation chain transcript with evidence links
  2. Prompt Chunk — per-turn prompt composition (prefix, skills, slices, contract)
  3. Conceptual Expansion — why each node was selected, what was excluded, assumptions

Stdlib only. Reads provenance/ JSONL and .context/prompt-graph.json.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROVENANCE_DIR = ROOT / "provenance"
WIKI_DIR = ROOT / "wiki"
PROMPT_GRAPH_PATH = ROOT / ".context" / "prompt-graph.json"


class WikiGenerator:
    """Generates the three wiki views from provenance records."""

    def __init__(self):
        self.graph = None
        self._graph_nodes = None

    def _load_graph(self):
        if self.graph is None:
            if PROMPT_GRAPH_PATH.exists():
                with PROMPT_GRAPH_PATH.open("r", encoding="utf-8") as f:
                    self.graph = json.load(f)
                self._graph_nodes = {n["id"]: n for n in self.graph.get("nodes", [])}
            else:
                self.graph = {"nodes": [], "edges": []}
                self._graph_nodes = {}
        return self.graph, self._graph_nodes

    def get_node_info(self, node_id: str) -> dict | None:
        """Get graph node info by ID."""
        self._load_graph()
        return self._graph_nodes.get(node_id)

    def generate_conversation_view(
        self, delegation_id: str, records: list[dict]
    ) -> str:
        """Generate the Agent Conversation view.

        Shows per turn: from_agent → to_agent, delegation_type, authority,
        objective, acceptance criteria, return status linked to evidence slices.
        """
        if not records:
            return "# Conversation View\n\nNo records found.\n"

        lines = [
            "# Agent Conversation View",
            "",
            f"Delegation: `{delegation_id}`",
            "",
            "---",
            "",
        ]

        for i, record in enumerate(records, 1):
            from_agent = record.get("from_agent", "unknown")
            to_agent = record.get("to_agent", "unknown")
            delegation_type = record.get("delegation_type", "unknown")
            timestamp = record.get("turn_timestamp", "unknown")

            lines.extend(
                [
                    f"## Turn {i}",
                    "",
                    f"**{from_agent} → {to_agent}**",
                    "",
                    f"- **Type**: {delegation_type}",
                    f"- **Timestamp**: {timestamp}",
                    "",
                ]
            )

            # Objective and acceptance criteria from return envelope
            return_env = record.get("return_envelope", {})
            status = return_env.get("status", "unknown")
            steps_used = return_env.get("steps_used", "N/A")

            lines.append(f"- **Status**: {status}")
            lines.append(f"- **Steps Used**: {steps_used}")
            lines.append("")

            # Acceptance results with evidence
            acceptance = return_env.get("acceptance_results", [])
            if acceptance:
                lines.append("### Acceptance Criteria")
                lines.append("")
                for ar in acceptance:
                    criterion = ar.get("criterion", "?")
                    result = ar.get("result", "unknown")
                    evidence = ar.get("evidence", "no evidence")
                    lines.append(f"- **Criterion {criterion}**: {result}")
                    lines.append(f"  - Evidence: {evidence}")
                lines.append("")

            # Residual risks
            risks = return_env.get("residual_risks", [])
            if risks:
                lines.append("### Residual Risks")
                lines.append("")
                for risk in risks:
                    lines.append(f"- {risk}")
                lines.append("")

            lines.append("---")
            lines.append("")

        return "\n".join(lines)

    def generate_prompt_chunk_view(
        self, delegation_id: str, records: list[dict]
    ) -> str:
        """Generate the Prompt Chunk View.

        Shows per turn: frozen prefix (node ID, token count, cache hit),
        skill nodes (node ID, version, token count, trigger condition),
        context slices (node ID, byte range, token count),
        output contract (node ID, version, token count).
        """
        if not records:
            return "# Prompt Chunk View\n\nNo records found.\n"

        lines = [
            "# Prompt Chunk View",
            "",
            f"Delegation: `{delegation_id}`",
            "",
            "---",
            "",
        ]

        for i, record in enumerate(records, 1):
            lines.extend(
                [
                    f"## Turn {i}",
                    "",
                ]
            )

            assembled = record.get("assembled_nodes", [])
            token_counts = record.get("token_counts", {})

            # Separate prefix from suffix nodes
            prefix_nodes = [
                n for n in assembled if n.get("node_type") == "SystemPrompt"
            ]
            suffix_nodes = [
                n for n in assembled if n.get("node_type") != "SystemPrompt"
            ]

            # Frozen prefix
            lines.append("### Frozen Prefix (SystemPrompt)")
            lines.append("")
            for node in prefix_nodes:
                node_id = node.get("node_id", "unknown")
                token_count = node.get("token_count", 0)
                cache_hit = node.get("cache_hit", False)
                node_info = self.get_node_info(node_id)
                content_ref = node_info.get("content_ref", "unknown") if node_info else "unknown"
                lines.append(
                    f"- **{node_id}** ({content_ref})"
                )
                lines.append(f"  - Tokens: {token_count}")
                lines.append(f"  - Cache Hit: {cache_hit}")
            lines.append("")

            # Variable suffix - grouped by type
            lines.append("### Variable Suffix")
            lines.append("")

            # Skill nodes
            skill_nodes = [n for n in suffix_nodes if n.get("node_type") == "Skill"]
            if skill_nodes:
                lines.append("#### Skill Nodes")
                lines.append("")
                for node in skill_nodes:
                    node_id = node.get("node_id", "unknown")
                    token_count = node.get("token_count", 0)
                    node_info = self.get_node_info(node_id)
                    trigger = (
                        node_info.get("trigger_condition", "none")
                        if node_info
                        else "none"
                    )
                    lines.append(f"- **{node_id}**")
                    lines.append(f"  - Tokens: {token_count}")
                    lines.append(f"  - Trigger: {trigger}")
                lines.append("")

            # Context slices
            slice_nodes = [
                n for n in suffix_nodes if n.get("node_type") == "ContextSlice"
            ]
            if slice_nodes:
                lines.append("#### Context Slices")
                lines.append("")
                for node in slice_nodes:
                    node_id = node.get("node_id", "unknown")
                    token_count = node.get("token_count", 0)
                    byte_range = node.get("byte_range")
                    node_info = self.get_node_info(node_id)
                    manifest_ref = (
                        node_info.get("metadata", {}).get("manifest_node", "unknown")
                        if node_info
                        else "unknown"
                    )
                    lines.append(f"- **{node_id}** → `{manifest_ref}`")
                    lines.append(f"  - Tokens: {token_count}")
                    if byte_range:
                        lines.append(f"  - Byte Range: [{byte_range[0]}, {byte_range[1]}]")
                lines.append("")

            # Output contract
            contract_nodes = [
                n for n in suffix_nodes if n.get("node_type") == "OutputContract"
            ]
            if contract_nodes:
                lines.append("#### Output Contract")
                lines.append("")
                for node in contract_nodes:
                    node_id = node.get("node_id", "unknown")
                    token_count = node.get("token_count", 0)
                    node_info = self.get_node_info(node_id)
                    content_ref = (
                        node_info.get("content_ref", "unknown") if node_info else "unknown"
                    )
                    lines.append(f"- **{node_id}** ({content_ref})")
                    lines.append(f"  - Tokens: {token_count}")
                lines.append("")

            # Adapters
            adapter_nodes = [
                n for n in suffix_nodes if n.get("node_type") == "Adapter"
            ]
            if adapter_nodes:
                lines.append("#### Adapters")
                lines.append("")
                for node in adapter_nodes:
                    node_id = node.get("node_id", "unknown")
                    token_count = node.get("token_count", 0)
                    node_info = self.get_node_info(node_id)
                    model = (
                        node_info.get("metadata", {}).get("model", "unknown")
                        if node_info
                        else "unknown"
                    )
                    lines.append(f"- **{node_id}** ({model})")
                    lines.append(f"  - Tokens: {token_count}")
                lines.append("")

            # Token counts
            lines.append("### Token Counts")
            lines.append("")
            lines.append(f"- Prefix: {token_counts.get('prefix_tokens', 0)} tokens")
            lines.append(f"- Suffix: {token_counts.get('suffix_tokens', 0)} tokens")
            lines.append(f"- Total: {token_counts.get('total_tokens', 0)} tokens")
            lines.append(f"- Ceiling: {token_counts.get('ceiling_tokens', 'N/A')} tokens")
            lines.append(f"- Budget Exceeded: {token_counts.get('budget_exceeded', False)}")
            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)

    def generate_conceptual_expansion_view(
        self, delegation_id: str, records: list[dict]
    ) -> str:
        """Generate the Conceptual Expansion View.

        Shows per turn: why each node was selected, what was considered
        and excluded, what lean instructions assume, what human should verify.
        Each expansion carries a provenance signature.
        """
        if not records:
            return "# Conceptual Expansion View\n\nNo records found.\n"

        lines = [
            "# Conceptual Expansion View",
            "",
            f"Delegation: `{delegation_id}`",
            "",
            "---",
            "",
        ]

        for i, record in enumerate(records, 1):
            lines.extend(
                [
                    f"## Turn {i}",
                    "",
                ]
            )

            assembled = record.get("assembled_nodes", [])
            pruned = record.get("pruned_nodes", [])
            adapter_params = record.get("adapter_params", {})
            token_counts = record.get("token_counts", {})

            # Why each node was selected
            lines.append("### Node Selection Rationale")
            lines.append("")
            for node in assembled:
                node_id = node.get("node_id", "unknown")
                node_type = node.get("node_type", "unknown")
                node_info = self.get_node_info(node_id)

                reason = self._infer_selection_reason(
                    node_id, node_type, node_info, record
                )
                lines.append(f"- **{node_id}** ({node_type}): {reason}")
            lines.append("")

            # What was considered and excluded
            lines.append("### Excluded Nodes (Pruned by Budget)")
            lines.append("")
            if pruned:
                for node_id in pruned:
                    node_info = self.get_node_info(node_id)
                    node_type = (
                        node_info.get("type", "unknown") if node_info else "unknown"
                    )
                    lines.append(f"- **{node_id}** ({node_type}): pruned — budget ceiling exceeded")
            else:
                lines.append("- None — all candidate nodes fit within budget")
            lines.append("")

            # Lean instruction assumptions
            lines.append("### Lean Instruction Assumptions")
            lines.append("")
            lines.append(
                "- The orchestrator assumes the manager has read the full context slices."
            )
            lines.append(
                "- The manager assumes the production worker understands the public API contract."
            )
            lines.append(
                "- Skills are assumed to be applicable based on trigger conditions only."
            )
            lines.append("")

            # What human should verify
            lines.append("### Human Verification Checklist")
            lines.append("")
            lines.append("- [ ] Verify acceptance criterion evidence links resolve to actual file:line locations")
            lines.append("- [ ] Confirm pruned nodes don't contain critical context for this delegation")
            lines.append("- [ ] Validate that the return envelope status matches observable results")
            lines.append("- [ ] Check that cache hits are legitimate (prefix content unchanged)")
            lines.append("")

            # Provenance signature
            lines.append("### Provenance Signature")
            lines.append("")
            cache_key = record.get("cache_key", "unknown")
            timestamp = record.get("turn_timestamp", "unknown")
            adapter_model = adapter_params.get("model", "unknown") if isinstance(adapter_params, dict) else "unknown"

            # Compute a content hash of the assembled nodes for provenance
            node_hash_input = json.dumps(
                sorted([n.get("node_id", "") for n in assembled]), sort_keys=True
            )
            node_hash = hashlib.sha256(node_hash_input.encode("utf-8")).hexdigest()[:12]

            lines.append(f"- **Delegation ID**: `{delegation_id}`")
            lines.append(f"- **Turn Timestamp**: {timestamp}")
            lines.append(f"- **Cache Key**: `{cache_key}`")
            lines.append(f"- **Node Hash**: `{node_hash}`")
            lines.append(f"- **Adapter Model**: {adapter_model}")
            lines.append(f"- **Assembled Node Count**: {len(assembled)}")
            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)

    def _infer_selection_reason(
        self, node_id: str, node_type: str, node_info: dict | None, record: dict
    ) -> str:
        """Infer why a node was selected for this turn."""
        delegation_type = record.get("delegation_type", "")

        if node_type == "SystemPrompt":
            return f"Required for {delegation_type} delegation — establishes identity, invariants, and workflow protocol"
        if node_type == "Envelope":
            metadata = node_info.get("metadata", {}) if node_info else {}
            dtype = metadata.get("delegation_type", delegation_type)
            return f"Defines the {dtype} delegation contract — authority, targets, and return schema"
        if node_type == "Skill":
            trigger = (
                node_info.get("trigger_condition", "")
                if node_info
                else ""
            )
            if trigger:
                return f"Trigger condition matched: {trigger}"
            return "Selected as a supporting skill for this delegation type"
        if node_type == "ContextSlice":
            manifest_ref = (
                node_info.get("metadata", {}).get("manifest_node", "unknown")
                if node_info
                else "unknown"
            )
            return f"Provides context from {manifest_ref} — byte-range slice for verified evidence"
        if node_type == "Adapter":
            metadata = node_info.get("metadata", {}) if node_info else {}
            model = metadata.get("model", "unknown")
            return f"Configures model dispatch for {model}"
        if node_type == "OutputContract":
            return "Defines the return envelope schema for result validation"
        return "Selected as part of the delegation assembly"

    def generate_all_views(
        self, delegation_id: str, output_dir: Path | None = None
    ) -> dict[str, str]:
        """Generate all three views for a delegation and write to files."""
        records = []
        jsonl_path = PROVENANCE_DIR / "turns.jsonl"
        if jsonl_path.exists():
            with jsonl_path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        record = json.loads(line)
                        if record.get("delegation_id") == delegation_id:
                            records.append(record)
                    except json.JSONDecodeError:
                        continue

        if not records:
            return {}

        conversation = self.generate_conversation_view(delegation_id, records)
        prompt_chunk = self.generate_prompt_chunk_view(delegation_id, records)
        conceptual = self.generate_conceptual_expansion_view(delegation_id, records)

        output_dir = output_dir or WIKI_DIR
        output_dir.mkdir(parents=True, exist_ok=True)

        written = {}
        views = {
            "conversation": conversation,
            "prompt-chunk": prompt_chunk,
            "conceptual-expansion": conceptual,
        }

        for view_name, content in views.items():
            view_path = output_dir / f"{view_name}.md"
            view_path.write_text(content, encoding="utf-8")
            written[view_name] = str(view_path)

        # Also generate an index page
        index_path = output_dir / "index.md"
        index_content = self._generate_index(delegation_id, records)
        index_path.write_text(index_content, encoding="utf-8")
        written["index"] = str(index_path)

        return written

    def _generate_index(self, delegation_id: str, records: list[dict]) -> str:
        """Generate an index page linking to all views."""
        latest = records[-1] if records else {}
        return_env = latest.get("return_envelope", {})
        status = return_env.get("status", "unknown")

        lines = [
            f"# Wiki Index: Delegation {delegation_id}",
            "",
            f"- **Status**: {status}",
            f"- **Turns**: {len(records)}",
            "",
            "## Views",
            "",
            "- [Conversation](conversation.md) — Delegation chain transcript with evidence links",
            "- [Prompt Chunk](prompt-chunk.md) — Per-turn prompt composition (prefix, skills, slices, contract)",
            "- [Conceptual Expansion](conceptual-expansion.md) — Why each node was selected, what was excluded, assumptions",
            "",
            "---",
            "",
            "*Generated from provenance records and prompt DAG.*",
        ]
        return "\n".join(lines)


def main():
    """CLI: generate wiki views for a delegation."""
    import argparse

    ap = argparse.ArgumentParser(description="Generate wiki views from provenance")
    ap.add_argument("delegation_id", help="Delegation ID to generate views for")
    ap.add_argument(
        "--output-dir",
        default=str(WIKI_DIR),
        help="Output directory (default: wiki/)",
    )
    args = ap.parse_args()

    generator = WikiGenerator()
    written = generator.generate_all_views(args.delegation_id, Path(args.output_dir))

    if written:
        for view_name, path in written.items():
            print(f"Wrote {view_name}: {path}")
    else:
        print(f"No records found for delegation {delegation_id}")


if __name__ == "__main__":
    main()
