# Market Status

Scope: market-status (longbridge-market-data).
Load when: you need the market-status (longbridge-market-data) detail described in SKILL.md.

## Contents

- Market Status

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# market-status

```
Market open/close status for each exchange

Example: longbridge market-status

Usage: longbridge market-status [OPTIONS]

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
longbridge market-status --format json

# See all options
longbridge market-status --help
```
