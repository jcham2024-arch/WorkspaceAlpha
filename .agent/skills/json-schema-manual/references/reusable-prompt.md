# Reusable Prompt

Scope: reusable-prompt (json-schema-manual).
Load when: you need the reusable-prompt (json-schema-manual) detail described in SKILL.md.

## Contents

- Reusable Prompt

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Reusable Prompt

```
I need a JSON Schema for [database], from the fields we already agreed.
Do not ask me for anything I have already told you.
Give me a draft 2020-12 object schema with one property per field, the same names and order
as the rest of the outputs, `required` only for the fields we confirmed as required, and
`enum` only for options we have actually settled. Tell me separately if strictness would
reject a valid payload. No examples unless I ask.
```
