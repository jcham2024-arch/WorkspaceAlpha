# senior-devops — Linux

Scope: Linux variant of the `senior-devops` skill.
Load when: you are doing `senior-devops` on Linux.

## Context

bash/zsh default; systemd services; POSIX paths; distro package managers (apt/dnf/pacman).
Topic: Set up CI/CD pipelines, infrastructure as code, containers and deployments on AWS, GCP or Azure. Use whenever the user needs a build or deploy pipeline, Terraform, a Dockerfile, or wants to manage a release to the cloud.

## Scripting

`#!/bin/sh` POSIX scripts, `set -euo pipefail` for bash; docker/podman for isolation. Pitfalls: distro drift, missing jq/python3, SELinux/AppArmor in hardened hosts.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
