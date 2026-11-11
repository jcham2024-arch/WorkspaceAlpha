# Input Validation

Scope: FormRequest rules, custom rules, messages, sanitize-after-validate.
Load when: writing request validation, upload rules, or custom Rule classes.

## Contents

- FormRequest structure (authorize + rules + messages)
- Image/document upload whitelists
- Custom rules: StrongPassword, NotBlacklistedDomain

## Checklist

- [ ] Every input validated (never trust raw request data)
- [ ] File rules: `mimes` whitelist + `max` + dimension limits
- [ ] Messages overridden for user-facing fields

## Commands

| Task | Command |
|---|---|
| Sanitize after validate | `strip_tags` inside `validated()` for string fields |

## Code

```php
public function rules(): array
{
    return [
        'title' => ['required', 'string', 'max:255'],
        'content' => ['required', 'string', 'max:10000'],
        'image' => ['required', 'image', 'mimes:jpg,jpeg,png,gif,webp', 'max:2048'],
        'tags' => ['array'],
        'tags.*' => ['integer', 'exists:tags,id'],
    ];
}

public function validated($key = null, $default = null): mixed
{
    $validated = parent::validated();
    $validated['title'] = strip_tags($validated['title']);
    return $key ? ($validated[$key] ?? $default) : $validated;
}
```

### Custom Validation Rules

```php
class StrongPassword implements Rule
{
    public function passes($attribute, $value): bool
    {
        return preg_match('/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#^()_\-+=])[A-Za-z\d@$!%*?&#^()_\-+=]{12,}$/', $value);
    }
    public function message(): string
    {
        return 'The :attribute must be at least 12 characters with uppercase, lowercase, number, and symbol.';
    }
}

final class NotBlacklistedDomain implements Rule
{
    private array $blacklisted = ['mailinator.com', 'guerrillamail.com'];
    public function passes($attribute, $value): bool
    {
        $domain = substr(strrchr($value, '@'), 1);
        return !in_array(strtolower($domain), $this->blacklisted);
    }
    public function message(): string
    {
        return 'Email from disposable domains is not allowed.';
    }
}
```

## Notes

- Keep messages specific; generic "validation failed" tells the user nothing.
