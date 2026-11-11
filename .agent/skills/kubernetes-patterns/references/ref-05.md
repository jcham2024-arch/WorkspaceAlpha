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
```yaml
# LoadBalancer — external traffic (cloud providers)
spec:
  type: LoadBalancer
  ports:
    - port: 443
      targetPort: 8080
```

```
