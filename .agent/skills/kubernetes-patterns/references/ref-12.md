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
# WRONG: No requests or limits — unpredictable scheduling, OOM evictions
containers:
  - name: app
    image: myapp:latest
    # Missing resources: {} — this is dangerous in production

# WRONG: Limits without requests — requests default to limits, over-reserves capacity
resources:
  limits:
    cpu: "2"
    memory: "1Gi"
  # requests missing — will default to limits values
```

```
