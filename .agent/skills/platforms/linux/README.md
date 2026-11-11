# Platform Variant — Linux

For skills that diverge on Linux. Context + scripting notes.

## Pattern

Variant lives either inline (`os: linux` + body OS section) or as
`platforms/linux.md` inside the skill folder.

## Context

- bash/zsh default; systemd services; distro package managers
  (apt / dnf / pacman); POSIX paths and permissions.

## Scripting

- Shell: `#!/bin/sh` (POSIX) for portability, `bash` only when
  bashisms are intended; always `set -euo pipefail`.
- Containers: docker/podman for reproducible environments.
- Pitfalls: distro drift (apt vs dnf), missing `jq`/`python3`,
  SELinux/AppArmor profiles in hardened environments.

## Top matching skills

- `docker-patterns`, `kubernetes-patterns`, bash/installer skills
  in the master (filter CATEGORIZATION.csv by os=linux).

Routing: provision by `os=linux` within coding/research roles.
