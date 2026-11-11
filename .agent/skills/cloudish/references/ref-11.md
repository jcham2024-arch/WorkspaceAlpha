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
curl https://cloudish.ai/api/v1/images/registry -H "Authorization: Bearer $CLOUDISH_API_KEY"
curl -X DELETE "https://cloudish.ai/api/v1/images/registry/tags?repo=builds/123&tag=v1" \
  -H "Authorization: Bearer $CLOUDISH_API_KEY"
```

```
