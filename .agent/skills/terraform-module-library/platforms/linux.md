# terraform-module-library — Linux

Scope: Linux variant of the `terraform-module-library` skill.
Load when: you are doing `terraform-module-library` on Linux.

## Context

bash/zsh default; systemd services; POSIX paths; distro package managers (apt/dnf/pacman).
Topic: Production-ready Terraform module patterns for AWS, Azure, and GCP infrastructure.

## Scripting

`#!/bin/sh` POSIX scripts, `set -euo pipefail` for bash; docker/podman for isolation. Pitfalls: distro drift, missing jq/python3, SELinux/AppArmor in hardened hosts.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
