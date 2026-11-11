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
// Safe - parameterized query
const { data } = await supabase
  .from('users')
  .select('*')
  .eq('email', userEmail)

// Or with raw SQL -- the value goes in the params array, never in the
// string. Use your driver's placeholder syntax (Postgres numbers its
// placeholders, MySQL uses "?").
await db.query(
  'SELECT * FROM users WHERE email = ?',
  [userEmail]
)
```

```
