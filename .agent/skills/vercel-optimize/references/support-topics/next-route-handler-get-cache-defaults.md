# Next Route Handler Get Cache Defaults

Scope: next-route-handler-get-cache-defaults (vercel-optimize).
Load when: you need the next-route-handler-get-cache-defaults (vercel-optimize) detail described in SKILL.md.

## Contents

- Next Route Handler Get Cache Defaults

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
---
id: next-route-handler-get-cache-defaults
title: Next.js Route Handler GET cache defaults
status: active
candidateKinds: ["uncached_route", "cache_header_gap"]
frameworks: ["next@>=15.0.0"]
priority: 91
citations: ["https://nextjs.org/docs/app/api-reference/file-conventions/route", "https://vercel.com/docs/caching/cdn-cache"]
maxBriefChars: 850
---

## Investigation Brief
On Next.js 15+, GET Route Handlers are dynamic by default. For hot public GET handlers, verify whether uncached behavior is intentional before recommending cache headers or route config.

## Evidence To Check
Use method share, cache result, and source. Check `GET`, `revalidate`, `dynamic`, request headers, cookies, auth, query params, and response `Cache-Control`.

## Do Not Recommend When
Do not cache POST-style handlers, webhooks, per-user APIs, streaming responses, search requests with user-specific params, or handlers that read auth/cookies.

## Verification
Name the Next.js version, GET share, cache result mix, and the exact handler or header line that makes public caching safe.
