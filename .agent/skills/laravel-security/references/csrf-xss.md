# CSRF & XSS

Scope: CSRF tokens, Blade escaping, JS data passing, security headers.
Load when: adding forms, echoing user input, or passing data to JS.

## Contents

- `@csrf` on every state-changing form
- `{{ }}` escaped default; `{!! !!}` only for trusted HTML
- `@js()` / `@json()` for JavaScript context
- Security-headers middleware

## Checklist

- [ ] `@csrf` on all state-changing forms
- [ ] Never echo unescaped user input
- [ ] JS data via `@js` vs `{!! !!}`
- [ ] Middleware sets CSP, X-Frame-Options, X-Content-Type-Options

## Commands

| Task | Command |
|---|---|
| CSRF token | `@csrf` |
| Pass data to JS safely | `@json($data)` / `@js($payload)` |

## Code

```blade
<form method="POST" action="{{ route('posts.store') }}">@csrf</form>
<form method="POST" action="{{ route('posts.update', $post) }}">
    @csrf @method('PUT')
</form>
```

```blade
{{ $userInput }}          {{-- escaped, default --}}
{!! $trustedHtml !!}       {{-- raw — only trusted HTML --}}
{{ $user->name ?? 'Anonymous' }}
<script>const d = @json($data);</script>
<script>const p = @js($payload);</script>
```

```php
// app/Http/Middleware/SecurityHeaders.php
final class SecurityHeaders
{
    public function handle(Request $request, Closure $next): Response
    {
        $response = $next($request);
        $response->headers->set('X-Content-Type-Options', 'nosniff');
        $response->headers->set('X-Frame-Options', 'DENY');
        $response->headers->set('X-XSS-Protection', '1; mode=block');
        $response->headers->set('Content-Security-Policy', [
            "default-src 'self';",
            "script-src 'self' 'unsafe-eval' 'unsafe-inline';",
            "style-src 'self' 'unsafe-inline';",
            "img-src 'self' data: https:;",
            "font-src 'self';",
            "connect-src 'self';",
            "frame-ancestors 'self';",
        ]);
        $response->headers->set('Permissions-Policy', [
            'geolocation=()', 'microphone=()', 'camera=()',
        ]);
        return $response;
    }
}
```

## Notes

- `@json($data)` is XSS-safe for JSON embedding; `{!! !!}` is XSS-prone by design.
