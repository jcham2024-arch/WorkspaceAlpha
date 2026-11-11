---
tier: experimental
last_reviewed: 2026-11-10
content_hash: e03989e24de50709df9aeb58fef79194fbf4c5b8a59224ad92a241d8e5fa19ad
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
date_added: 2026-02-27
description: Upscale and enhance image and video resolution using AI
name: fal-upscale
risk: critical
source: ""https://github.com/fal-ai-community/skills/blob/main/skills/claude.ai/fal-upscale/SKILL.md""
---
# Fal Upscale
## Overview
Upscale and enhance image and video resolution using AI
## When to Use This Skill
Use this skill when you need to work with upscale and enhance image and video resolution using ai.
## Procedure
Inspect the actual source image/video and resolve desired dimensions, scaling factor,
output format, preservation constraints and budget. Use an available integration's
verified input schema; no upscaler/runtime is bundled and the historical upstream
path is absent from the current source tree. Confirm upload authorization and avoid
exposing private media or inventing a supported model.
Submit only the requested operation; record job identity and actual status. Compare
returned dimensions, artifacts and subject/detail preservation against the source.
Keep the original unchanged and deliver the actual returned file. Increased pixel
count does not prove recovered real detail; generated enhancement can alter content.
If execution is unavailable, return the job specification with that limitation.
## Example
**User request:**
> Use @fal-upscale for this task: Upscale and enhance image and video resolution using AI.
## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.