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
curl https://cloudish.ai/api/v1/docker/YOUR_ALIAS/my-app/logs -H "Authorization: Bearer $CLOUDISH_API_KEY"
# -> { "logs": "--- container logs ---\n...\n--- events ---\n..." }
```

```
