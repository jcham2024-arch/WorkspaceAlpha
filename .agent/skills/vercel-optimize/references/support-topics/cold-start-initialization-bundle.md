# Cold Start Initialization Bundle

Scope: cold-start-initialization-bundle (vercel-optimize).
Load when: you need the cold-start-initialization-bundle (vercel-optimize) detail described in SKILL.md.

## Contents

- Cold Start Initialization Bundle

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
id: cold-start-initialization-bundle
title: Cold-start initialization and bundle weight
status: active
candidateKinds: ["cold_start"]
frameworks: ["*"]
priority: 92
citations: ["https://vercel.com/docs/functions/debug-slow-functions", "https://vercel.com/docs/functions/limitations", "https://vercel.com/docs/functions/runtimes"]
maxBriefChars: 850
---

## Investigation Brief
Cold-start candidates need a code-path check, not only a project-setting check. First prove whether cold requests are paying for imports, module-scope setup, runtime choice, or dependency weight.

## Evidence To Check
Use `startTypeSplit`, `coldVsWarmLatencyP95`, and `coldByDeployment`. In source, inspect module-scope SDK setup, database/client construction, top-level network calls, heavy dependencies, runtime exports, and deployment-local changes.

## Do Not Recommend When
Do not blame cold starts when warm requests are similarly slow. Do not recommend keep-warm traffic or more memory before proving initialization or runtime pressure.

## Verification
Name the cold-start share, cold-vs-warm gap, and exact initialization, dependency, or runtime line that explains it.
