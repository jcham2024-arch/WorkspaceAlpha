# gitops-workflow — Linux

Scope: Linux variant of the `gitops-workflow` skill.
Load when: you are doing `gitops-workflow` on Linux.

## Context

bash/zsh default; systemd services; POSIX paths; distro package managers (apt/dnf/pacman).
Topic: Complete guide to implementing GitOps workflows with ArgoCD and Flux for automated Kubernetes deployments.

## Scripting

`#!/bin/sh` POSIX scripts, `set -euo pipefail` for bash; docker/podman for isolation. Pitfalls: distro drift, missing jq/python3, SELinux/AppArmor in hardened hosts.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
