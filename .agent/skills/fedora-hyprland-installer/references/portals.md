# Portals

Scope: portals (fedora-hyprland-installer).
Load when: you need the portals (fedora-hyprland-installer) detail described in SKILL.md.

## Contents

- Portals

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# XDG Desktop Portals & PipeWire

## Portals Requirement
For screen sharing, file open dialogs, and screenshots under Hyprland:
- `xdg-desktop-portal`
- `xdg-desktop-portal-hyprland`
- `xdg-desktop-portal-gtk`

## Service Startup Order
```text
Hyprland starts
  └─ exec-once = dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP
      └─ systemctl --user restart xdg-desktop-portal
```

## Audio Architecture
PipeWire handles low-latency audio and video streams (screen sharing). WirePlumber manages session routing.
Status check: `wpctl status`
