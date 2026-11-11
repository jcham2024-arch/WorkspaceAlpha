# Production Configuration

Scope: essential production settings, env file security, HTTPS enforcement.
Load when: setting up or reviewing production config, .env handling, or HTTPS.

## Contents

- Essential settings (app.php/session.php snippets)
- Validating required env at boot
- Trusted proxies + ForceHttps middleware

## Checklist

- [ ] `APP_DEBUG=false`, `APP_KEY` set
- [ ] Session cookies `secure`, `http_only`, `same_site=lax`
- [ ] HTTPS enforced (URL::forceScheme + middleware)
- [ ] Trusted proxies narrowed to LB CIDRs — never `*`

## Commands

| Task | Command |
|---|---|
| Set app key | `php artisan key:generate` |
| Never commit | `.env` in `.gitignore`; keep `.env.example` with placeholders |

## Code

```php
// config/app.php
'env' => env('APP_ENV', 'production'),
'debug' => (bool) env('APP_DEBUG', false), // CRITICAL: Never true in production
'key' => env('APP_KEY'), // Must be set: php artisan key:generate

// config/session.php
'secure' => env('SESSION_SECURE_COOKIE', true),
'http_only' => true,
'same_site' => 'lax',

// Verify APP_KEY is set at boot (bootstrap/app.php or a provider)
if (empty(config('app.key'))) {
    throw new RuntimeException('APP_KEY is not set. Run: php artisan key:generate');
}
```

### Environment File Security

```php
$requiredKeys = ['app.key', 'database.connections.mysql.database', 'database.connections.mysql.username'];
foreach ($requiredKeys as $key) {
    if (empty(config($key))) {
        throw new RuntimeException("Missing required config key: {$key}");
    }
}
```

### HTTPS Enforcement

```php
if (app()->environment('production')) {
    URL::forceScheme('https');
    request()->server->set('HTTPS', 'on');
}

// trusted proxies (load balancers) — Use specific IP ranges; '*' trusts all, allowing X-Forwarded-* spoofing
'trusted_proxies' => ['10.0.0.0/8', '172.16.0.0/12'],

// app/Http/Middleware/ForceHttps.php
public function handle($request, Closure $next)
{
    if (!$request->secure() && app()->environment('production')) {
        return redirect()->secure($request->getRequestUri());
    }
    return $next($request);
}
```

## Notes

- `.gitignore` already includes `.env` by default; validate required keys at boot rather than failing silently.
