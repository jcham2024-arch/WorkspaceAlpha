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
# BAD — breaks on other machines
[vars]
PROJECT_DIR = "/home/alice/projects/myapp"

# GOOD — use Flox environment variables
[vars]
PROJECT_DIR = "$FLOX_ENV_PROJECT"
```

```
