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
curl -X POST https://cloudish.ai/api/v1/projects/YOUR_ALIAS/my-app/domains \
  -H "Authorization: Bearer $CLOUDISH_API_KEY" -H "content-type: application/json" \
  -d '{"host": "foobar.com"}'
# -> { "domain": { "host": "foobar.com", "status": "pending", "redirect": false,
#      "txtRecord": { "name": "_cloudish-challenge.foobar.com", "value": "cloudish-verify=..." } } }
```

```
