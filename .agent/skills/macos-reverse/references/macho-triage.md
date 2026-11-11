# Macho Triage

Scope: macho-triage (macos-reverse).
Load when: you need the macho-triage (macos-reverse) detail described in SKILL.md.

## Contents

- Macho Triage

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Mach-O 分诊

```bash
file ./app
otool -hv ./app
otool -l ./app | head
codesign -d --entitlements :- ./app
```

关注：`com.apple.security.*` entitlements、Library Validation、禁用库注入相关标志。