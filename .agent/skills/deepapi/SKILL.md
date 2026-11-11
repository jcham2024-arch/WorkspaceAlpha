---
tier: "experimental"
last_reviewed: 2026-11-10
source_url: ""
source_ref: ""
source_commit: ""
content_hash: "5a19d56a26c843c8a8f4100f12f33146ed35817af93909292a0767d0fa35621f"
fetched_at: "2026-11-10"
upstream_license: "unknown"
owner: "taskmaster"
---
name: deepapi
description: "Use DeepAPI for supported scraping, research, and email workflows with explicit credentials and approval."
tier: "experimental"
category: research
risk: critical
source: community
source_repo: davidondrej/skills
source_type: community
date_added: "2026-07-07"
author: davidondrej
tags: [deepapi, scraping, email, api]
tools: [claude, codex]
license: "MIT"
license_source: "https://github.com/davidondrej/skills/blob/main/LICENSE"
version: b17ad5148ab7
---


# DeepAPI

## Detailed Guide

The bundled endpoint guide describes a versioned external service, not a local runtime. Validate the authorized service origin and current schema before attaching credentials or spending credits; setup must never request secrets in chat.

Read [the detailed guide](references/detailed-guide.md) before executing this skill. It retains the complete procedure and reference material. Treat its safety, prerequisites, and validation requirements as mandatory. For focused work, load the relevant sections; for end-to-end work, read the guide completely.

## When to Use

- Use when the task needs supported DeepAPI scraping, research, or email endpoints.
- Use when the user has provided or confirmed the required DeepAPI credentials and scope.

Use this skill when the user asks you to scrape public web data or draft/read/send email through DeepAPI.

## Limitations

- Adapted from `davidondrej/skills`; verify local paths, tools, credentials, and agent features before acting.
- For commands, remote access, scheduling, browser automation, or file-changing workflows, get explicit user approval and confirm the target environment first.
