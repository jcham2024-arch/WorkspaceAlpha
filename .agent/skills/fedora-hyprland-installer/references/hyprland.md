# Hyprland

Scope: hyprland (fedora-hyprland-installer).
Load when: you need the hyprland (fedora-hyprland-installer) detail described in SKILL.md.

## Contents

- Hyprland

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Hyprland Compositor & Configuration

## Overview
Hyprland is a dynamic tiling Wayland compositor that does not sacrifice appearance.

## Key Config Locations
- Main configuration: `~/.config/hypr/hyprland.conf`
- Additional split configs: `~/.config/hypr/monitors.conf`, `~/.config/hypr/keybinds.conf`

## Common Keybindings (Default Base)
- `SUPER + RETURN`: Open terminal
- `SUPER + SPACE`: Application launcher (`wofi` / `rofi`)
- `SUPER + Q`: Close focused window
- `SUPER + M`: Exit Hyprland session
- `SUPER + R`: Reload Hyprland config

## Monitor Syntax
```text
monitor=name,resolution@hz,position,scale
# Example auto monitor setup:
monitor=,preferred,auto,1
```
