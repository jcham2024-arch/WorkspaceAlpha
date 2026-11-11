# Astro Edge Middleware Scope

Scope: astro-edge-middleware-scope (vercel-optimize).
Load when: you need the astro-edge-middleware-scope (vercel-optimize) detail described in SKILL.md.

## Contents

- Astro Edge Middleware Scope

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
id: astro-edge-middleware-scope
title: Astro edge middleware scope
status: active
candidateKinds: ["middleware_heavy"]
frameworks: ["astro@*"]
priority: 88
citations: ["https://vercel.com/docs/frameworks/frontend/astro", "https://docs.astro.build/en/guides/integrations-guide/vercel/"]
maxBriefChars: 800
---

## Investigation Brief
Astro middleware can run at the edge for broad request sets. If middleware volume is high, prove which paths actually need interception.

## Evidence To Check
Use middleware invocation share and top paths. Inspect adapter middleware mode, middleware source, auth/redirect logic, and whether static assets, prerendered pages, or public pages are being intercepted.

## Do Not Recommend When
Do not bypass required auth, locale, header, or routing logic. Do not move global middleware work into every page when the current scope is already minimal.

## Verification
Name the middleware share, dominant paths, current middleware mode, and exact source or config line to narrow.
