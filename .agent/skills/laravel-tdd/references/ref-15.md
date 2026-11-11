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
Event::fake();

$order->markAsShipped();

Event::assertDispatched(OrderShipped::class, function ($event) use ($order) {
    return $event->order->id === $order->id;
});
```

```
