# Tactical Checklist

Scope: tactical-checklist (ddd-tactical-patterns).
Load when: you need the tactical-checklist (ddd-tactical-patterns) detail described in SKILL.md.

## Contents

- Tactical Checklist

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Tactical Pattern Checklist

## Aggregate design

- One aggregate root per transaction boundary
- Invariants enforced inside aggregate methods
- Avoid cross-aggregate synchronous consistency rules

## Value objects

- Immutable by default
- Validation at construction
- Equality by value, not identity

## Repositories

- Persist and load aggregate roots only
- Expose domain-friendly query methods
- Avoid leaking ORM entities into domain layer

## Domain events

- Past-tense event names (for example, `OrderSubmitted`)
- Include minimal, stable event payloads
- Version event schema before breaking changes
