#!/usr/bin/env python3
"""MCP server for the baselayer — stdlib JSON-RPC 2.0 over stdio.

Implements the Baselayer §9 layer contract:
  - compile_context(target_files): must return the same closure as
    manifest traversal (AGENTS.md §1).
  - read_section(node_id): must return exactly sha256-verified byte_range.

Tools additionally exposed for convenience:
  - search_nodes(query): substring match on summaries/ids.
  - list_nodes(offset, limit): paginated node inventory.
  - knowledge_search(query): keyword search over the memory knowledge DB.
  - knowledge_last(kind): most recent memory entries of one kind.

Run:  python3 .agent/tools/mcp/server.py
Read-only: never writes .context/manifest.json or wiki/.
Env: reads keys from workspace .agent/.env (never committed).
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import signal
import sys
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger("mcp")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import context  # noqa: E402

PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {"name": "baselayer-mcp", "version": "0.2.0"}

# Request metrics
METRICS = {
    "request_count": 0,
    "total_latency_ms": 0.0,
    "total_token_bytes": 0,
    "verification_failures": 0,
    "errors": 0,
    "started_at": time.time(),
}

_SHUTDOWN = False


def handle_sigterm(signum, frame):
    global _SHUTDOWN
    _SHUTDOWN = True
    log.info("received SIGTERM, shutting down gracefully")


signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGINT, handle_sigterm)

TOOLS = [
    {
        "name": "compile_context",
        "description": "Return the requires-closure of node ids for given content files, following the baselayer manifest. Same result as AGENTS.md traversal.",
        "inputSchema": {
            "type": "object",
            "properties": {"target_files": {"type": "array", "items": {"type": "string"}}},
            "required": ["target_files"],
        },
    },
    {
        "name": "read_section",
        "description": "Return exactly the byte_range bytes of one manifest node, sha256-verified.",
        "inputSchema": {
            "type": "object",
            "properties": {"node_id": {"type": "string"}},
            "required": ["node_id"],
        },
    },
    {
        "name": "search_nodes",
        "description": "Substring search over node summaries and ids.",
        "inputSchema": {
            "type": "object",
            "properties": {"query": {"type": "string"}, "limit": {"type": "integer"}},
            "required": ["query"],
        },
    },
    {
        "name": "list_nodes",
        "description": "Paginated inventory of manifest nodes (id + summary).",
        "inputSchema": {
            "type": "object",
            "properties": {"offset": {"type": "integer"}, "limit": {"type": "integer"}},
        },
    },
    {
        "name": "knowledge_search",
        "description": "Keyword search over the memory knowledge DB (FTS5).",
        "inputSchema": {
            "type": "object",
            "properties": {"query": {"type": "string"}, "limit": {"type": "integer"}},
            "required": ["query"],
        },
    },
    {
        "name": "knowledge_last",
        "description": "Most recent memory entries of one kind (work/error/lesson/decision).",
        "inputSchema": {
            "type": "object",
            "properties": {"kind": {"type": "string"}, "limit": {"type": "integer"}},
        },
    },
    {
        "name": "wiki.search",
        "description": "Search wiki pages (conversation, prompt-chunk, conceptual-expansion) by keyword.",
        "inputSchema": {
            "type": "object",
            "properties": {"query": {"type": "string"}, "limit": {"type": "integer"}},
            "required": ["query"],
        },
    },
    {
        "name": "wiki.read",
        "description": "Read a wiki page by node ID, returning full markdown content with breadcrumb navigation.",
        "inputSchema": {
            "type": "object",
            "properties": {"node_id": {"type": "string"}},
            "required": ["node_id"],
        },
    },
]


def _tool_result(payload):
    return {"content": [{"type": "text", "text": json.dumps(payload, indent=2, ensure_ascii=False)}]}


def _record_request(tool_name: str, latency_ms: float, token_bytes: int, verification_failed: bool = False):
    METRICS["request_count"] += 1
    METRICS["total_latency_ms"] += latency_ms
    METRICS["total_token_bytes"] += token_bytes
    if verification_failed:
        METRICS["verification_failures"] += 1
    log.info(
        "mcp tool=%s latency_ms=%.1f token_bytes=%d verification_failed=%s",
        tool_name, latency_ms, token_bytes, verification_failed,
    )


def handle(msg):
    method = msg.get("method")
    mid = msg.get("id")
    params = msg.get("params") or {}

    def ok(result):
        return {"jsonrpc": "2.0", "id": mid, "result": result}

    def err(code, message):
        METRICS["errors"] += 1
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": code, "message": message}}

    if method == "initialize":
        return ok({
            "protocolVersion": params.get("protocolVersion", PROTOCOL_VERSION),
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": SERVER_INFO,
        })
    if method in ("notifications/initialized", "notifications/cancelled"):
        return None  # no response to notifications
    if method == "ping":
        return ok({"status": "healthy", "server": SERVER_INFO})
    if method == "tools/list":
        return ok({"tools": TOOLS})
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        start = time.time()
        verification_failed = False
        try:
            if name == "compile_context":
                result = context.compile_context(args.get("target_files", []))
                payload = _tool_result(result)
                token_bytes = len(json.dumps(payload).encode("utf-8"))
                _record_request(name, (time.time() - start) * 1000, token_bytes)
                return ok(payload)
            if name == "read_section":
                node_id = args["node_id"]
                nodes, _ = context._manifest_nodes()
                if node_id not in nodes:
                    METRICS["errors"] += 1
                    return err(-32000, f"unknown node: {node_id}")
                n = nodes[node_id]
                ref = n["content_ref"].split("#")[0]
                data = (context.ROOT / ref).read_bytes()
                s, e = n["byte_range"]
                chunk = data[s:e]
                expected = n["sha256"]
                actual = hashlib.sha256(chunk).hexdigest()
                if actual != expected:
                    METRICS["verification_failures"] += 1
                    METRICS["errors"] += 1
                    log.error("sha256 mismatch on %s: expected=%s actual=%s", node_id, expected, actual)
                    return err(-32000, f"sha256 mismatch on {node_id} — rebuild with python3 seed.py && python3 build.py")
                token_bytes = len(chunk)
                _record_request(name, (time.time() - start) * 1000, token_bytes)
                return ok(_tool_result({"node_id": node_id, "text": chunk.decode("utf-8", "replace")}))
            if name == "search_nodes":
                result = context.search_nodes(args.get("query", ""), args.get("limit", 20))
                payload = _tool_result(result)
                token_bytes = len(json.dumps(payload).encode("utf-8"))
                _record_request(name, (time.time() - start) * 1000, token_bytes)
                return ok(payload)
            if name == "list_nodes":
                result = context.list_nodes(args.get("limit", 50), args.get("offset", 0))
                payload = _tool_result(result)
                token_bytes = len(json.dumps(payload).encode("utf-8"))
                _record_request(name, (time.time() - start) * 1000, token_bytes)
                return ok(payload)
            if name == "knowledge_search":
                result = context.knowledge_search(args.get("query", ""), args.get("limit", 10))
                payload = _tool_result(result)
                token_bytes = len(json.dumps(payload).encode("utf-8"))
                _record_request(name, (time.time() - start) * 1000, token_bytes)
                return ok(payload)
            if name == "knowledge_last":
                result = context.knowledge_last(args.get("kind", "work"), args.get("limit", 5))
                payload = _tool_result(result)
                token_bytes = len(json.dumps(payload).encode("utf-8"))
                _record_request(name, (time.time() - start) * 1000, token_bytes)
                return ok(payload)
            if name == "wiki.search":
                result = context.search_nodes(args.get("query", ""), args.get("limit", 20))
                payload = _tool_result(result)
                token_bytes = len(json.dumps(payload).encode("utf-8"))
                _record_request(name, (time.time() - start) * 1000, token_bytes)
                return ok(payload)
            if name == "wiki.read":
                node_id = args["node_id"]
                nodes, _ = context._manifest_nodes()
                if node_id not in nodes:
                    METRICS["errors"] += 1
                    return err(-32000, f"unknown node: {node_id}")
                n = nodes[node_id]
                ref = n["content_ref"].split("#")[0]
                try:
                    data = (context.ROOT / ref).read_bytes()
                    s, e = n["byte_range"]
                    chunk = data[s:e]
                    content = chunk.decode("utf-8", "replace")
                except Exception as exc:
                    METRICS["errors"] += 1
                    return err(-32000, f"cannot read section: {exc}")
                payload = _tool_result({
                    "node_id": node_id,
                    "content_ref": n["content_ref"],
                    "title": n.get("summary", n["id"]),
                    "content": content,
                    "byte_range": [s, e],
                    "sha256": n.get("sha256", ""),
                })
                token_bytes = len(json.dumps(payload).encode("utf-8"))
                _record_request(name, (time.time() - start) * 1000, token_bytes)
                return ok(payload)
        except Exception as exc:  # surface as tool error, keep server alive
            METRICS["errors"] += 1
            log.exception("tool %s failed: %s", name, exc)
            return err(-32000, str(exc))
        return err(-32601, f"unknown tool: {name}")
    return err(-32601, f"method not found: {method}")


def main():
    # Load keys from .agent/.env (gitignored) into the environment.
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    if os.path.exists(env_path):
        for line in open(env_path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    log.info("MCP server starting: %s", SERVER_INFO)
    for raw in sys.stdin:
        if _SHUTDOWN:
            log.info("shutdown requested, exiting")
            break
        raw = raw.strip()
        if not raw:
            continue
        try:
            msg = json.loads(raw)
        except json.JSONDecodeError:
            METRICS["errors"] += 1
            log.warning("received invalid JSON, skipping")
            continue
        resp = handle(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
    log.info("MCP server stopped: requests=%d errors=%d verification_failures=%d",
             METRICS["request_count"], METRICS["errors"], METRICS["verification_failures"])


if __name__ == "__main__":
    main()
