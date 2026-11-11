#!/usr/bin/env python3
"""MCP server for the baselayer — stdlib JSON-RPC 2.0 over stdio.

Implements the Baselayer §9 layer contract:
  - compile_context(target_files): must return the same closure as
    manifest traversal (AGENTS.md §1).
  - read_section(node_id): must return exactly sha256-verified byte_range.

Tools additionally exposed for convenience:
  - search_nodes(query): substring match on summaries/ids.
  - list_nodes(offset, limit): paginated node inventory.

Run:  python3 .agent/tools/mcp/server.py
Read-only: never writes .context/manifest.json or wiki/.
Env: reads keys from workspace .agent/.env (never committed).
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import context  # noqa: E402

PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {"name": "baselayer-mcp", "version": "0.1.0"}

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
]


def _tool_result(payload):
    return {"content": [{"type": "text", "text": json.dumps(payload, indent=2, ensure_ascii=False)}]}


def handle(msg):
    method = msg.get("method")
    mid = msg.get("id")
    params = msg.get("params") or {}

    def ok(result):
        return {"jsonrpc": "2.0", "id": mid, "result": result}

    def err(code, message):
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
        return ok({})
    if method == "tools/list":
        return ok({"tools": TOOLS})
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        try:
            if name == "compile_context":
                return ok(_tool_result(context.compile_context(args.get("target_files", []))))
            if name == "read_section":
                chunk = context.read_section(args["node_id"])
                return ok(_tool_result({"node_id": args["node_id"], "text": chunk.decode("utf-8", "replace")}))
            if name == "search_nodes":
                return ok(_tool_result(context.search_nodes(args.get("query", ""), args.get("limit", 20))))
            if name == "list_nodes":
                return ok(_tool_result(context.list_nodes(args.get("limit", 50), args.get("offset", 0))))
            if name == "knowledge_search":
                return ok(_tool_result(context.knowledge_search(args.get("query", ""), args.get("limit", 10))))
            if name == "knowledge_last":
                return ok(_tool_result(context.knowledge_last(args.get("kind", "work"), args.get("limit", 5))))
        except Exception as exc:  # surface as tool error, keep server alive
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
    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue
        try:
            msg = json.loads(raw)
        except json.JSONDecodeError:
            continue
        resp = handle(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
