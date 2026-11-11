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
async function mapWithConcurrency<T, R>(
  items: readonly T[],
  limit: number,
  mapper: (item: T) => Promise<R>
): Promise<R[]> {
  if (!Number.isInteger(limit) || limit < 1) {
    throw new RangeError(`Expected concurrency limit to be a positive integer, got: ${limit}`)
  }
  const results: R[] = new Array(items.length)
  let nextIndex = 0

  const workers = Array.from({ length: Math.min(limit, items.length) }, async () => {
    while (true) {
      const index = nextIndex++
      if (index >= items.length) return
      // Required under noUncheckedIndexedAccess: the index is proven
      // in-bounds above, but the compiler still types this T | undefined.
      // Skip only genuine sparse-array holes, mirroring Array.prototype.map:
      // a present `undefined` element is a legitimate value and must still
      // reach the mapper.
      if (!Object.hasOwn(items, index)) continue
      // Presence is proven above, so the indexed access is in-bounds and
      // filled — never a hole and never the compiler's speculative undefined.
      results[index] = await mapper(items[index]!)
    }
  })

  // One worker rejecting rejects the whole pool: Promise.all propagates the
  // first rejection to the caller (fail-fast). That is rejection, not
  // cancellation — the other workers keep running and may settle more of
  // their remaining items after the pool has already rejected. Use
  // Promise.all only when leaving that in-flight work running is acceptable;
  // otherwise use allSettled or thread an AbortSignal through the mapper.
  await Promise.all(workers)
  return results
}
```

```
