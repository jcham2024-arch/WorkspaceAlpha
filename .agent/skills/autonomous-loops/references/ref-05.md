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
# Use the configured plugin root or standalone install (~/.claude or
# $CLAUDE_CONFIG_DIR). For a reviewed and explicitly authorized ECC checkout:
# export CLAUDE_PLUGIN_ROOT="/absolute/path/to/reviewed/ECC"
ECC_ROOT="${CLAUDE_PLUGIN_ROOT:-${CLAUDE_CONFIG_DIR:-$HOME/.claude}}"
[ -f "$ECC_ROOT/scripts/claw.js" ] || { echo "ECC scripts not found in the selected root (set CLAUDE_PLUGIN_ROOT to an authorized ECC checkout)" >&2; exit 1; }

# Start the default session
node "$ECC_ROOT/scripts/claw.js"

# Named session with skill context
CLAW_SESSION=my-project CLAW_SKILLS=tdd-workflow,security-review node "$ECC_ROOT/scripts/claw.js"
```

```
