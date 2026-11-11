# Astro Output Mode And Isr

Scope: astro-output-mode-and-isr (vercel-optimize).
Load when: you need the astro-output-mode-and-isr (vercel-optimize) detail described in SKILL.md.

## Contents

- Astro Output Mode And Isr

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
id: astro-output-mode-and-isr
title: Astro output mode and ISR
status: active
candidateKinds: ["uncached_route", "rendering_candidate"]
frameworks: ["astro@*"]
priority: 90
citations: ["https://vercel.com/docs/frameworks/frontend/astro", "https://docs.astro.build/en/guides/on-demand-rendering/", "https://docs.astro.build/en/reference/configuration-reference/"]
maxBriefChars: 850
---

## Investigation Brief
Astro defaults to static output; `server` output makes pages render on demand unless route-level prerendering changes that. First decide whether the hot route truly needs SSR.

## Evidence To Check
Inspect `astro.config`, adapter options, `output`, route-level `prerender`, dynamic params, middleware, and whether the content is shared across visitors. Compare route cache result and request volume.

## Do Not Recommend When
Do not prerender or cache personalized, preview, cart, checkout, or auth-gated pages. Do not change output mode for the whole app when one route-level flag is enough.

## Verification
Name the Astro output mode, route-level prerender state, observed route signal, and exact config or page line.
