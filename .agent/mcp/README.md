# MCP — Baselayer Tool Contract

Layer above the baselayer (Baselayer.md §9). Must return the same
closure as manifest traversal (AGENTS.md §1) and exactly
sha256-verified bytes.

Tools: compile_context(target_files), read_section(node_id),
search_nodes(query), list_nodes(offset, limit).

Transport: JSON-RPC 2.0 over stdio (stdlib only, no SDK dependency).
Config: mcp.json. Keys: .agent/.env (gitignored).
