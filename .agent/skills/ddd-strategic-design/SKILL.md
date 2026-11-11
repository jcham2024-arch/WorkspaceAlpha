---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 5fd9f7f722eb0d5e77e121af800b380fd5bb140bafbe2e6578f9ad93c5231780
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
date_added: 2026-02-27
description: Design DDD strategic artifacts including subdomains, bounded contexts, and ubiquitous language for complex business domains.
name: ddd-strategic-design
risk: safe
source: self
tags: "[ddd, strategic-design, bounded-context, ubiquitous-language]"
---
# DDD Strategic Design
## Use this skill when
- Defining core, supporting, and generic subdomains.
- Splitting a monolith or service landscape by domain boundaries.
- Aligning teams and ownership with bounded contexts.
- Building a shared ubiquitous language with domain experts.
## Do not use this skill when
- The domain model is stable and already well bounded.
- You need tactical code patterns only.
- The task is purely infrastructure or UI oriented.
## Instructions
1. Extract domain capabilities and classify subdomains.
2. Define bounded contexts around consistency and ownership.
3. Establish a ubiquitous language glossary and anti-terms.
4. Capture context boundaries in ADRs before implementation.
If detailed templates are needed, open `references/strategic-design-template.md`.
## Required artifacts
- Subdomain classification table
- Bounded context catalog
- Glossary with canonical terms
- Boundary decisions with rationale
## Examples
```text
Use @ddd-strategic-design to map our commerce domain into bounded contexts,
classify subdomains, and propose team ownership.
```
## Limitations
- This skill does not produce executable code.
- It cannot infer business truth without stakeholder input.
- It should be followed by tactical design before implementation.