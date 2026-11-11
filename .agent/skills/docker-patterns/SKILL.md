---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 2f3f18ab7588844be42560bdfb25e3b6e8c4f5a3fa6674d697334c9ccd7ed19e
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
description: Docker and Docker Compose patterns for local development, hardened CLI installer harnesses, container security, networking, volumes, and multi-service orchestration. Use when creating or reviewing Dockerfiles and Compose services, testing installers across Linux distributions, or planning accurate native macOS and Windows validation.
name: docker-patterns
---
# Docker Patterns
Docker and Docker Compose best practices for containerized development.
## Docker Compose for Local Development
### Standard Web App Stack
### Development vs Production Dockerfile
### Override Files
## Networking
### Service Discovery
Services in the same Compose network resolve by service name:
```
# From "app" container:
postgres://postgres:postgres@db:5432/app_dev    # "db" resolves to the db container
redis://redis:6379/0                             # "redis" resolves to the redis container
```
### Custom Networks
### Exposing Only What's Needed
## Volume Strategies
### Common Patterns
## Container Security
### Dockerfile Hardening
### Compose Security
### Secret Management
## Hardened CLI Installer Harnesses
Use containers to test installer behavior against disposable project copies without allowing the test to mutate the source checkout.
### Respect the Platform Boundary
- Run real containers for Linux distributions such as Debian and Ubuntu.
- macOS cannot run as a Docker container because Docker shares a Linux kernel. Run the same shell-free test entry point natively on macOS.
- Windows containers require a Windows Docker engine. Run platform-independent logic on a native Windows CI runner and reserve Windows containers for a Windows host.
- Keep a native Ubuntu/macOS/Windows CI matrix for host-specific paths, command shims, quoting, and filesystem behavior.
Do not claim that a Linux container validates macOS or Windows behavior.
### Enforce the Isolation Contract
- Pin base images by immutable digest and pin installed CLI versions.
- Run as a non-root numeric UID/GID when distro account names differ.
- Mount the repository and source project read-only.
- Copy the source project into a writable `tmpfs` workspace before any mutation.
- Mount `/workspace` with `noexec`, UID/GID 1000, and `mode=0700` so only the
  container user can inspect project data.
- Keep npm and npx's executable cache at `NPM_CONFIG_CACHE=/tmp/npm-cache` on
  the executable `/tmp` mount. Its default size is 2 GiB and can be adjusted
  with `ECC_TMPFS_SIZE`; `ECC_WORKSPACE_SIZE` separately controls the private
  workspace mount.
- Set `read_only: true`, `no-new-privileges:true`, `cap_drop: [ALL]`, and a finite `pids_limit`.
- Keep the default real-CLI services on `network_mode: none`. Add network access
  only through a visibly named opt-in service for an authenticated provider
  session; never make it an accidental environment-driven default.
- Create only the writable temporary paths the tool needs.
- Do not pass host credentials into the container by default.
- Default to a dry run and whitelist only the explicit `dry-run`, `install`,
  `plugin`, and `shell` modes.
- Use argument arrays or `spawnSync(..., { shell: false })` for cross-platform runners. Never interpolate project paths into a shell command.
### Exercise the ECC Plugin Setup Harness
Use `docker/plugin-setup/compose.yaml` as the reference implementation. It provides:
- `fixture-tests` for the focused install manifest, target, and executor suite.
- `real-cli` for the pinned Debian-based generic Linux image.
- `real-cli-ubuntu` for the pinned Ubuntu image.
Validate the Compose model before building:
Build both real Linux images:
Run the safe default flow in each image:
The dry run executes the current public command contract:
Before that command runs, the container creates a locally packed npm artifact
from the read-only checkout with `npm pack --ignore-scripts`. It extracts the
self-created tarball under `/tmp`, validates the `ecc-universal` package name,
required install manifests, and the confined `package.json` `bin.ecc` mapping,
then invokes the extracted `ecc` executable. The runtime stays on
`network_mode: none`, does not execute package lifecycle scripts, and does not
rely on host `node_modules`; its exact pinned production dependencies are
already present in the image.
The harness rejects an empty plan, a non-`claude-project` target, any operation
outside `/workspace/project/.claude`, or any dry run that creates the target
directory. `install` performs the isolated apply twice, checks its managed
install state, lists the installed target, and runs `doctor`.
### Start, Open, Reconnect, and Clean Up a Named Session
Start a detached container without `--rm` so leaving a terminal does not remove
the session:
The container copies the read-only fixture to the stable private directory
`/workspace/project`. Confirm it is running, then emit the Docker side of the
terminal-opener v1 data contract:
The JSON result has exactly an `executable` and `argv` boundary (plus
`contractVersion: 1`): the executable is `docker`, and argv begins with
`exec`, `-it`, and `-w`. Pass that data to the separate terminal-opener skill
when it is installed. This Docker harness deliberately does not import a
terminal adapter, interpolate a shell command, or manage a host GUI process.
Until then, open the same PTY in the current host terminal directly:
Exit the shell without stopping the detached container. Reconnect with the
same `docker exec -it` command. When finished, remove the exact named container
and its Compose project resources:
Host credentials are absent by default and credential directories are never
mounted. The default service also has no network access. When an authenticated
provider session genuinely needs a network, build `real-cli` first and then opt
in visibly with `docker compose -f docker/plugin-setup/compose.yaml
--profile networked run --service-ports real-cli-networked shell`. The
`--service-ports` flag publishes the service's loopback callback mapping.
Prefer authenticating inside that disposable session. If a CI run must
inherit a host environment credential, make that opt-in at invocation with an
explicit Compose `--env NAME` flag, understand that the value is inspectable
and can be exfiltrated for the container lifetime, and remove the exact named
container immediately after.
### Authenticate Codex Inside the Networked Session
`codex login` binds its OAuth callback server to `127.0.0.1:1455` inside the
container. A Docker port publish forwards to the container interface, not
loopback, so the host browser's redirect to `http://localhost:1455` is refused
without a bridge. The `real-cli-networked` service publishes host
`127.0.0.1:1455` to container port `1456`; bridge that port to loopback before
logging in:
The networked service sets `NPM_CONFIG_PREFIX=/tmp/ecc-npm` and adds its `bin`
directory to `PATH`. This keeps the pinned installation writable for UID 1000
on the executable `/tmp` mount while the root filesystem remains read-only.
Complete the sign-in in the host browser. Each attempt mints a fresh
`state`/`code`, so always follow the newest printed link. The token stays in
the disposable container's `~/.codex/auth.json`; removing the named container
deletes that credential copy. The login block stops the relay on success or failure.
Only one container can hold host port 1455 at a time
because the OAuth redirect targets a fixed port.
The host publish is restricted to loopback. Inside the container, the relay
listens on all interfaces so Docker can forward to it; other containers on the
same bridge network can reach it while it runs. Use a dedicated network without
untrusted peers for this login, and remove the exact named container after use.
Idle callback connections close after 30 seconds.
Run the same focused suite natively on the host:
Inspect the produced identity and environment before trusting the image:
Clean each named test project without deleting unrelated volumes or images:
## .dockerignore
```
node_modules
.git
.env
.env.*
dist
coverage
*.log
.next
.cache
docker-compose*.yml
Dockerfile*
README.md
tests/
```
## Debugging
### Common Commands
### Debugging Network Issues
## Anti-Patterns
```
# BAD: Using docker compose in production without orchestration
# Use Kubernetes, ECS, or Docker Swarm for production multi-container workloads
# BAD: Storing data in containers without volumes
# Containers are ephemeral -- all data lost on restart without volumes
# BAD: Running as root
# Always create and use a non-root user
# BAD: Using :latest tag
# Pin to specific versions for reproducible builds
# BAD: One giant container with all services
# Separate concerns: one process per container
# BAD: Putting secrets in docker-compose.yml
# Use .env files (gitignored) or Docker secrets
```
## Platform variants
OS-specific companions for this skill:
- [Linux](platforms/linux.md)