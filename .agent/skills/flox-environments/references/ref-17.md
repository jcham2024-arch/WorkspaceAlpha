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
```toml
# BAD — manifest is committed to git
[vars]
API_KEY = "<set-at-runtime>"

# GOOD — reference external config or pass at runtime
# Use: API_KEY="<your-api-key>" flox activate
[vars]
API_KEY = "${API_KEY:-}"
```

```
