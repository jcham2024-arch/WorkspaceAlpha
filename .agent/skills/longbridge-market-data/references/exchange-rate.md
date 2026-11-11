# Exchange Rate

Scope: exchange-rate (longbridge-market-data).
Load when: you need the exchange-rate (longbridge-market-data) detail described in SKILL.md.

## Contents

- Exchange Rate

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# exchange-rate

```
Exchange rates for all supported currencies

Example: longbridge exchange-rate Example: longbridge exchange-rate --format json

Usage: longbridge exchange-rate [OPTIONS]

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
longbridge exchange-rate --format json

# See all options
longbridge exchange-rate --help
```
