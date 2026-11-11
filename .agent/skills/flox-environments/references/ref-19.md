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
# BAD — hook functions aren't available in the interactive shell
[hook]
on-activate = """
  deploy() { kubectl apply -f k8s/; }
"""

# GOOD — use [profile] for user-invokable functions
[profile]
common = """
  deploy() { kubectl apply -f k8s/; }
"""
```

```
