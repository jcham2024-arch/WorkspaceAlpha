# Participants

Scope: participants (longbridge-market-data).
Load when: you need the participants (longbridge-market-data) detail described in SKILL.md.

## Contents

- Participants

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# participants

```
Market maker (participant) broker IDs and names

Use these IDs to interpret results from the `brokers` command.

Usage: longbridge participants [OPTIONS]

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
longbridge participants --format json

# See all options
longbridge participants --help
```
