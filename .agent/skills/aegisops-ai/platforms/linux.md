# aegisops-ai — Linux

Scope: Linux variant of the `aegisops-ai` skill.
Load when: you are doing `aegisops-ai` on Linux.

## Context

bash/zsh default; systemd services; POSIX paths; distro package managers (apt/dnf/pacman).
Topic: Autonomous DevSecOps & FinOps Guardrails. Guide to reviewing Linux kernel patches, Terraform cost changes and Kubernetes policy with a separately reviewed upstream tool and configured model.

## Scripting

`#!/bin/sh` POSIX scripts, `set -euo pipefail` for bash; docker/podman for isolation. Pitfalls: distro drift, missing jq/python3, SELinux/AppArmor in hardened hosts.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
