# Get Collection

Scope: get_collection (weaviate).
Load when: you need the get_collection (weaviate) detail described in SKILL.md.

## Contents

- Get Collection

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Get Collection Details

Get detailed configuration of a specific collection including vectorizer, properties, replication, and multi-tenancy settings.

## Usage

```bash
uv run scripts/get_collection.py --name "CollectionName" [--json]
```

## Parameters

| Parameter | Flag | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--name` | `-n` | Yes | — | Collection name |
| `--json` | — | No | `false` | Output in JSON format |

## Output

- **Default**: Markdown-formatted collection details with property table
- **JSON**: Full collection configuration object

## Examples

```bash
uv run scripts/get_collection.py --name "Articles"
```

```bash
uv run scripts/get_collection.py --name "Products" --json
```

