---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 9bac4d477901357e314acd8beb4677ab3eec32bdb5f87b2c9890b11d6eecef4b
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
description: Laravel security best practices — authentication, authorization, Eloquent safety, CSRF, XSS prevention, API security, and secure deployment configurations. Use when reviewing Laravel auth, Eloquent safety, CSRF, XSS, API security, or deployment configuration.
name: laravel-security
origin: ECC
---
# Laravel Security Best Practices
Scope: secure Laravel apps — auth, authorization, Eloquent, CSRF,
XSS, API, uploads, secrets, queues, logging, deployment.
Load references by domain when you need that domain's code.
## When to Activate
- Setting up Laravel authentication and authorization (Sanctum,
  Passport, Jetstream, Breeze)
- Implementing user roles, permissions, and policies
- Configuring production security settings and environment variables
- Reviewing Laravel applications for security vulnerabilities
- Deploying Laravel applications to production
- Writing secure Eloquent queries and migrations
## Workflow
1. **Production config**: force `APP_DEBUG=false`, set `APP_KEY`,
   harden sessions, enforce HTTPS. See [production-config](references/production-config.md).
2. **Authentication**: Sanctum (API, scoped tokens) with bcrypt/Argon2id,
   strong password rules, rate-limited logins, session regeneration,
   logout invalidation. See [authentication](references/authentication.md).
3. **Authorization**: Gates for one-off rules, Policies for model
   rules, middleware for role areas. See [authorization](references/authorization.md).
4. **Eloquent**: whitelist `$fillable` (never `$guarded = []`),
   parameterized queries only, `$hidden` for sensitive attrs, `$casts`
   for types. See [eloquent-security](references/eloquent-security.md).
5. **CSRF/XSS**: `@csrf` everywhere; `@js`/`@json` for JavaScript
   context; never `{!! $userInput !!}`; security headers middleware.
   See [csrf-xss](references/csrf-xss.md).
6. **Input validation**: FormRequest rules with whitelists; custom
   rules for special cases. See [input-validation](references/input-validation.md).
7. **API**: rate limiters (api/auth/uploads), Sanctum vs Passport,
   CORS whitelist. See [api-security](references/api-security.md).
8. **Uploads, secrets, queues, logging**: MIME whitelists, signed
   URLs, `composer audit` in CI, encrypted jobs, security audit log.
   See [file-uploads-secrets](references/file-uploads-secrets.md)
   and [queue-logging](references/queue-logging.md).
9. **Checklist** (below) on every security review.
## Quick Security Checklist
| Check | Description |
|-------|-------------|
| `APP_DEBUG=false` | Never run with debug enabled in production |
| `APP_KEY` set | Always run `php artisan key:generate` |
| HTTPS enforced | Force HTTPS in production via middleware or proxy |
| `$fillable` whitelisted | Never use `$guarded = []` |
| CSRF active | `@csrf` on all state-changing forms |
| Sanctum/Passport configured | API authentication with token abilities/scopes |
| Rate limiting applied | Throttle API and auth endpoints |
| Input validation | FormRequest with specific rules, never `$request->all()` |
| File upload restrictions | Validate MIME types, size, dimensions |
| `composer audit` in CI | Check dependencies for known vulnerabilities |
| `password_hash` / `password_verify` | Use Laravel's built-in hashing (bcrypt/Argon2) |
| Session regeneration on login | Call `$request->session()->regenerate()` |
| Security headers middleware | CSP, X-Frame-Options, X-Content-Type-Options |
| Logged security events | Audit log for auth failures, role changes, suspicious activity |
| `.env` not committed | Verify `.gitignore` includes `.env` |
## References
- [production-config](references/production-config.md) — APP_DEBUG,
  keys, sessions, HTTPS
- [authentication](references/authentication.md) — Sanctum, passwords,
  sessions
- [authorization](references/authorization.md) — Gates, Policies,
  middleware
- [eloquent-security](references/eloquent-security.md) — mass
  assignment, SQL injection, casts, hidden attributes
- [csrf-xss](references/csrf-xss.md) — CSRF, Blade escaping, headers
- [input-validation](references/input-validation.md) — FormRequests,
  custom rules
- [api-security](references/api-security.md) — rate limiting,
  Sanctum/Passport, CORS
- [file-uploads-secrets](references/file-uploads-secrets.md) —
  uploads, S3, secrets, composer
- [queue-logging](references/queue-logging.md) — encrypted jobs,
  audit logging
## Related Skills
- `laravel-patterns` — Laravel architecture, routing, Eloquent, and API patterns
- `backend-patterns` — General backend API and database patterns
- `laravel-tdd` — Laravel testing with PHPUnit and Pest