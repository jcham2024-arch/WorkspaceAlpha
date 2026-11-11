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
import os
import magic  # pip install python-magic
from django.core.exceptions import ValidationError

ALLOWED_MIMES = {
    'image/jpeg', 'image/png', 'image/gif', 'application/pdf',
}

MIME_TO_EXTENSIONS = {
    'image/jpeg': {'.jpg', '.jpeg'},
    'image/png': {'.png'},
    'image/gif': {'.gif'},
    'application/pdf': {'.pdf'},
}

def validate_file_type(value):
    """Validate file type using magic bytes and cross-check extension."""
    mime = magic.from_buffer(value.read(2048), mime=True)
    value.seek(0)

    if mime not in ALLOWED_MIMES:
        raise ValidationError('Unsupported file type.')

    ext = os.path.splitext(value.name)[1].lower()
    if ext not in MIME_TO_EXTENSIONS.get(mime, set()):
        raise ValidationError('File extension does not match file content.')

def validate_file_size(value):
    """Validate file size (max 5MB)."""
    if value.size > 5 * 1024 * 1024:
        raise ValidationError('File too large. Max size is 5MB.')

# models.py
class Document(models.Model):
    file = models.FileField(
        upload_to='documents/',
        validators=[validate_file_type, validate_file_size]
    )

```

```
