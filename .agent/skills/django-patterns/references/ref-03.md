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
```python
from django.db import models

class ProductQuerySet(models.QuerySet):
    """Custom QuerySet for Product model."""

    def active(self):
        """Return only active products."""
        return self.filter(is_active=True)

    def with_category(self):
        """Select related category to avoid N+1 queries."""
        return self.select_related('category')

    def with_tags(self):
        """Prefetch tags for many-to-many relationship."""
        return self.prefetch_related('tags')

    def in_stock(self):
        """Return products with stock > 0."""
        return self.filter(stock__gt=0)

    def search(self, query):
        """Search products by name or description."""
        return self.filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query)
        )

class Product(models.Model):
    # ... fields ...

    objects = ProductQuerySet.as_manager()  # Use custom QuerySet

# Usage
Product.objects.active().with_category().in_stock()
```

```
