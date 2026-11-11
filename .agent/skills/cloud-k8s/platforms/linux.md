# cloud-k8s — Linux

Scope: Linux variant of the `cloud-k8s` skill.
Load when: you are doing `cloud-k8s` on Linux.

## Context

bash/zsh default; systemd services; POSIX paths; distro package managers (apt/dnf/pacman).
Topic: Authorized cloud, container, and Kubernetes security assessment: metadata SSRF, IAM misconfiguration, container escape paths, and cluster RBAC review.

## Scripting

`#!/bin/sh` POSIX scripts, `set -euo pipefail` for bash; docker/podman for isolation. Pitfalls: distro drift, missing jq/python3, SELinux/AppArmor in hardened hosts.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
