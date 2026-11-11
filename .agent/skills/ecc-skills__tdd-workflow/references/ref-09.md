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
import { describe, it, expect, mock } from 'bun:test'
import { searchMarkets } from './search'

describe('searchMarkets', () => {
  it('returns an empty list for an empty query', async () => {
    expect(await searchMarkets('')).toEqual([])
  })

  it('sorts results by similarity score', async () => {
    const results = await searchMarkets('election')
    expect(results).toEqual([...results].sort((a, b) => b.score - a.score))
  })
})
```

```
