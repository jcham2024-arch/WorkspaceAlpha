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
```dart
// BAD — crashes at runtime if null
final name = user!.name;

// GOOD — provide fallback
final name = user?.name ?? 'Unknown';

// GOOD — Dart 3 pattern matching (preferred for complex cases)
final display = switch (user) {
  User(:final name, :final email) => '$name <$email>',
  null => 'Guest',
};

// GOOD — guard early return
String getUserName(User? user) {
  if (user == null) return 'Unknown';
  return user.name; // promoted to non-null after check
}
```

```
