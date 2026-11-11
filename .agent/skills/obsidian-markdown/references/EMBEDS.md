# Embeds

Scope: EMBEDS (obsidian-markdown).
Load when: you need the EMBEDS (obsidian-markdown) detail described in SKILL.md.

## Contents

- Embeds

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Embeds Reference

## Embed Notes

```markdown
![[Note Name]]
![[Note Name#Heading]]
![[Note Name#^block-id]]
```

## Embed Images

```markdown
![[image.png]]
![[image.png|640x480]]    Width x Height
![[image.png|300]]        Width only (maintains aspect ratio)
```

## External Images

```markdown
![Alt text](https://example.com/image.png)
![Alt text|300](https://example.com/image.png)
```

## Embed Audio

```markdown
![[audio.mp3]]
![[audio.ogg]]
```

## Embed PDF

```markdown
![[document.pdf]]
![[document.pdf#page=3]]
![[document.pdf#height=400]]
```

## Embed Lists

```markdown
![[Note#^list-id]]
```

Where the list has a block ID:

```markdown
- Item 1
- Item 2
- Item 3

^list-id
```

## Embed Search Results

````markdown
```query
tag:#project status:done
```
````
