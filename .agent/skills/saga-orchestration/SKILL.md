---
tier: "experimental"
last_reviewed: 2026-11-10
source_url: ""
source_ref: ""
source_commit: ""
content_hash: "7710530a113517e5eafeebe3c4e655f5645412dd64c8fa9b9399550e77651d1d"
fetched_at: "2026-11-10"
upstream_license: "unknown"
owner: "taskmaster"
---
name: saga-orchestration
description: "Patterns for managing distributed transactions and long-running business processes."
tier: "experimental"
risk: critical
source: community
date_added: "2026-02-27"
---


# Saga Orchestration

Patterns for managing distributed transactions and long-running business processes.

## Detailed Guide

Read [the detailed guide](references/detailed-guide.md) before executing this skill. It retains the complete procedure and reference material. Treat its safety, prerequisites, and validation requirements as mandatory. For focused work, load the relevant sections; for end-to-end work, read the guide completely.

## Do not use this skill when

- The task is unrelated to saga orchestration
- You need a different domain or tool outside this scope

## Use this skill when

- Coordinating multi-service transactions
- Implementing compensating transactions
- Managing long-running business workflows
- Handling failures in distributed systems
- Building order fulfillment processes
- Implementing approval workflows

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

## Example

After inventory reservation succeeds, a payment timeout is an unknown outcome.
Query the provider using the original idempotency key before charging again or
releasing inventory; record the resolution and retry compensation durably.
