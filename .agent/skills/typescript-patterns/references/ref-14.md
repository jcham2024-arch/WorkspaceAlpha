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
type User = { id: string; email: string }

function isUser(value: unknown): value is User {
  if (typeof value !== 'object' || value === null) return false
  if (!('id' in value) || !('email' in value)) return false
  const { id, email } = value
  return (
    typeof id === 'string' && id.length > 0 &&
    typeof email === 'string' && email.includes('@')
  )
}

function assertUserId(userId: string): void {
  if (typeof userId !== 'string' || userId.length === 0 || /[^A-Za-z0-9_-]/.test(userId)) {
    throw new TypeError('Expected a user ID using letters, digits, "_" or "-"')
  }
}

async function loadUser(userId: string): Promise<User> {
  assertUserId(userId)
  const response = await fetch(`/users/${userId}`)
  if (!response.ok) {
    throw new Error(`Failed to load user ${userId}: ${response.status}`)
  }
  const data: unknown = await response.json()
  if (!isUser(data)) {
    throw new TypeError(`Invalid user payload for ${userId}`)
  }
  return data
}

export async function getUser(userId: string): Promise<User> {
  try {
    return await loadUser(userId)
  } catch (error: unknown) {
    if (error instanceof Error) {
      // known failure mode: retry or surface a friendly message
      throw new Error(`user lookup failed: ${error.message}`, { cause: error })
    }
    throw new TypeError('unknown error shape')
  }
}
```

```
