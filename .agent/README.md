# .agent — Agent Runtime Layer

Holds agent-side resources, tools, and the MCP server that consume
the baselayer. Per Baselayer.md §9, each layer reads the baselayer's
output and never writes it; the baselayer never knows these exist.

## Layout

```
.agent/
├── README.md          ← this file (design)
├── .env               ← keys (gitignored; never commit)
├── .env.example       ← committed template
├── mcp/
│   ├── server.py      ← MCP server (stdlib JSON-RPC 2.0 over stdio)
│   ├── mcp.json       ← server config
│   └── README.md      ← tool contract
├── tools/
│   ├── context.py     ← compile_context / read_section core (shared)
│   └── README.md
└── resources/
    └── README.md      ← pointers to baselayer docs + skills
```

## Contract with the baselayer

- build.py emits .context/graph.json → manifest.json + wiki/index.html.
  .agent/* never writes those files.
- .agent reads .context/manifest.json and docs/ byte ranges.
- Keys live in .agent/.env (gitignored). Template: .agent/.env.example.
  Fill in EXA_API_KEY to enable Exa semantic search (exa-search skill);
  other provider keys go here as needed.

## MCP tools (server.py)

| Tool | Contract |
|---|---|
| compile_context | Same closure as AGENTS.md §1 traversal |
| read_section | Exactly sha256-verified byte_range bytes |

Run: python3 .agent/mcp/server.py
