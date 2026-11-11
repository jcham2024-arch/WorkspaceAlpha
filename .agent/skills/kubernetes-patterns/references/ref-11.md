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
resources:
  requests:       # Scheduler uses this to place the pod
    cpu: "100m"   # 100 millicores = 0.1 CPU
    memory: "128Mi"
  limits:         # Container is killed/throttled above this
    cpu: "500m"
    memory: "256Mi"
```

```
