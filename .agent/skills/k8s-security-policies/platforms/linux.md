# k8s-security-policies — Linux

Scope: Linux variant of the `k8s-security-policies` skill.
Load when: you are doing `k8s-security-policies` on Linux.

## Context

bash/zsh default; systemd services; POSIX paths; distro package managers (apt/dnf/pacman).
Topic: Guide for NetworkPolicy, RBAC, and Pod Security Admission/Standards (PodSecurityPolicy was removed in Kubernetes1.25) in Kubernetes.

## Scripting

`#!/bin/sh` POSIX scripts, `set -euo pipefail` for bash; docker/podman for isolation. Pitfalls: distro drift, missing jq/python3, SELinux/AppArmor in hardened hosts.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
