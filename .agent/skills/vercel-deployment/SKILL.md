---
tier: "experimental"
last_reviewed: 2026-11-10
source_url: ""
source_ref: ""
source_commit: ""
content_hash: "11174799b23c52cb80edc998230b83fda87231b4ea1779614c015bcd70f55e32"
fetched_at: "2026-11-10"
upstream_license: "unknown"
owner: "taskmaster"
---
name: vercel-deployment
description: Expert knowledge for deploying to Vercel with Next.js
tier: "experimental"
risk: critical
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---


# Vercel Deployment

Expert knowledge for deploying to Vercel with Next.js

## Detailed Guide

Read [the detailed guide](references/detailed-guide.md) before executing this skill. It retains the complete procedure and reference material. Treat its safety, prerequisites, and validation requirements as mandatory. For focused work, load the relevant sections; for end-to-end work, read the guide completely.

## Prerequisites

- Verify the project's Next.js version and available local skills; historical upstream names such as `nextjs-app-router` may not be installed.

## When to Use
- User mentions or implies: vercel
- User mentions or implies: deploy
- User mentions or implies: deployment
- User mentions or implies: hosting
- User mentions or implies: production
- User mentions or implies: environment variables
- User mentions or implies: edge function
- User mentions or implies: serverless function

## Example

```text
Prepare a preview deployment for the approved Vercel project/team using staging data. Verify build/runtime settings, environment scopes and rollback; production promotion and DNS changes require explicit destination authorization. Report the actual deployment ID and smoke-check result.
```

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
