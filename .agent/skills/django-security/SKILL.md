---
name: django-security
description: Django security best practices, authentication, authorization, CSRF protection, SQL injection prevention, XSS prevention, and secure deployment configurations. Use when reviewing Django authentication, authorization, input handling, or deployment settings.
metadata:
  origin: ECC
---

# Django Security Best Practices

Comprehensive security guidelines for Django applications to protect against common vulnerabilities.

## When to Activate

- Setting up Django authentication and authorization
- Implementing user permissions and roles
- Configuring production security settings
- Reviewing Django application for security issues
- Deploying Django applications to production

## Core Security Settings

### Production Settings Configuration


## Authentication

### Custom User Model


### Password Hashing


### Session Management


## Authorization

### Permissions


### Custom Permissions


### Role-Based Access Control (RBAC)


## SQL Injection Prevention

### Django ORM Protection


### Extra Security with raw()


## XSS Prevention

### Template Escaping


### Safe String Handling


### HTTP Headers


## CSRF Protection

### Default CSRF Protection


### Exempting Views (Use Carefully)


## File Upload Security

### File Validation


For environments where installing libmagic is difficult (e.g., minimal containers),
use the pure-Python `filetype` package as an alternative:


### Secure File Storage


## API Security

### Rate Limiting


### Authentication for APIs


## Security Headers

### Content Security Policy


## Environment Variables

### Managing Secrets


## Logging Security Events


## Quick Security Checklist

| Check | Description |
|-------|-------------|
| `DEBUG = False` | Never run with DEBUG in production |
| HTTPS only | Force SSL, secure cookies |
| Strong secrets | Use environment variables for SECRET_KEY |
| Password validation | Enable all password validators |
| CSRF protection | Enabled by default, don't disable |
| XSS prevention | Django auto-escapes, don't use `&#124;safe` with user input |
| SQL injection | Use ORM, never concatenate strings in queries |
| File uploads | Validate file type and size |
| Rate limiting | Throttle API endpoints |
| Security headers | CSP, X-Frame-Options, HSTS |
| Logging | Log security events |
| Updates | Keep Django and dependencies updated |

Remember: Security is a process, not a product. Regularly review and update your security practices.
