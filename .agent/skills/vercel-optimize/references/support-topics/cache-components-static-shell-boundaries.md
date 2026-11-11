# Cache Components Static Shell Boundaries

Scope: cache-components-static-shell-boundaries (vercel-optimize).
Load when: you need the cache-components-static-shell-boundaries (vercel-optimize) detail described in SKILL.md.

## Contents

- Cache Components Static Shell Boundaries

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
id: cache-components-static-shell-boundaries
title: Cache Components static shell boundaries
status: active
candidateKinds: ["rendering_candidate"]
frameworks: ["next@>=16.0.0"]
priority: 94
citations: ["https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents", "https://nextjs.org/docs/app/getting-started/caching", "https://nextjs.org/docs/app/guides/migrating-to-cache-components"]
maxBriefChars: 900
---

## Investigation Brief
On Next.js 16 with Cache Components, avoid older segment-config advice. The right question is whether the route can keep a static shell while dynamic data moves behind explicit cached or runtime boundaries.

## Evidence To Check
Check `cacheComponents`, `use cache`, `cacheLife`, request-time APIs, Suspense boundaries, and scanner evidence such as `force-dynamic` or `headers-in-page`.

## Do Not Recommend When
Do not suggest `dynamic`, `revalidate`, or `fetchCache` as the primary fix when Cache Components is enabled. Do not cache request-personalized content.

## Verification
Name the Next.js version, Cache Components state, dynamic trigger, and the exact boundary or directive that can change.
