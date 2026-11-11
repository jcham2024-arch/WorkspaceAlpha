# Middleware Proxy Edge Cost

Scope: middleware-proxy-edge-cost (vercel-optimize).
Load when: you need the middleware-proxy-edge-cost (vercel-optimize) detail described in SKILL.md.

## Contents

- Middleware Proxy Edge Cost

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
id: middleware-proxy-edge-cost
title: Middleware edge cost
status: active
candidateKinds: ["middleware_heavy"]
frameworks: ["next@>=12.0.0"]
priority: 90
citations: ["https://nextjs.org/docs/app/building-your-application/routing/middleware", "https://vercel.com/docs/routing-middleware"]
maxBriefChars: 850
---

## Investigation Brief
Middleware recommendations should reduce unnecessary interception, not remove required request handling.

## Evidence To Check
Use `topMiddlewarePaths` and the matcher config. Confirm which paths need auth, rewrites, headers, or locale handling. Check whether static assets, images, or routes with no middleware need are being matched.

## Do Not Recommend When
Do not narrow the matcher in a way that bypasses required auth or routing behavior. Do not move middleware work into every route if the current matcher is already scoped.

## Verification
State the current middleware share, the dominant matched paths, and the exact matcher line to change.
