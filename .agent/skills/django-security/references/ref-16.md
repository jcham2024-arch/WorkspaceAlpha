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
from django.core.exceptions import ValidationError

import filetype  # pip install filetype

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
    """Validate file type using magic bytes."""
    kind = filetype.guess(value.read(2048))
    value.seek(0)

    if kind is None or kind.mime not in ALLOWED_MIMES:
        raise ValidationError('Unsupported file type.')

    ext = os.path.splitext(value.name)[1].lower()
    if ext not in MIME_TO_EXTENSIONS.get(kind.mime, set()):
        raise ValidationError('File extension does not match file content.')
```

```
