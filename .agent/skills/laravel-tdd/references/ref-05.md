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
```php
$user = User::factory()->create();
$admin = User::factory()->admin()->create();
$product = Product::factory()->create(['user_id' => $user->id]);
$products = Product::factory()->count(10)->create();
$draft = Product::factory()->make(); // Not persisted

// With relationships
$user = User::factory()->has(Product::factory()->count(3))->create();

// Sequences
User::factory()->count(3)->sequence(
    ['role' => 'admin'], ['role' => 'editor'], ['role' => 'user'],
)->create();
```

```
