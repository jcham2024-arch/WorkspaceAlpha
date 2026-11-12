#!/usr/bin/env python3
"""Integration tests for the MCP server.

Tests compile_context, read_section (with SHA-256 verification),
search_nodes, list_nodes, and error handling paths.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SERVER_PY = ROOT / ".agent" / "tools" / "mcp" / "server.py"
MANIFEST_JSON = ROOT / ".context" / "manifest.json"


def rpc_call(method, params=None, msg_id=1):
    """Send a JSON-RPC request to the MCP server and return the parsed response."""
    payload = {"jsonrpc": "2.0", "id": msg_id, "method": method}
    if params is not None:
        payload["params"] = params
    proc = subprocess.run(
        [sys.executable, str(SERVER_PY)],
        input=json.dumps(payload) + "\n",
        capture_output=True, text=True, timeout=30,
    )
    # The server may log to stderr; find the JSON response line on stdout
    for line in proc.stdout.strip().splitlines():
        line = line.strip()
        if line.startswith("{"):
            return json.loads(line)
    raise AssertionError(f"No JSON response. stdout={proc.stdout!r} stderr={proc.stderr!r}")


def rpc_tool(tool_name, arguments, msg_id=1):
    """Call a tool via tools/call and return the result payload."""
    resp = rpc_call("tools/call", {"name": tool_name, "arguments": arguments}, msg_id)
    if "error" in resp:
        raise AssertionError(f"Tool error: {resp['error']}")
    content = resp["result"]["content"][0]["text"]
    return json.loads(content)


class TestMCPServer(unittest.TestCase):
    """Integration tests for the baselayer MCP server."""

    def setUp(self):
        self.manifest = json.loads(MANIFEST_JSON.read_text(encoding="utf-8"))
        self.nodes = {n["id"]: n for n in self.manifest["nodes"]}

    def test_ping_health_check(self):
        """ping returns healthy status."""
        resp = rpc_call("ping", msg_id=1)
        self.assertEqual(resp["jsonrpc"], "2.0")
        self.assertEqual(resp["id"], 1)
        self.assertEqual(resp["result"]["status"], "healthy")
        self.assertEqual(resp["result"]["server"]["name"], "baselayer-mcp")

    def test_tools_list(self):
        """tools/list returns all registered tools."""
        resp = rpc_call("tools/list", msg_id=2)
        tool_names = {t["name"] for t in resp["result"]["tools"]}
        expected = {"compile_context", "read_section", "search_nodes", "list_nodes",
                    "knowledge_search", "knowledge_last", "wiki.search", "wiki.read"}
        self.assertEqual(tool_names, expected)

    def test_read_section_returns_verified_bytes(self):
        """read_section returns sha256-verified byte range content."""
        # Pick a known node from the manifest
        node_id = list(self.nodes.keys())[0]
        node = self.nodes[node_id]
        result = rpc_tool("read_section", {"node_id": node_id})
        self.assertEqual(result["node_id"], node_id)
        # Read the expected bytes directly
        ref = node["content_ref"].split("#")[0]
        data = (ROOT / ref).read_bytes()
        s, e = node["byte_range"]
        expected_text = data[s:e].decode("utf-8", "replace")
        self.assertEqual(result["text"], expected_text)

    def test_read_section_unknown_node_raises(self):
        """read_section on unknown node returns an error."""
        resp = rpc_call("tools/call", {
            "name": "read_section",
            "arguments": {"node_id": "nonexistent::node"},
        }, msg_id=3)
        self.assertIn("error", resp)
        self.assertIn("unknown node", resp["error"]["message"])

    def test_compile_context_returns_closure(self):
        """compile_context returns node ids in requires closure."""
        # Use a file that exists in the manifest
        refs = set()
        for n in self.manifest["nodes"]:
            refs.add(n["content_ref"])
        # Pick the first ref
        first_ref = sorted(refs)[0]
        result = rpc_tool("compile_context", {"target_files": [first_ref]})
        self.assertIn(first_ref, result)
        self.assertIsInstance(result[first_ref], list)

    def test_search_nodes_returns_matches(self):
        """search_nodes returns substring matches on summaries/ids."""
        result = rpc_tool("search_nodes", {"query": "documentation", "limit": 5})
        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), 5)
        # Every result should have id and summary
        for item in result:
            self.assertIn("id", item)
            self.assertIn("summary", item)

    def test_list_nodes_is_paginated(self):
        """list_nodes returns paginated results."""
        result = rpc_tool("list_nodes", {"limit": 3, "offset": 0})
        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), 3)

    def test_unknown_tool_returns_error(self):
        """Calling an unknown tool returns an error."""
        resp = rpc_call("tools/call", {
            "name": "nonexistent_tool",
            "arguments": {},
        }, msg_id=4)
        self.assertIn("error", resp)

    def test_invalid_json_is_skipped(self):
        """Server does not crash on invalid JSON input."""
        proc = subprocess.run(
            [sys.executable, str(SERVER_PY)],
            input="not json\n",
            capture_output=True, text=True, timeout=30,
        )
        # Should not crash; may produce no stdout response
        self.assertEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
