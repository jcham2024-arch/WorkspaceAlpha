---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 3bfd97d59968d49e18f29e92db75549ca1e0d857db1c27d7af5a24d0268ffac7
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
description: Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, or implementing payment/sensitive features. Provides comprehensive security checklist and patterns.
name: security-review
origin: ECC
---
# Security Review Skill
This skill ensures all code follows security best practices and identifies potential vulnerabilities.
## When to Activate
- Implementing authentication or authorization
- Handling user input or file uploads
- Creating new API endpoints
- Working with secrets or credentials
- Implementing payment features
- Storing or transmitting sensitive data
- Integrating third-party APIs
## Security Checklist
### 1. Secrets Management
#### FAIL: NEVER Do This
#### PASS: ALWAYS Do This
#### Verification Steps
- [ ] No hardcoded API keys, tokens, or passwords
- [ ] All secrets in environment variables
- [ ] `.env.local` in .gitignore
- [ ] No secrets in git history
- [ ] Production secrets in hosting platform (Vercel, Railway)
### 2. Input Validation
#### Always Validate User Input
#### File Upload Validation
#### Verification Steps
- [ ] All user inputs validated with schemas
- [ ] File uploads restricted (size, type, extension)
- [ ] No direct use of user input in queries
- [ ] Whitelist validation (not blacklist)
- [ ] Error messages don't leak sensitive info
### 3. SQL Injection Prevention
#### FAIL: NEVER Concatenate SQL
#### PASS: ALWAYS Use Parameterized Queries
<!-- Do not write a literal dollar-sign-N placeholder anywhere in this file.
     Invoking this skill with arguments substitutes it away, and the example
     above then renders as concatenated SQL -- the exact anti-pattern this
     section warns against. Use "?" and name the Postgres form in prose. -->
#### Verification Steps
- [ ] All database queries use parameterized queries
- [ ] No string concatenation in SQL
- [ ] ORM/query builder used correctly
- [ ] Supabase queries properly sanitized
### 4. Authentication & Authorization
#### JWT Token Handling
#### Authorization Checks
#### Row Level Security (Supabase)
#### Verification Steps
- [ ] Tokens stored in httpOnly cookies (not localStorage)
- [ ] Authorization checks before sensitive operations
- [ ] Row Level Security enabled in Supabase
- [ ] Role-based access control implemented
- [ ] Session management secure
### 5. XSS Prevention
#### Sanitize HTML
#### Content Security Policy
Start strict and loosen only with a documented removal plan. Do not default to
`'unsafe-inline'` or `'unsafe-eval'`; they neutralize much of CSP's protection
and should be treated as temporary compatibility debt.
#### Verification Steps
- [ ] User-provided HTML sanitized
- [ ] CSP headers configured
- [ ] No unvalidated dynamic content rendering
- [ ] React's built-in XSS protection used
### 6. CSRF Protection
#### CSRF Tokens
#### SameSite Cookies
#### Verification Steps
- [ ] CSRF tokens on state-changing operations
- [ ] SameSite=Strict on all cookies
- [ ] Double-submit cookie pattern implemented
### 7. Rate Limiting
#### API Rate Limiting
#### Expensive Operations
#### Verification Steps
- [ ] Rate limiting on all API endpoints
- [ ] Stricter limits on expensive operations
- [ ] IP-based rate limiting
- [ ] User-based rate limiting (authenticated)
### 8. Sensitive Data Exposure
#### Logging
#### Error Messages
#### Verification Steps
- [ ] No passwords, tokens, or secrets in logs
- [ ] Error messages generic for users
- [ ] Detailed errors only in server logs
- [ ] No stack traces exposed to users
### 9. Blockchain Security (Solana)
#### Wallet Verification
#### Transaction Verification
#### Verification Steps
- [ ] Wallet signatures verified
- [ ] Transaction details validated
- [ ] Balance checks before transactions
- [ ] No blind transaction signing
### 10. Dependency Security
#### Regular Updates
#### Lock Files
#### Verification Steps
- [ ] Dependencies up to date
- [ ] No known vulnerabilities (npm audit clean)
- [ ] Lock files committed
- [ ] Dependabot enabled on GitHub
- [ ] Regular security updates
## Security Testing
### Automated Security Tests
## Pre-Deployment Security Checklist
Before ANY production deployment:
- [ ] **Secrets**: No hardcoded secrets, all in env vars
- [ ] **Input Validation**: All user inputs validated
- [ ] **SQL Injection**: All queries parameterized
- [ ] **XSS**: User content sanitized
- [ ] **CSRF**: Protection enabled
- [ ] **Authentication**: Proper token handling
- [ ] **Authorization**: Role checks in place
- [ ] **Rate Limiting**: Enabled on all endpoints
- [ ] **HTTPS**: Enforced in production
- [ ] **Security Headers**: CSP, X-Frame-Options configured
- [ ] **Error Handling**: No sensitive data in errors
- [ ] **Logging**: No sensitive data logged
- [ ] **Dependencies**: Up to date, no vulnerabilities
- [ ] **Row Level Security**: Enabled in Supabase
- [ ] **CORS**: Properly configured
- [ ] **File Uploads**: Validated (size, type)
- [ ] **Wallet Signatures**: Verified (if blockchain)
## Resources
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Next.js Security](https://nextjs.org/docs/security)
- [Supabase Security](https://supabase.com/docs/guides/auth)
- [Web Security Academy](https://portswigger.net/web-security)
---
**Remember**: Security is not optional. One vulnerability can compromise the entire platform. When in doubt, err on the side of caution.