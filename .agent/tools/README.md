# Tools — Baselayer Context Core

context.py implements compile_context(target_files) and
read_section(node_id) over .context/manifest.json (read-only).
Used by the MCP server (../mcp/server.py) and directly:

  python3 .agent/tools/context.py context docs/README.md
  python3 .agent/tools/context.py section <node_id>
  python3 .agent/tools/context.py search <query>
