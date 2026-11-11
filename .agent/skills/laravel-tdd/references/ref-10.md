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
use Illuminate\Support\Facades\Http;

public function test_it_handles_successful_payment(): void
{
    Http::fake([
        'api.stripe.com/*' => Http::response(['id' => 'pi_123', 'status' => 'succeeded'], 200),
    ]);

    $result = (new PaymentService())->charge(2999);
    $this->assertTrue($result->success);
}

public function test_it_handles_gateway_failure(): void
{
    Http::fake([
        'api.stripe.com/*' => Http::response(['error' => 'card_declined'], 402),
    ]);

    $this->expectException(PaymentFailedException::class);
    (new PaymentService())->charge(2999);
}

public function test_it_retries_on_timeout(): void
{
    Http::fake([
        'api.stripe.com/*' => Http::sequence()
            ->pushStatus(408)
            ->pushStatus(200),
    ]);

    $this->assertTrue((new PaymentService())->charge(2999)->success);
}
```

```
