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
# Build an inspected allowlisted staging directory outside the source tree first.
# Do not assume tar honors .dockerignore; exclude credential files, private data and symlinks.
tar -czf ../context.tar.gz -C ../approved-build-context .
curl -X POST https://cloudish.ai/api/v1/projects \
  -H "Authorization: Bearer $CLOUDISH_API_KEY" \
  -F "name=notes-api" -F "port=8000" -F "context=@../context.tar.gz" \
  -F "volumeEnabled=true" -F "volumeSizeGb=1" -F "volumeMountPath=/data"
```

```
