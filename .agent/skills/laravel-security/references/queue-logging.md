# Queue & Logging Security

Scope: encrypted jobs, rate limits, retries; security audit channel.
Load when: securing queued work, or setting up audit logging.

## Contents

- `ShouldBeEncrypted` jobs + named rate limiters + retry policy
- Security log channel + SecurityLogger helper

## Checklist

- [ ] Sensitive job payloads encrypted (`ShouldBeEncrypted`)
- [ ] Rate limits + bounded retries on jobs
- [ ] Security events logged to dedicated channel with user/IP/UA

## Commands

| Task | Command |
|---|---|
| Log a security event | `SecurityLogger::log('event_name', [...])` |

## Code

```php
RateLimiter::for('payments', fn () => Limit::perMinute(5));

final class ProcessPaymentJob implements ShouldQueue, ShouldBeEncrypted
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;
    public function __construct(
        private readonly string $paymentIntentId,
        private readonly string $cardFingerprint,
    ) {}
    public function handle(): void {}
    public function retryUntil(): Carbon { return now()->addMinutes(5); }
    public function middleware(): array { return [new RateLimited('payments')]; }
}
```

```php
// config/logging.php
'channels' => ['security' => ['driver' => 'single',
    'path' => storage_path('logs/security.log'), 'level' => 'warning']],

final class SecurityLogger
{
    public static function log(string $event, array $context = []): void
    {
        Log::channel('security')->warning($event, array_merge([
            'user_id' => Auth::id(), 'ip' => request()->ip(),
            'user_agent' => request()->userAgent(), 'url' => request()->fullUrl(),
            'timestamp' => now()->toIso8601String(),
        ], $context));
    }
}

SecurityLogger::log('failed_login_attempt', ['email' => $email]);
SecurityLogger::log('role_change', ['target_user' => $targetId, 'new_role' => 'admin']);
SecurityLogger::log('suspicious_activity', ['reason' => 'multiple_attempts_from_different_ips']);
```

## Notes

- Encrypt only sensitive fields; public IDs are fine in the payload.
