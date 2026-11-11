# Security Safety Notes

Scope: security-safety-notes (json-schema-manual).
Load when: you need the security-safety-notes (json-schema-manual) detail described in SKILL.md.

## Contents

- Security Safety Notes

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Security & Safety Notes

Never put a secret in a schema. Never embed password, token, API key, banking or health values as defaults or examples.
A requested schema may describe a sensitive field without containing its real value.

Never put real personal data in an `examples` block. Examples are obviously fake, and a
schema is published in places a spreadsheet is not.

If the user pastes a real payload to debug it, describe the failing rule instead of
echoing unnecessary personal data. Do not claim that deleting a message erases service storage.


See the [Common Pitfalls](common-pitfalls.md) reference for the full guidance.
