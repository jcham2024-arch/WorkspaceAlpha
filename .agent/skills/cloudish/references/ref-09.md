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
curl -X PUT https://cloudish.ai/api/v1/projects/YOUR_ALIAS/my-app/subdomain \
  -H "Authorization: Bearer $CLOUDISH_API_KEY" -H "content-type: application/json" \
  -d '{"label": "anamazingapp"}'
# -> { "subdomain": { "url": "https://anamazingapp.cloudish.app/", ... } }
```

```
