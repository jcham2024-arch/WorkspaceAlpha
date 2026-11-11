# What Counts as Already Done

Scope: order of checks, sensitive / hard-linked targets, prior-search
credit, comment-only edits, sibling collapse, canonical path keys,
counters, compatibility.
Load when: a first-touch denial needs softening, or you are tuning
exemptions / thresholds.

## Contents

- Order of checks (9-step decision order)
- Sensitive targets (what never gets softened)
- Hard-linked targets
- Prior-search credit
- Comment/whitespace-only edits
- Same-turn sibling creation collapse
- Canonical path keys, in-session counters
- Compatibility and trust limits

## Checklist

- [ ] Exempts win over every later rule (operator exemptions are authoritative)
- [ ] Sensitive / hard-linked targets are always denied on first touch
- [ ] Credit, trivial and sibling allows never consume the denial cap
- [ ] Real location (symlinks resolved) is also judged for sensitivity

## Commands

| Fallback | Command |
|---|---|
| Disable the gate | `ECC_GATEGUARD=off` (session) |

## Notes

- **Order of checks** (first rule that applies wins):
  1. Exempt (`GATEGUARD_EXEMPT_GLOBS`, Claude settings) — allowed, wins over sensitive/hard-link rules.
  2. Subagent call — allowed, except sensitive or hard-linked (denied once per path).
  3. Already checked this session — allowed.
  4. Sensitive or hard-linked — skip straight to denial.
  5. Prior-search credit — allowed with a note.
  6. Comment or whitespace-only Edit — allowed with a note; file **not** marked checked.
  7. Sibling collapse — allowed with a note.
  8. Denial cap (`GATEGUARD_FACT_FORCE_MAX_DENIALS`) — passes through past budget.
  9. Deny (counted in `fact_force_denials`).
- **Sensitive targets** (judged on lowercased project-relative path AND real location):
  names `.env`, `.netrc`, `.pgpass`, `.env.*` prefixes, `.pem/.key/.p12/.pfx`, `id_rsa*` etc., `credentials`/`secrets.`; any exact segment `auth|authn|authz|security|secrets|payment(s)|billing|migrations`; `.github/workflows/`. Denial carries "Sensitive target: … do not apply."
- **Hard-linked targets** (`nlink > 1` or symlink to such): same treatment; denial says "Hard-linked target: …". A stat error other than missing counts as hard-linked.
- **Prior-search credit**: allowed with a note when a qualifying search in the current human turn already covered the file. Qualifying tools: Glob, Grep, LS, and Bash segments (`rg`, `grep`, `git grep`, `find`, `fd`, `ls`, `tree`, `Get-ChildItem`, `Select-String`, …). `Read` never counts. Needs a completed, unambiguous `tool_result` (not an error), not in the same batch, stem = basename-minus-extension ≥ 4 chars as a whole word (generic stems like `index`, `main`, `utils` never match). Exclusions never credit; lookups of the file itself never credit. Scope must contain the target. Note only — file marked checked, `fact_force_credited` incremented, denial count untouched.
- **Classification note**: denied ordinary touch that had an uncredited in-turn mention adds a "Closest search this turn did not count" line, sanitized to 60 chars.
- **Comment/whitespace-only edits**: allowed for code/test/prose non-sensitive targets; not marked checked; counted in `trivial_allows`. Comment tokens per language given (C family `//` `/* */`, Python/shell `#`, PowerShell `<# #>`, batch `REM`). Directives (shebangs, `# type:`, `// @ts-...`, `//go:build`, Rust doc comments, etc.) are code. Raw/multiline strings, `\` lines, JSX-like tags, heredocs never trivial. Checked against the current file (≤1 MiB); Go files importing `"C"` never pass.
- **Sibling collapse**: later first-touch Writes of new files of the same class in the same (real) directory allowed with note "Sibling of <first>…". Never config/instruction or dotfiles/8.3 names; only within the same human turn. Edits/MultiEdits never collapsed.
- **Canonical path keys**: relative paths resolve against tool `cwd` → `CLAUDE_PROJECT_DIR` → process dir; `a.py`, `./a.py`, absolute share one first-touch. Older raw-key state files are honoured.
- **In-session counters** (state file under `GATEGUARD_STATE_DIR`): `fact_force_credited`, `denials_by_class`, `credited_by_class`, `sibling_allows`, `dir_gates`, `cap_allows`, `trivial_allows`, `routine_readonly_passes`. Missing/malformed load as empty/zero.
- **Trust limit**: prior-search credit reads the local transcript, which the agent could in principle write to. Credit verifies observed behaviour, not intent.
