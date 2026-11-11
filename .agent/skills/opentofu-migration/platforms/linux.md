# opentofu-migration — Linux

Scope: Linux variant of the `opentofu-migration` skill.
Load when: you are doing `opentofu-migration` on Linux.

## Context

bash/zsh default; systemd services; POSIX paths; distro package managers (apt/dnf/pacman).
Topic: Migrate from Terraform to OpenTofu with state compatibility, provider

## Scripting

`#!/bin/sh` POSIX scripts, `set -euo pipefail` for bash; docker/podman for isolation. Pitfalls: distro drift, missing jq/python3, SELinux/AppArmor in hardened hosts.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
