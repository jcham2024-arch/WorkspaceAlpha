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
# .flox/env/manifest.toml

[install]
# Packages to install — the core of the environment
ripgrep.pkg-path = "ripgrep"
jq.pkg-path = "jq"

[vars]
# Static environment variables
DATABASE_URL = "postgres://localhost:5432/myapp"

[hook]
# Non-interactive setup scripts (run every activation)
on-activate = """
  echo "Environment ready"
"""

[profile]
# Shell functions and aliases (available in interactive shell)
common = """
  alias dev="npm run dev"
"""

[options]
# Supported platforms
systems = ["x86_64-linux", "aarch64-linux", "x86_64-darwin", "aarch64-darwin"]
```

```
