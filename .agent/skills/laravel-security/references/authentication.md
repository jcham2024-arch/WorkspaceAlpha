# Authentication

Scope: Sanctum API tokens, password security, session management.
Load when: configuring API auth, password rules, or session handling.

## Contents

- Sanctum token issuance + abilities
- Hashing (bcrypt/Argon2id) + strong password rules
- Session regeneration on login, invalidation on logout

## Checklist

- [ ] Tokens carry abilities; routes check them
- [ ] Password rules: letters, mixed case, numbers, symbols, uncompromised
- [ ] Login attempts rate-limited
- [ ] `$request->session()->regenerate()` on login; invalidate + regenerate token on logout

## Commands

| Task | Command |
|---|---|
| Issue scoped token | `$user->createToken('api-token', ['read', 'write'])->plainTextToken` |

## Code

```php
// config/sanctum.php
'stateful' => explode(',', env('SANCTUM_STATEFUL_DOMAINS', sprintf(
    '%s%s',
    'localhost,localhost:3000,127.0.0.1,127.0.0.1:8000,::1',
    env('APP_URL') ? ',' . parse_url(env('APP_URL'), PHP_URL_HOST) : ''
)));
'expiration' => 60 * 24, // Token expiration in minutes (null = never)
'token_prefix' => env('SANCTUM_TOKEN_PREFIX', '');

// Route ability checks
Route::middleware('auth:sanctum')->group(function () {
    Route::get('/orders', function () {
        abort_unless(Auth::user()->tokenCan('read'), 403);
    })->middleware('abilities:read');
    Route::post('/orders', function () {
        abort_unless(Auth::user()->tokenCan('write'), 403);
    })->middleware('abilities:write');
});
```

### Password Security

```php
// config/hashing.php — default bcrypt; Argon2id is stronger
'bcrypt' => ['rounds' => env('BCRYPT_ROUNDS', 12)];

// RegisterRequest rules
'password' => [
    'required', 'confirmed',
    Password::min(12)  // trim to house policy
        ->letters()->mixedCase()->numbers()->symbols()->uncompromised(),
],

// AuthenticatedSessionController — notify on recent lockout
protected function authenticated(Request $request, $user)
{
    if ($user->wasRecentlyLockedOut()) {
        $user->notify(new SuspiciousLoginNotification($request->ip()));
    }
}
```

### Session Management

```php
// config/session.php
'driver' => env('SESSION_DRIVER', 'database'), // database/redis > file
'lifetime' => env('SESSION_LIFETIME', 120),
'expire_on_close' => env('SESSION_EXPIRE_ON_CLOSE', false),
'encrypt' => env('SESSION_ENCRYPT', false),

public function store(LoginRequest $request): RedirectResponse
{
    $request->authenticate();
    $request->session()->regenerate(); // CRITICAL: prevents session fixation
    return redirect()->intended(RouteServiceProvider::HOME);
}

public function destroy(Request $request): RedirectResponse
{
    Auth::guard('web')->logout();
    $request->session()->invalidate();
    $request->session()->regenerateToken();
    return redirect('/');
}
```

## Notes

- Use `ability` checks with `tokenCan`; unscoped tokens are weaker than scoped ones.
