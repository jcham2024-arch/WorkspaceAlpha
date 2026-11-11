# Eloquent Security

Scope: mass-assignment, SQL injection, casts, hidden attributes, model scopes.
Load when: writing Eloquent models, creating users from requests, raw queries.

## Contents

- `$fillable` whitelist; `$guarded = []` never
- Parameterized queries only; raw interpolation is vulnerable
- `$casts` (boolean, encrypted:array, hashed) and `$hidden`
- Soft deletes; optional lazy-loading prevention

## Checklist

- [ ] `$fillable` whitelisted; sensitive fields excluded
- [ ] `$hidden`: password, remember_token, 2fa secrets
- [ ] Never interpolate request input into raw SQL
- [ ] `$request->validated()` / `safe()->only()` — never `$request->all()`

## Commands

| Task | Command |
|---|---|
| Safe create | `User::create($request->validated())` |

## Code

```php
final class User extends Authenticatable
{
    protected $fillable = ['name', 'email', 'phone', 'avatar'];
    // NEVER add 'role', 'is_admin', 'is_verified' here

    protected $casts = [
        'email_verified_at' => 'datetime',
        'is_admin' => 'boolean',
        'settings' => 'array',
        'metadata' => 'encrypted:array', // Laravel 11+
        'password' => 'hashed',          // Laravel 10+
    ];

    protected $hidden = ['password', 'remember_token', 'two_factor_secret', 'two_factor_recovery_codes'];
    protected $appends = ['full_name']; // safe computed only
}

public function store(StoreUserRequest $request): RedirectResponse
{
    $user = User::create($request->safe()->only(['name', 'email', 'phone', 'avatar']));
}

// SQL injection — GOOD
User::where('email', $userInput)->first();
User::whereRaw('email = ?', [$userInput])->first();
DB::select('SELECT * FROM users WHERE email = ?', [$userInput]);

// BAD — never interpolate; never `$request->all()`
DB::select("SELECT * FROM users WHERE email = '{$userInput}'");
User::orderByRaw($userInput); // VULNERABLE
DB::statement("INSERT INTO users (email) VALUES ('{$userInput}')");

// Model patterns
final class Post extends Model
{
    use SoftDeletes;
    // AppServiceProvider::boot(): Model::preventLazyLoading(!app()->isProduction());
}
```

## Notes

- `$request->only()` is NOT safe without validation rules; `safe()` uses validated data only.
