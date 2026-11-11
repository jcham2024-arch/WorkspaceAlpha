---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 226aa606438e86367a26de5e4b1fadf5a4bcc85df8925875fd95c0217c5cfe42
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
date_added: 2026-03-06
description: Expert guidance for ffuf web fuzzing during penetration testing, including authenticated fuzzing with raw requests, auto-calibration, and result analysis
name: ffuf-web-fuzzing
risk: offensive
source: community
---
> **⚠️ AUTHORIZED USE ONLY**
> This skill is for educational purposes or authorized security assessments only.
> You must have explicit, written permission from the system owner before using this tool.
> Misuse of this tool is illegal and strictly prohibited.
> **Mandatory confirmation gate**
> Before running any command that probes, exploits, changes, persists on, extracts data from, or attempts credential access against a target:
> 1. Ask the user to state the exact target URL, IP, account, or resource.
> 2. Ask the user to confirm written authorization and the permitted scope.
> 3. Show the exact command(s) and explain their expected effect.
> 4. Wait for explicit confirmation in the current conversation.
>
> Without that confirmation, remain read-only and provide defensive guidance only. Prefer a sandbox, disposable VM, or controlled lab.
# FFUF (Fuzz Faster U Fool) Skill
## Detailed Guide
Read [the detailed guide](references/detailed-guide.md) before executing this skill. It retains the complete procedure and reference material. Treat its safety, prerequisites, and validation requirements as mandatory. For focused work, load the relevant sections; for end-to-end work, read the guide completely.
## When to Use
- You are fuzzing web targets with `ffuf` during authorized security testing or penetration testing.
- The task involves content discovery, subdomain enumeration, parameter fuzzing, or authenticated request fuzzing.
- You need guidance on wordlists, filtering, calibration, and interpreting ffuf results efficiently.
## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.