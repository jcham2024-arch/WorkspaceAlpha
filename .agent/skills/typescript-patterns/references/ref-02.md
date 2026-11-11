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
// If you have proven the index exists, lift the element into a local first.
const [first] = items
if (first === undefined) {
  throw new Error("expected at least one item")
}
```

```
