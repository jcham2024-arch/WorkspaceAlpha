# Secret Handling and Key Rotation

This document covers how secrets are stored, rotated, and recovered in the WorkspaceAlpha workspace.

## Keys

| Key | Required | Where it lives | Purpose |
|-----|----------|----------------|---------|
| `EXA_API_KEY` | Yes | `.agent/.env` | Web search API key (exa-search skill) |

No other keys are currently defined. `.agent/.env.example` lists every required key with an empty value — copy it to `.env` and fill in actual values.

## Storage

- **`.agent/.env`** — Committed to `.gitignore`, never tracked in git. Contains actual secret values.
- **`.agent/.env.example`** — Committed template. Lists every required key with empty values. Safe to commit.

## Rotation Procedure

When a key needs rotation (compromise, expiration, scheduled refresh):

1. **Revoke** the old key with the provider (e.g., Exa dashboard for `EXA_API_KEY`)
2. **Issue** a new key from the provider
3. **Update** `.agent/.env` with the new value
4. **Restart** the harness / any long-running process using the key

No restart of the build pipeline or wiki renderer is required — keys are read at runtime by individual skills.

## Key Leak Response

If a real credential is accidentally committed to git:

1. **Revoke immediately** — assume the key is compromised
2. **Rotate** — issue a new key, update `.agent/.env`
3. **Purge history** — use `git filter-branch` or `bfg` to remove the key from all commits
4. **Verify** — `git log --all -p` should return no real credential values in tracked files

## Example `.env` (do not commit)

```
# .agent/.env — local only, never commit
EXA_API_KEY=your-actual-key-here
```

## Links

- Template: `.agent/.env.example`
- MCP server: `.agent/tools/mcp/server.py`
- Profile docs: `.agent/profiles/agent.md`
- Root docs: `README.md`

---

*This document is linked from `agent.md` and `README.md`. Update when new keys are added.*
