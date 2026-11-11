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
# Agent discovers it needs a tool (e.g., jq for JSON processing)
flox search jq                    # Verify the package exists
flox install jq                   # Install into project environment

# Or for more control, edit the manifest directly
tmp_manifest="$(mktemp)"
flox list -c > "$tmp_manifest"
# Add the package to [install] section, then apply
flox edit -f "$tmp_manifest"

# Run a command with the tool available
flox activate -- jq '.results[]' data.json
```

```
