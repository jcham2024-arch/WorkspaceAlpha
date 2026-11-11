# ADR-003: Why Python Standard Library Only

## Status

Accepted

## Context

The baselayer tooling (`seed.py`, `build.py`, `validate.py`, and all `tools/`) runs in the AndroidHarness environment (Android 17, API 37, app UID). Three dependency options were considered:

1. **pip install**: Requires network access, package management, and potential compilation of native extensions. Not always available in the Android/Termux environment.
2. **Vendored dependencies**: Bundling third-party packages in the repo increases size and creates supply-chain concerns.
3. **Standard library only**: Uses only Python 3.14 stdlib modules. Zero dependencies, zero network, zero compilation.

## Decision

All baselayer tooling uses Python 3 standard library only. No `pip install` of any kind. Tools that need HTTP (e.g., `check_links.py`) use `urllib.request`. Tools that need hashing use `hashlib`. Tools that need JSON use `json`.

## Consequences

**Positive:**
- Zero network required — works fully offline
- Zero installation — runs on any Python 3.14+ system
- No supply-chain attacks via compromised packages
- Predictable behavior across environments
- Smaller repo (no vendored packages)

**Negative:**
- More verbose code for common tasks (e.g., HTTP, argument parsing)
- Some modern Python features unavailable (but 3.14 is quite complete)
- Cannot use rich ecosystem (requests, click, pyyaml, etc.)

## Links

- Build scripts: `.wiki/seed.py`, `.wiki/build.py`
- Validator: `validate.py`
- Tooling: `tools/`
- Environment: `.agent/agent.md` §"Environment facts"
