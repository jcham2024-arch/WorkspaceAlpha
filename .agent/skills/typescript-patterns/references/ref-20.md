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
// user/model.ts — internal types
export interface UserAccount {
  id: string
  email: string
  role: UserRole
}

// user/index.ts — public surface
export { type UserAccount, type UserRole } from './model'
export { createUser, findUser, updateUser } from './service'
```

```
