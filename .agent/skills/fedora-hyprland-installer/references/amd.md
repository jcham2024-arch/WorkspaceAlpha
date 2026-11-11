# Amd

Scope: amd (fedora-hyprland-installer).
Load when: you need the amd (fedora-hyprland-installer) detail described in SKILL.md.

## Contents

- Amd

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# AMD Radeon Support

## Driver Architecture
AMD GPUs use open-source kernel drivers (`amdgpu`) and the Mesa graphics stack included in Fedora by default.

## Verification
- Verify Mesa openGL driver: `glxinfo | grep "OpenGL vendor"`
- Verify RADV Vulkan driver: `vulkaninfo | grep driverName`

No proprietary driver installation is required for Hyprland on AMD GPUs.
