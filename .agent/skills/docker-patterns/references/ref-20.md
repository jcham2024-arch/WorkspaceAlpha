# Reference

Scope: moved detail from SKILL.md.
Load when: needed by the operation described in SKILL.md.

## Contents

- Reference

## Checklist

- [ ] (see SKILL.md)

## Commands

| Fallback | Command |
|---|---|
| see body | — |

## Notes

- Original code preserved verbatim from SKILL.md.

```
```bash
(
  set -e
  npm install --global @openai/codex@0.162.0   # the harness image does not ship codex
  node /ecc/docker/plugin-setup/codex-auth-relay.js &
  relay_pid=$!
  trap 'kill "$relay_pid" 2>/dev/null || true; wait "$relay_pid" 2>/dev/null || true' EXIT
  codex login
)
```

```
