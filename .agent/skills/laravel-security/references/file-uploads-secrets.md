# File Uploads, Secrets & Dependencies

Scope: upload validation, secure storage (S3), secrets, composer.
Load when: handling file uploads, storing documents, auditing dependencies.

## Contents

- Upload rules (MIME whitelist, size, dimensions)
- Secure storage + signed URLs
- `composer audit`, pinning, `.env` secrets at boot

## Checklist

- [ ] `mimes` + `max` + dimensions on every upload
- [ ] Sensitive files on private disk, accessed via signed URLs
- [ ] `composer audit` in CI; lock file committed
- [ ] Secrets from env/secret manager, validated at boot

## Commands

| Task | Command |
|---|---|
| Audit dependencies | `composer audit` |
| Why a package is outdated | `composer why-not` |
| Pin majors | `"laravel/framework": "^11.0"` in composer.json |

## Code

```php
public function rules(): array
{
    return [
        'document' => ['required', 'file', 'mimes:pdf,doc,docx,xls,xlsx', 'max:10240', 'extensions:pdf,doc,docx,xls,xlsx'],
        'avatar' => ['nullable', 'image', 'mimes:jpg,jpeg,png,webp', 'max:2048'],
    ];
}

// s3 disk
$path = $request->file('document')->store('documents', 's3');

public function download(Document $document)
{
    $this->authorize('download', $document); // own-model resource, never request path
    $url = Storage::disk('s3')->temporaryUrl($document->path, now()->addMinutes(15));
    return redirect($url);
}

// config/filesystems.php — s3, server_side_encryption => 'AES256'

// .env — never commit; validate at boot
$secrets = ['services.stripe.key', 'services.stripe.webhook_secret'];
foreach ($secrets as $key) {
    if (empty(config($key))) Log::critical("Missing secret: {$key}");
}
```

## Notes

- Never use the `public` disk for sensitive documents.
