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
namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    protected function setUp(): void
    {
        parent::setUp();
        // Call $this->withoutExceptionHandling() only in tests that
        // test non-HTTP exceptions; it suppresses assertStatus() etc.
    }

    // Helper: Authenticate and return user
    protected function actingAsUser(): mixed
    {
        $user = \App\Models\User::factory()->create();
        $this->actingAs($user);
        return $user;
    }

    protected function actingAsAdmin(): mixed
    {
        $admin = \App\Models\User::factory()->admin()->create();
        $this->actingAs($admin);
        return $admin;
    }
}
```

```
