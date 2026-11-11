---
tier: "experimental"
last_reviewed: 2026-11-10
source_url: ""
source_ref: ""
source_commit: ""
content_hash: "1b25d490253b34745d91c21740675a0fa268940d006635ef8a6856695c746b0c"
fetched_at: "2026-11-10"
upstream_license: "unknown"
owner: "taskmaster"
---
name: ddd-context-mapping
description: "Map relationships between bounded contexts and define integration contracts using DDD context mapping patterns."
tier: "experimental"
risk: safe
source: self
tags: "[ddd, context-map, anti-corruption-layer, integration]"
date_added: "2026-02-27"
---


# DDD Context Mapping

## Use this skill when

- Defining integration patterns between bounded contexts.
- Preventing domain leakage across service boundaries.
- Planning anti-corruption layers during migration.
- Clarifying upstream and downstream ownership for contracts.

## Do not use this skill when

- You have a single-context system with no integrations.
- You only need internal class design.
- You are selecting cloud infrastructure tooling.

## Instructions

1. List all context pairs and dependency direction.
2. Choose relationship patterns per pair.
3. Define translation rules and ownership boundaries.
4. Add failure modes, fallback behavior, and versioning policy.

If detailed mapping structures are needed, open `references/context-map-patterns.md`.

## Output requirements

- Relationship map for all context pairs
- Contract ownership matrix
- Translation and anti-corruption decisions
- Known coupling risks and mitigation plan

## Examples

```text
Use @ddd-context-mapping to define how Checkout integrates with Billing,
Inventory, and Fraud contexts, including ACL and contract ownership.
```

## Limitations

- This skill does not replace API-level schema design.
- It does not guarantee organizational alignment by itself.
- It should be revisited when team ownership changes.
