# External Api Critical Path

Scope: external-api-critical-path (vercel-optimize).
Load when: you need the external-api-critical-path (vercel-optimize) detail described in SKILL.md.

## Contents

- External Api Critical Path

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
id: external-api-critical-path
title: External API critical path
status: active
candidateKinds: ["external_api_slow"]
frameworks: ["next@>=13.0.0"]
priority: 90
citations: ["vercel-react-best-practices:async-parallel", "vercel-react-best-practices:server-parallel-fetching", "vercel-react-best-practices:server-cache-react"]
maxBriefChars: 850
---

## Investigation Brief
For external API candidates, identify the customer route that waits on the slow hostname and whether the call is on the critical path.

## Evidence To Check
Use callers-by-route evidence, transfer size, and source awaits. Check whether the upstream call can run in parallel, be cached safely, be reduced in payload size, or move after response.

## Do Not Recommend When
Do not cache mutations, secrets, per-user responses, or upstream calls whose freshness requirement is unknown.

## Verification
Name the hostname, caller route, p75 or p95 latency, and the exact source line that waits on the call.
