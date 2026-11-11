---
tier: "experimental"
last_reviewed: 2026-11-10
source_url: ""
source_ref: ""
source_commit: ""
content_hash: "fbb81116ee84e56d5eb087ba409cd078ad08b30230f06027de56fa0e3f670ec5"
fetched_at: "2026-11-10"
upstream_license: "unknown"
owner: "taskmaster"
---
name: email-systems
description: Design transactional and marketing email delivery, queues, templates, authentication, suppression and monitoring.
tier: "experimental"
risk: critical
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---


# Email Systems

Measure email return and deliverability for the actual audience and attribution
window; no universal ROI or inbox-delivery guarantee applies.

This skill covers transactional email that works, marketing automation that
converts, deliverability that reaches inboxes, and the infrastructure decisions
that scale.

## Detailed Guide

Read [the detailed guide](references/detailed-guide.md) before executing this skill. It retains the complete procedure and reference material. Treat its safety, prerequisites, and validation requirements as mandatory. For focused work, load the relevant sections; for end-to-end work, read the guide completely.

## When to Use
Use this skill when the request clearly matches the capabilities and patterns described above.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

## Example

For a password reset, enqueue a short-lived opaque reference, fetch the token
server-side without logging it, and deduplicate provider submission by event ID.
A timeout is an unknown send outcome: reconcile before resending; show the same
user-facing response whether or not the account exists.
