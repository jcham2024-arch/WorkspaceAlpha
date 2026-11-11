# Nextjs Version Cache Semantics

Scope: nextjs-version-cache-semantics (vercel-optimize).
Load when: you need the nextjs-version-cache-semantics (vercel-optimize) detail described in SKILL.md.

## Contents

- Nextjs Version Cache Semantics

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
id: nextjs-version-cache-semantics
title: Next.js cache semantics by version
status: active
candidateKinds: ["uncached_route"]
frameworks: ["next@>=15.0.0"]
priority: 85
citations: ["https://nextjs.org/docs/app/api-reference/directives/use-cache", "https://nextjs.org/docs/app/api-reference/functions/cacheLife", "https://nextjs.org/docs/app/building-your-application/caching"]
maxBriefChars: 800
---

## Investigation Brief
On Next.js 15+, match the fix to the cache primitive already in use.

## Evidence To Check
Check `'use cache'`, `cacheLife`, `cacheTag`, `fetch` cache options, route handlers, and dynamic APIs.

## Do Not Recommend When
Do not suggest APIs outside the detected Next.js version. Do not claim `cacheLife()` emits CDN `Cache-Control` headers or that missing `cacheLife()` alone makes a `'use cache'` route run per request. Omitted `cacheLife()` calls use the default profile.

## Verification
Name the detected Next.js version and exact cache primitive or route header.
