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
import { z } from 'zod'

const userInputSchema = z.object({
  email: z.string().email(),
  age: z.number().int().min(0).max(150)
})

export type UserInput = z.infer<typeof userInputSchema>

// validate once at the edge
const input: UserInput = userInputSchema.parse(rawBody)
```

```
