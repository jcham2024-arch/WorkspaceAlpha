# Adoption Checklist

Scope: adoption-checklist (markstream-migration).
Load when: you need the adoption-checklist (markstream-migration) detail described in SKILL.md.

## Contents

- Adoption Checklist

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Adoption Checklist

Search for `react-markdown`, `remarkPlugins`, `rehypePlugins`, `markdown-it`, `marked`, `rehypeRaw`, `skipHtml`, allow/deny lists, `urlTransform`, custom renderers, CSS, and tests.

- `direct`: plain renderer swap
- `renderer-custom`: custom components can become overrides
- `plugin-heavy`: transform chains need manual mapping
- `security-heavy`: HTML and URL policy need explicit review

Swap the package first, preserve CSS order, prefer scoped mappings, and adopt `nodes` only when another layer owns parsing or structural updates.
