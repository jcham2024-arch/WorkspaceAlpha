---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 4efbe89f5cf06610e3e6ddd3061275fb90d3b6eb75c7d916023429e04cd3f7ec
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
date_added: 2026-02-27
description: Scientific research and analysis skills
name: claude-scientific-skills
risk: safe
source: ""https://github.com/K-Dense-AI/claude-scientific-skills""
---
# Claude Scientific Skills
## Overview
Scientific research and analysis skills
## When to Use This Skill
Use this skill when you need to work with scientific research and analysis skills.
## Instructions
This is a discovery guide to the upstream scientific library; its many scientific
packages and workflows are not bundled inside this entrypoint.
1. Identify the scientific question, discipline, input data, desired analysis,
   computational environment, and evidence needed to support the result.
2. Browse the source repository for the particular relevant skill; inspect its full
   instructions, supporting files, dependencies, data licenses and limitations.
3. Prefer an appropriate already-installed canonical AAS skill when available.
   Import or install upstream content only within the user's authorized scope;
   do not silently load the whole library or execute unreviewed scripts.
4. Record methods, package versions, data provenance, uncertainty and actual checks.
   Separate reproduced results from proposed analysis or vendor claims.
The upstream library now calls itself Scientific Agent Skills. The original source
URL is preserved for attribution and redirects to the same project.
## Example
**User request:**
> Use @claude-scientific-skills for this task: Scientific research and analysis skills.
## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.