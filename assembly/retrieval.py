#!/usr/bin/env python3
"""Execute the retrieval protocol the router selected.

The assembler binds a ``RetrievalProtocol`` node into the prompt; this module
is what actually calls the tool named in that node's ``metadata.tool`` and
turns the result into text the model can read.

Design constraints, all deliberate:

- **Never raise for an unavailable tool.** A missing vector index, an absent
  optional dependency or a tool that does not import is a normal condition in
  this workspace, not an error. The result carries ``status="unavailable"``
  and a reason, and the prompt gets a one-line marker instead of content.
  Failing the whole assembly because VECTOR has no index would make the
  default protocol unusable.
- **Bounded output.** Each protocol node declares a ``token_budget``. The
  executor truncates to it rather than letting a 2000-token retrieval blow a
  1500-token ceiling.
- **No LLM calls.** Retrieval is deterministic given the query and the index.
- **Every result is attributable.** Each carries the manifest ``node_id`` and
  ``byte_range`` it came from, so the assembler can record provenance and a
  human can audit the logic chain.

Stdlib only. Imports tools lazily so a broken tool cannot break import of the
assembler.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = ROOT / ".agent" / "tools"
ADAPTERS_DIR = ROOT / "adapters"


@dataclass
class RetrievedUnit:
    """One retrieved span, traceable to a manifest node."""

    node_id: str
    text: str
    score: float = 0.0
    byte_range: list[int] | None = None
    content_ref: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "score": self.score,
            "byte_range": self.byte_range,
            "content_ref": self.content_ref,
        }


@dataclass
class RetrievalResult:
    """Outcome of executing one protocol."""

    protocol: str
    status: str  # "ok" | "empty" | "unavailable"
    units: list[RetrievedUnit] = field(default_factory=list)
    text: str = ""
    tokens: int = 0
    reason: str | None = None
    truncated: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "protocol": self.protocol,
            "status": self.status,
            "reason": self.reason,
            "tokens": self.tokens,
            "truncated": self.truncated,
            "units": [u.to_dict() for u in self.units],
        }


def _unavailable(protocol: str, reason: str) -> RetrievalResult:
    return RetrievalResult(
        protocol=protocol,
        status="unavailable",
        reason=reason,
        text=f"<!-- retrieval {protocol} unavailable: {reason} -->",
    )


def _import_tool(tool_path: str):
    """Import a tool module by path, reusing an already-imported copy.

    Caching in ``sys.modules`` matters for two reasons: module-level work in a
    tool (loading the graph, the manifest, the GPM store) is not repeated on
    every retrieval, and tests can install a stub under the module name.
    """
    path = ROOT / tool_path
    if not path.exists():
        raise FileNotFoundError(f"tool not found: {tool_path}")

    cached = sys.modules.get(path.stem)
    if cached is not None:
        return cached

    for extra in (str(TOOLS_DIR), str(ADAPTERS_DIR), str(path.parent)):
        if extra not in sys.path:
            sys.path.insert(0, extra)

    import importlib.util

    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load spec for {tool_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        # Do not leave a half-initialised module cached.
        sys.modules.pop(path.stem, None)
        raise
    return module


def _approx_tokens(text: str) -> int:
    """Cheap token estimate — bytes//4, matching the adapter heuristic."""
    return len(text.encode("utf-8")) // 4


def _truncate(units: list[RetrievedUnit], max_tokens: int) -> tuple[list[RetrievedUnit], bool]:
    """Keep whole units while they fit. Never emits a partial unit."""
    kept: list[RetrievedUnit] = []
    used = 0
    for unit in units:
        cost = _approx_tokens(unit.text)
        if used + cost > max_tokens:
            return kept, True
        kept.append(unit)
        used += cost
    return kept, False


def _format(protocol: str, units: list[RetrievedUnit]) -> str:
    """Render retrieved units as a labelled block for the variable suffix.

    The header names the protocol and states the count so the model knows the
    provenance of the context it is reading, and so a human reading the
    assembled prompt can see which strategy produced it.
    """
    header = (
        f"## Retrieved context — {protocol} "
        f"({len(units)} unit{'s' if len(units) != 1 else ''})"
    )
    body = "\n\n".join(unit.text for unit in units)
    return f"{header}\n\n{body}"


# --- per-protocol executors -------------------------------------------------
# Each returns a list of RetrievedUnit. They raise only for genuinely
# exceptional conditions; expected absences are handled by the caller.


def _exec_direct(query: str, meta: dict, role: str) -> list[RetrievedUnit]:
    """DIRECT performs no retrieval — the skill node is already bound."""
    return []


def _exec_stair(query: str, meta: dict, role: str) -> list[RetrievedUnit]:
    module = _import_tool(meta.get("navigator", ".agent/tools/stair_navigator.py"))
    prediction = module.navigate(query)
    if prediction is None or not getattr(prediction, "node_id", None):
        return []
    return [
        RetrievedUnit(
            node_id=prediction.node_id,
            text=getattr(prediction, "content", "") or "",
            score=float(getattr(prediction, "confidence", 0.0) or 0.0),
            byte_range=getattr(prediction, "byte_range", None),
            content_ref=getattr(prediction, "content_ref", None),
        )
    ]


def _exec_vector(query: str, meta: dict, role: str) -> list[RetrievedUnit]:
    module = _import_tool(".agent/tools/vector_retriever.py")
    chunks = module.retrieve(
        query,
        max_results=int(meta.get("max_results", 5)),
        max_tokens=int(meta.get("max_tokens", 2000)),
    )
    return [
        RetrievedUnit(
            node_id=chunk.node_id,
            text=chunk.chunk_text,
            score=float(chunk.score),
            byte_range=[chunk.byte_range_start, chunk.byte_range_end],
            content_ref=chunk.content_ref,
        )
        for chunk in chunks
    ]


def _exec_graph(query: str, meta: dict, role: str) -> list[RetrievedUnit]:
    module = _import_tool(".agent/tools/graph_traverser.py")
    traverser = module.GraphTraverser()
    traverser._load_graph()
    # Start from the nodes that mention the query terms, so the traversal is
    # anchored rather than scanning the whole graph.
    starts = [n for n in traverser.nodes_by_id if _mentions(query, n)]
    if not starts:
        return []
    result = traverser.traverse(starts[:3], max_hops=3, max_nodes=8, role=role)
    units = []
    for node in result.get("nodes", []):
        summary = node.get("summary") or node.get("id", "")
        if not summary:
            continue
        units.append(
            RetrievedUnit(
                node_id=node.get("id", ""),
                text=f"- {node.get('id', '')}: {summary}",
                score=0.0,
            )
        )
    return units


def _exec_pattern(query: str, meta: dict, role: str) -> list[RetrievedUnit]:
    module = _import_tool(".agent/tools/pattern_retriever.py")
    try:
        retriever = module.PatternRetriever()
    except json.JSONDecodeError as exc:
        # An empty or partially written GPM store must not break assembly.
        raise FileNotFoundError(f"GPM store unreadable: {exc}") from exc
    pattern = retriever.retrieve(
        query, role=role, min_score=float(meta.get("min_score", 0.82))
    )
    if not pattern:
        return []
    skeleton = pattern.get("skeleton", [])
    if isinstance(skeleton, list):
        body = "\n".join(f"  {step}" for step in skeleton)
    else:
        body = str(skeleton)
    return [
        RetrievedUnit(
            node_id=f"pattern:{pattern.get('pattern_id', 'unknown')}",
            text=f"Reasoning scaffold ({pattern.get('type_signature', '')}):\n{body}",
            score=float(pattern.get("similarity_score", 0.0) or 0.0),
        )
    ]


def _mentions(query: str, node: dict) -> bool:
    """True if any query word of 4+ chars appears in the node's id or summary."""
    haystack = f"{node.get('id', '')} {node.get('summary', '')}".lower()
    return any(
        word in haystack
        for word in query.lower().split()
        if len(word) >= 4
    )


EXECUTORS = {
    "DIRECT": _exec_direct,
    "STAIR": _exec_stair,
    "VECTOR": _exec_vector,
    "GRAPH": _exec_graph,
    "PATTERN": _exec_pattern,
}


def execute(
    protocol: str,
    query: str,
    *,
    meta: dict | None = None,
    role: str = "taskmaster",
    max_tokens: int = 2000,
) -> RetrievalResult:
    """Run the named protocol and return bounded, attributable units.

    Never raises for a missing or broken tool: returns status
    ``"unavailable"`` with a reason instead.
    """
    meta = meta or {}
    executor = EXECUTORS.get(protocol)
    if executor is None:
        return _unavailable(protocol, f"no executor registered for {protocol!r}")

    try:
        units = executor(query, meta, role)
    except PermissionError as exc:
        # Protocol-level RBAC, e.g. a worker asking for PATTERN.
        return _unavailable(protocol, f"not permitted: {exc}")
    except FileNotFoundError as exc:
        return _unavailable(protocol, str(exc))
    except ImportError as exc:
        return _unavailable(protocol, f"import failed: {exc}")
    except Exception as exc:  # noqa: BLE001 - see contract above
        # A broken tool must not take down the assembly. Report the type so
        # the reason is diagnosable without a traceback in the prompt.
        return _unavailable(protocol, f"{type(exc).__name__}: {exc}")

    units = [u for u in units if u.text]
    if not units:
        return RetrievalResult(protocol=protocol, status="empty")

    kept, truncated = _truncate(units, max_tokens)
    if not kept:
        return RetrievalResult(
            protocol=protocol,
            status="empty",
            reason=f"all {len(units)} units exceeded the {max_tokens}-token cap",
            truncated=True,
        )

    text = _format(protocol, kept)
    return RetrievalResult(
        protocol=protocol,
        status="ok",
        units=kept,
        text=text,
        tokens=_approx_tokens(text),
        truncated=truncated,
    )
