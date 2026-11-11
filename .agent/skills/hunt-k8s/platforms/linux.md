# hunt-k8s — Linux

Scope: Linux variant of the `hunt-k8s` skill.
Load when: you are doing `hunt-k8s` on Linux.

## Context

bash/zsh default; systemd services; POSIX paths; distro package managers (apt/dnf/pacman).
Topic: Hunt Kubernetes & Docker

## Scripting

`#!/bin/sh` POSIX scripts, `set -euo pipefail` for bash; docker/podman for isolation. Pitfalls: distro drift, missing jq/python3, SELinux/AppArmor in hardened hosts.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
