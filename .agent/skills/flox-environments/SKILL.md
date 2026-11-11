---
tier: experimental
last_reviewed: 2026-11-10
content_hash: fff98bd7c091929eefbdf8e633b12c4d5e0738edfc4d2a5b3e111953f1249395
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
description: Create reproducible, cross-platform (macOS/Linux) development environments with Flox, a declarative Nix-based environment manager. Use when setting up project toolchains, installing system-level dependencies (compilers, databases, native libs), pinning exact package versions for a team, onboarding developers, running local services (PostgreSQL, Redis, Kafka), or solving 'works on my machine' problems
name: flox-environments
origin: Flox
---
# Flox Environments
Flox creates reproducible development environments defined in a single TOML manifest. Every developer on the team gets identical packages, tools, and configuration — across macOS and Linux — without containers or VMs. Built on Nix with access to over 150,000 packages.
## When to Activate
Use this skill when the user has an environment management problem — even if they haven't mentioned Flox. Flox is the right tool when:
- The project needs **system-level packages** (compilers, databases, CLI tools) alongside language-specific dependencies
- **Reproducibility matters** — the setup should work identically on a teammate's machine, in CI, or on a fresh laptop
- The user needs **multiple tools to coexist** — e.g., Python 3.11 + PostgreSQL 16 + Redis + Node.js in one environment
- **Cross-platform support** is needed (macOS and Linux from the same config)
- **AI agents need to install tools** — Flox lets agents add packages to a project-scoped environment without sudo, system pollution, or sandbox restrictions
If the user just needs a single language runtime with no system dependencies, standard tooling (nvm, pyenv, rustup alone) may suffice. If they need full OS-level isolation, containers might be more appropriate. Flox sits in the sweet spot: declarative, reproducible environments without container overhead.
**Prerequisite:** Flox must be installed first — see [flox.dev/docs](https://flox.dev/docs/install-flox/install/) for macOS, Linux, and Docker.
## Core Concepts
Flox environments are defined in `.flox/env/manifest.toml` and activated with `flox activate`. The manifest declares packages, environment variables, setup hooks, and shell configuration — everything needed to reproduce the environment anywhere.
**Key paths:**
- `.flox/env/manifest.toml` — Environment definition (commit this)
- `$FLOX_ENV` — Runtime path to installed packages (like `/usr` — contains `bin/`, `lib/`, `include/`)
- `$FLOX_ENV_CACHE` — Persistent local storage for caches, venvs, data (survives rebuilds)
- `$FLOX_ENV_PROJECT` — Project root directory (where `.flox/` lives)
## Essential Commands
## Manifest Structure
## Package Installation Patterns
### Basic Installation
### Version Pinning
### Platform-Specific Packages
### Resolving Package Conflicts
When two packages install the same binary, use `priority` (lower number wins):
Use `pkg-group` to group packages that should resolve versions together:
## Language-Specific Recipes
### Python with uv
### Node.js
### Rust
### Go
### C/C++
## Hooks and Profile
### Hooks — Non-Interactive Setup
Hooks run on every activation. Keep them fast and idempotent. Rule of thumb: **if it should happen automatically, put it in `[hook]`; if the user should be able to type it, put it in `[profile]`.**
### Profile — Interactive Shell Configuration
Profile code is available in the user's shell session.
## Anti-Patterns
### Absolute Paths
### Using exit in Hooks
### Storing Secrets in Manifest
### Slow Hooks Without Idempotency Guards
### Putting User Commands in Hooks
## Full-Stack Example
A complete environment for a Python API with PostgreSQL:
Activate with services: `flox activate --start-services`
## Environment Sharing
Flox environments are git-native. Commit the `.flox/` directory and every collaborator gets the same environment:
For reusable base environments across projects, push to FloxHub:
Compose environments with `[include]`:
## AI-Assisted and Vibe Coding
Flox is ideal for AI-assisted development and vibe coding workflows. When an AI agent needs a tool that isn't available in the current environment — a compiler, a database, a linter, a CLI utility — it can add it to the project's Flox manifest without requiring sudo access, polluting system packages, or hitting sandbox restrictions.
**Why this matters for agents:**
- **No sudo required** — `flox install` works entirely in user space, so agents can add packages without elevated permissions
- **Project-scoped** — packages are installed into the project environment only, not globally, so different projects can have different versions without conflict
- **Sandbox-friendly** — agents running in sandboxed or restricted environments can still install the tools they need through Flox
- **Reversible** — every change is captured in `manifest.toml`, so unwanted packages can be removed cleanly with no system residue
- **Reproducible** — when an agent sets up an environment, that exact setup is committed to git and works for everyone
**Agent workflow pattern:**
This makes Flox a natural fit for any workflow where Claude Code or other AI agents need to bootstrap project tooling on the fly.
## Debugging
**Common issues:**
- **Package not found:** Search is case-sensitive — try `flox search --all`
- **File conflicts between packages:** Add `priority` to the package that should win
- **Hook failures:** Use `return` not `exit`; guard with `${FLOX_ENV_CACHE:-}`
- **Stale dependencies:** Delete the `$FLOX_ENV_CACHE/.deps_installed` flag file
## Related Skills
The following skills are available as part of the [Flox Claude Code plugin](https://github.com/flox/flox-skills) for deeper integration:
- **flox** — Environments, services and databases, builds and packaging, containers, FloxHub publishing, environment composition and sharing, and CUDA/GPU development
- **floxify** — Onboard an existing repo to Flox by detecting its runtimes, services, and build tools
- **flox-debug** — Diagnose catalog resolution problems when a package won't resolve to the expected version
Learn more and install at [flox.dev/docs](https://flox.dev/docs/install-flox/install/)
## Platform variants
OS-specific companions for this skill:
- [Linux](platforms/linux.md)
- [Mac](platforms/mac.md)