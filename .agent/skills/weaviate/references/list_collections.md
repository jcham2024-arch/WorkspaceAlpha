# List Collections

Scope: list_collections (weaviate).
Load when: you need the list_collections (weaviate) detail described in SKILL.md.

## Contents

- List Collections

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# List Collections

Show all available Weaviate collections with their properties.

## Usage

```bash
uv run scripts/list_collections.py [--json]
```

## Parameters

| Parameter | Flag | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--json` | — | No | `false` | Output in JSON format |

## Output

- **Default**: Markdown table with collection names, descriptions, and property lists
- **JSON**: Array of collection objects with full property details

## Examples

```bash
uv run scripts/list_collections.py
```

```bash
uv run scripts/list_collections.py --json
```

