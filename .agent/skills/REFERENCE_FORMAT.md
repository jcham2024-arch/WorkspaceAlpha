# Reference Format Standard (master library)

Canonical expanded guide: SKILL_AUTHORING.md in this folder —
Anthropic best practices (schemas, sizes, wording, process).
This file is the compact per-file checklist used by the rewrite
pass.

Every skill's SKILL.md body stays under 500 lines. Long material
lives in `references/` — one level deep, linked directly from the
body. Bodies are lean: workflow + checklists only. Detail goes in
references; headers name the section to load.

## Language standard

- One instruction per line; imperative mood.
- Cut: hedging (just, really, basically), pleasantries, narration,
  repeated paragraphs, banners/ASCII art.
- Keep: frontmatter, checklists, tables, commands, concrete examples.
- No filler openers ("in this section…"), no closers ("in summary…").

## Reference file standard

Every `references/*.md` follows this format:

```
# <Title>
Scope: <one line — what this reference covers>
Load when: <condition that triggers loading this file>

## Contents (one level)
- <section> — <one-line description>

## Checklist
- [ ] ...

## Commands
| Task | Command |
|---|---|
| ... | `...` |

## Notes
- <gotchas, edge cases>
```

Rules:
- Reference files linked one level deep (SKILL.md → references/*.md).
- TOC when the file exceeds 100 lines.
- No nested links beyond that (Anthropic best practice).

## Size budget

- Frontmatter (Layer 1, name + description): always loaded. < 60
  words per description.
- SKILL.md body (Layer 2, on trigger): < 500 lines.
- references/ (Layer 3, on demand): unbounded, but one level deep.

## Rewrite procedure (line by line)

For a skill over 500 lines:
1. Mark each line: keep (workflow/checklist), move (deep detail),
   delete (filler, duplicate, stale).
2. Keep-lines form the new SKILL.md body (< 500 lines). Do not
   renumber or reflow checklists — keep the author's checklist.
3. Move-lines become `references/<section>.md` in the format above;
   link them from the body by name.
4. Re-run the profile eval prompt for the skill; selection must
   not degrade (description is the load-bearing line).
