# Wayland

Scope: wayland (fedora-hyprland-installer).
Load when: you need the wayland (fedora-hyprland-installer) detail described in SKILL.md.

## Contents

- Wayland

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Wayland Session Environment

## Key Environment Variables
- `XDG_CURRENT_DESKTOP=Hyprland`
- `XDG_SESSION_TYPE=wayland`
- `XDG_SESSION_DESKTOP=Hyprland`
- `MOZ_ENABLE_WAYLAND=1` (Firefox Wayland native mode)
- `QT_QPA_PLATFORM=wayland;xcb` (Qt app compatibility)
- `GDK_BACKEND=wayland,x11` (GTK app compatibility)
