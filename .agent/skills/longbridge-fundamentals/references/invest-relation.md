# Invest Relation

Scope: invest-relation (longbridge-fundamentals).
Load when: you need the invest-relation (longbridge-fundamentals) detail described in SKILL.md.

## Contents

- Invest Relation

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# invest-relation

```
Investment relations (subsidiary/parent companies)

Example: longbridge invest-relation 700.HK

Usage: longbridge invest-relation [OPTIONS] <SYMBOL>

Arguments:
  <SYMBOL>
          Symbol in <CODE>.<MARKET> format

Options:
      --format <FORMAT>
          Output format: 'pretty' for human-readable, 'json' for AI agents and scripting

          [default: pretty]
          [possible values: table, json]

  -v, --verbose
          Print verbose request info (host, elapsed) to stderr, prefixed with `*` like curl -v

      --lang <LANG>
          Language for content fetched from longbridge.com: zh-CN or en. Defaults to system LANG env var, then en

  -h, --help
          Print help (see a summary with '-h')
```

## Usage

```bash
# Run with JSON output for AI agents
longbridge invest-relation 700.HK --format json

# See all options
longbridge invest-relation --help
```
