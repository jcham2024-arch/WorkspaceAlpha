#!/usr/bin/env python3
"""Sync prompt-graph.yaml from prompt-graph.json.

The JSON is the runtime source of truth: assembly/manifest_reader.py,
.agent/tools/graph_traverser.py and wiki/views/generator.py all read
`.context/prompt-graph.json`. The YAML existed only as a human-readable
mirror, and had drifted — it carried a duplicate `edges:` key, so a
conformant YAML loader silently kept the last 3 edges and discarded the
first 18, while the JSON had all of them. tools/validate_prompt_graph.py
validated the YAML, so the gate was checking the stale copy.

Run this after editing the JSON. It refuses to write if the YAML would
not round-trip to an identical graph.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / ".context" / "prompt-graph.json"
YAML_PATH = ROOT / ".context" / "prompt-graph.yaml"

HEADER = """\
# Prompt DAG — human-readable mirror of .context/prompt-graph.json.
# Generated file: do not edit by hand.
# Edit the JSON, then run: python3 tools/sync_prompt_graph.py
# tools/validate_prompt_graph.py fails if this file drifts from the JSON.
"""


def q(value) -> str:
    """Render a scalar as a YAML scalar."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    unsafe = any(c in text for c in ':#"\'{}[]&*!|>%@`')
    if unsafe or text.strip() != text or text == "":
        return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return text


def render(graph: dict) -> str:
    lines = [HEADER.rstrip(), 'version: "1.0.0"', "", "nodes:"]
    for node in graph["nodes"]:
        lines.append(f'  - id: {node["id"]}')
        lines.append(f'    type: {node["type"]}')
        if "content_ref" in node:
            lines.append(f'    content_ref: {q(node["content_ref"])}')
        for key in ("tier", "token_budget"):
            if key in node:
                lines.append(f"    {key}: {q(node[key])}")
        if "trigger_condition" in node:
            lines.append(f'    trigger_condition: {q(node["trigger_condition"])}')
        if "metadata" in node:
            if not node["metadata"]:
                lines.append("    metadata: {}")
            else:
                lines.append("    metadata:")
                for mk, mv in node["metadata"].items():
                    lines.append(f"      {mk}: {q(mv)}")
        lines.append("")

    lines.append("edges:")
    for edge in graph["edges"]:
        lines.append(f'  - from: {edge["from"]}')
        lines.append(f'    to: {edge["to"]}')
        lines.append(f'    type: {edge["type"]}')
        if "condition" in edge:
            lines.append(f'    condition: {q(edge["condition"])}')
        if "note" in edge:
            lines.append(f'    note: {q(edge["note"])}')
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def signature(graph: dict) -> tuple:
    return (
        tuple(sorted(n["id"] for n in graph["nodes"])),
        tuple(sorted((e["from"], e["to"], e["type"]) for e in graph["edges"])),
    )


def main() -> int:
    graph = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    rendered = render(graph)

    try:
        import yaml
    except ImportError:
        print("FAIL: PyYAML not installed", file=sys.stderr)
        return 1

    # Round-trip check: what we are about to write must parse back to the
    # same node and edge sets. This is the exact failure the old YAML had.
    reparsed = yaml.safe_load(rendered)
    if signature(reparsed) != signature(graph):
        print("FAIL: rendered YAML does not round-trip to the JSON graph")
        return 1

    if YAML_PATH.exists() and YAML_PATH.read_text(encoding="utf-8") == rendered:
        print(f"unchanged: {YAML_PATH.relative_to(ROOT)}")
        return 0

    YAML_PATH.write_text(rendered, encoding="utf-8")
    print(f"wrote {YAML_PATH.relative_to(ROOT)}: "
          f"{len(graph['nodes'])} nodes, {len(graph['edges'])} edges")
    return 0


if __name__ == "__main__":
    sys.exit(main())
