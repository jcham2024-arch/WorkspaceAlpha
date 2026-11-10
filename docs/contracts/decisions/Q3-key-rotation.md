# Decision: Q3 — Key Storage & Rotation Strategy for MCP Secrets

## Context

The MCP server (`.agent/tools/mcp/server.py`) requires secrets for:
- GitHub token (API access)
- Potential future: LLM API keys, signing keys

Need a strategy for storage, access, and rotation that works on Android without desktop keychains.

## Threat Model

| Asset | Threat | Impact |
|-------|--------|--------|
| GitHub token | App compromise | Repo read/write, private data |
| LLM API keys | App compromise | Cost, rate limits |
| Signing keys | App compromise | Supply chain attack |

## Options Considered

| Option | Storage | Rotation | Android Support | Complexity |
|--------|---------|----------|-----------------|------------|
| A: `.agent/.env` (gitignored) | Plaintext file | Manual replace | Native | Low |
| B: Android Keystore | Hardware-backed | Key rotation API | Strong | Medium |
| C: Encrypted file + Keystore-wrapped DEK | Encrypted file | DEK rotation | Strong | High |
| D: External secret manager | Cloud | Automated | Requires network | High |

## Decision

**Option A (`.agent/.env` plaintext) for now, with migration path to Option C.**

**Rationale:**
- Current threat model: local device, single user, no network secret manager
- Android Keystore requires Java/Kotlin bridge — adds build complexity
- `.env` is gitignored, only accessible to app UID (10450)
- Shizuku/root access is separate UID — cannot read app-private files
- Migration to encrypted file + Keystore-wrapped DEK documented for v2

## Current Implementation

```
.agent/.env (gitignored, mode 600)
├── GITHUB_TOKEN=ghp_xxx
├── GITHUB_USER=username
└── # Future keys added here
```

**Access control:**
- Only app UID (10450) can read
- Shizuku shell runs as different UID — no access
- Root shell can read but requires explicit grant

## Rotation Procedure (Manual v1)

1. Human generates new token at provider (GitHub → Settings → Developer settings)
2. Human edits `.agent/.env` via app UI or file editor
3. Restart MCP server: `python3 .agent/tools/mcp/server.py`
4. Verify: `doctor --github` passes

## Migration Path (v2 — Planned)

```
.agent/secrets.enc (encrypted, mode 600)
.agent/.env.master (Keystore-wrapped DEK, mode 600)
```

- DEK (Data Encryption Key) generated in Android Keystore (hardware-backed if available)
- DEK encrypts `secrets.enc` (AES-256-GCM)
- Keystore stores DEK, never exports it
- Rotation: generate new DEK in Keystore, re-encrypt `secrets.enc`

## Validation

- `doctor --github` verifies token works
- File permissions: `stat .agent/.env` → mode 600, uid 10450
- No secrets in git: `git check-ignore .agent/.env` → ignored
- No secrets in logs: grep audit logs for token patterns → none

## Links

- Spec: `docs/specs/mcp-protocol-spec.md` (planned)
- Tracking: `open-questions.md` (Q3)
- Implementation: `.agent/tools/mcp/server.py`, `.agent/.env.example`

---

*Decision recorded 2026-11-09. Current: manual rotation via .env. v2 encryption planned for multi-user or networked scenarios.*
