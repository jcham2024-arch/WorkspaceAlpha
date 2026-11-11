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
tar --exclude='.env*' --exclude='.git' -czf context.tar.gz .
curl -X POST https://cloudish.ai/api/v1/projects \
  -H "Authorization: Bearer $CLOUDISH_API_KEY" \
  -F "name=my-app" -F "port=8080" -F "context=@context.tar.gz"
# -> { "project": { "path": "your-alias/my-app", ... }, "build": { "id": 123, "status": "pending" } }
```

```
