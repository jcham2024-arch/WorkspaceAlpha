# Env Vars & graduated controls

Scope: env-var effects, metrics logging, turning the gate off, glob semantics.
Load when: configuring/ tuning GateGuard, or wiring its controls.

## Contents

- Graduated controls table
- Decision metrics schema
- Turning the gate off completely
- Glob semantics for `GATEGUARD_EXEMPT_GLOBS`

## Checklist

- [ ] Gate off entirely uses `ECC_GATEGUARD=off` or `GATEGUARD_DISABLED=1`
- [ ] Narrowed controls never disable the destructive-Bash checks
- [ ] Metrics never contain paths, commands, or transcript text

## Commands

| Task | Command |
|---|---|
| Disable for session | `ECC_GATEGUARD=off` |
| Hook-level off | `ECC_DISABLED_HOOKS` with GateGuard hook ID |
| Metric summary | see [metrics](metrics.md) summarizer note below |

## Notes

- **Graduated controls** (narrow one behaviour; destructive checks keep running):

| Variable | Default | Effect |
|---|---|---|
| `GATEGUARD_BASH_ROUTINE_DISABLED` | unset (gate on) | Disables routine-Bash gate only |
| `GATEGUARD_EXEMPT_GLOBS` | unset (no exemptions) | Comma-separated globs skip first-touch fact-forcing |
| `GATEGUARD_FACT_FORCE_FULL_DENIALS` | `3` | Full fact block for first N denials, then condensed to one line |
| `GATEGUARD_FACT_FORCE_MAX_DENIALS` | unset (no cap) | Denial budget; once spent, new paths pass through (counted in `cap_allows`) |
| `GATEGUARD_BASH_EXTRA_DESTRUCTIVE` | unset | Extra destructive-command regex patterns |
| `GATEGUARD_STATE_DIR` | `~/.gateguard` | State location; failure to persist allows instead of looping |
| `GATEGUARD_METRICS` | unset (off) | One JSON line per decision to `metrics.jsonl` (see guide) |
| `GATEGUARD_EXTERNAL_CONTRACT_QUESTION` | unset (off) | Adds external-contract question after data-schema |

`GATEGUARD_BASH_ROUTINE_DISABLED`, `GATEGUARD_METRICS`, `GATEGUARD_EXTERNAL_CONTRACT_QUESTION` accept `1`/`true`/`on`/`enabled`/`enable`/`yes` (case-insensitive); anything else leaves them off.

- **Turning the gate off completely**: `ECC_GATEGUARD=off` (also `0`/`false`/`off`/`disabled`/`disable`) or `GATEGUARD_DISABLED=1` (recognises `1` only).
- **Glob semantics**: patterns match the entire project-relative target path (root from `CLAUDE_PROJECT_DIR`, cwd, then process dir). `/` separators, lowercase; `*` in-segment, `**` across, `?` one non-separator. `**/*.md` for all Markdown; `services/**` is root tree only. Malformed patterns are dropped.
