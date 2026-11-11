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
function assertIsStringArray(value: unknown): asserts value is string[] {
  if (!Array.isArray(value)) {
    throw new TypeError('Expected an array of strings')
  }
  // Iteration visits sparse positions as undefined instead of skipping them.
  for (const item of value) {
    if (typeof item !== 'string') throw new TypeError('Expected an array of strings')
  }
}
```

```
