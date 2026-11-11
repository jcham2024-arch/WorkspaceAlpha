# Filters

Scope: filters (obsidian-clipper-template-creator).
Load when: you need the filters (obsidian-clipper-template-creator) detail described in SKILL.md.

## Contents

- Filters

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Obsidian Web Clipper Filters

**Official Docs:** [help.obsidian.md/web-clipper/filters](https://help.obsidian.md/web-clipper/filters)

Use filters to format variables: `{{variable|filter}}`.

## Text Formatting
- `markdown`: Convert HTML to Markdown.
- `strip_tags`: Remove HTML tags.
- `trim`: Remove whitespace.
- `upper`: Convert to uppercase.
- `lower`: Convert to lowercase.
- `title`: Title Case.
- `capitalize`: Capitalize first letter.
- `camel`: CamelCase.
- `kebab`: kebab-case.
- `snake`: snake_case.
- `pascal`: PascalCase.
- `replace:"old":"new"`: Replace text.
- `safe_name`: Make safe for filenames.
- `blockquote`: Format as blockquote.
- `link`: Create markdown link.
- `wikilink`: Create [[wikilink]].
- `list`: Format array as list.
- `table`: Format array as table.
- `callout`: Format as callout block.

## Dates
- `date:"format"`: Format date (e.g., `YYYY-MM-DD`).
- `date_modify:"+1 day"`: Modify date.
- `duration`: Format duration.

## Numbers
- `calc`: Perform calculations.
- `length`: Get length of string/array.
- `round`: Round numbers.

## HTML Processing
- `remove_html`: Remove selected elements and their contents; use `strip_tags` to retain text.
- `remove_attr`: Remove attributes.
- `strip_attr`: Remove all attributes, optionally preserving a specified allowlist; `remove_attr` removes named attributes.

## Arrays and Objects
- `map`: Transform array items (e.g., `map:item => item.text`).
- `join:"separator"`: Join array items.
- `split:"separator"`: Split string into array.
- `first`: First item.
- `last`: Last item.
- `slice:start,end`: Slice array.
- `unique`: Unique items.
- `template:"format"`: Format items using a template string.
