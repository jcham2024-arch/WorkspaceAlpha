# Intel

Scope: intel (fedora-hyprland-installer).
Load when: you need the intel (fedora-hyprland-installer) detail described in SKILL.md.

## Contents

- Intel

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Intel Graphics Support

## Driver Architecture
Intel Integrated & Arc graphics utilize kernel drivers (`i915` or `xe`) and the Mesa Intel driver (`iris` / `ANV`).

## Verification
- Verify hardware acceleration: `vainfo`
- Check active driver: `lspci -nnk | grep -A 2 VGA`
