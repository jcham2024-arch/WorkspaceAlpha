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
```typescript
const results: PromiseSettledResult<number>[] = await Promise.allSettled(
  sourceIds.map((id) => fetchCount(id))
)

const total = results.reduce((sum, result) => {
  if (result.status === 'fulfilled') {
    return sum + result.value
  }
  log.warn('count fetch failed', result.reason)
  return sum
}, 0)
```

```
