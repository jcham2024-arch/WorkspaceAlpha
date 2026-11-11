# API Security

Scope: rate limiting, Sanctum vs Passport, CORS.
Load when: rate-limiting endpoints, choosing API auth, or configuring CORS.

## Contents

- RateLimiter::for('api'|'auth'|'uploads')
- Sanctum (default) vs Passport (OAuth2, third-party)
- CORS whitelist origins + credentials

## Checklist

- [ ] `throttle:api` on API group; `throttle:auth` on login
- [ ] Scoped tokens + abilities middleware
- [ ] CORS origins whitelisted — never `*` in production

## Commands

| Task | Command |
|---|---|
| 60/min api | `RateLimiter::for('api', fn($r) => Limit::perMinute(60)->by(...))` |
| 5/min auth | `Limit::perMinute(5)` with 429 JSON response |

## Code

```php
protected function configureRateLimiting(): void
{
    RateLimiter::for('api', fn (Request $request) =>
        Limit::perMinute(60)->by($request->user()?->id ?: $request->ip()));
    RateLimiter::for('auth', fn (Request $request) =>
        Limit::perMinute(5)->by($request->ip())->response(fn () =>
            response()->json(['message' => 'Too many login attempts. Try again in 1 minute.'], 429)));
    RateLimiter::for('uploads', fn (Request $request) =>
        Limit::perHour(10)->by($request->user()?->id ?? $request->ip())->response(fn () =>
            response()->json(['message' => 'Upload limit reached. Try again later.'], 429)));
}

Route::middleware(['auth:sanctum', 'throttle:api'])->group(fn () =>
    Route::apiResource('posts', PostController::class));
Route::post('/login', [AuthController::class, 'login'])->middleware('throttle:auth');
```

### Sanctum vs Passport

```php
// Sanctum (recommended for most apps — simple, first-party, SPA)
'expiration' => 60 * 24,
Route::middleware('auth:sanctum')->group(function () {
    Route::get('/posts', [PostController::class, 'index'])->middleware('abilities:posts:read');
    Route::post('/posts', [PostController::class, 'store'])->middleware('abilities:posts:write');
});

// Passport (OAuth2 — for third-party clients or complex auth flows)
Passport::tokensExpireIn(now()->addDays(15));
Passport::refreshTokensExpireIn(now()->addDays(30));
Passport::personalAccessTokensExpireIn(now()->addMonths(6));
```

### CORS

```php
return [
    'paths' => ['api/*', 'sanctum/csrf-cookie'],
    'allowed_methods' => ['*'],
    'allowed_origins' => explode(',', env('CORS_ALLOWED_ORIGINS', '')),
    'allowed_origins_patterns' => [],
    'allowed_headers' => ['*'],
    'exposed_headers' => ['X-Total-Count', 'X-Pagination-Page'],
    'max_age' => 0,
    'supports_credentials' => true,
];
```

## Notes

- Never allow all origins in production unless the API is truly public.
