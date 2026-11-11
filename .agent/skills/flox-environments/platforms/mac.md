# flox-environments — Mac

Scope: Mac variant of the `flox-environments` skill.
Load when: you are doing `flox-environments` on Mac.

## Context

POSIX base + Apple extensions (Frameworks, Keychain, Gatekeeper, Xcode); zsh default; Homebrew prefixes.
Topic: Create reproducible, cross-platform (macOS/Linux) development environments with Flox, a declarative Nix-based environment manager. Use when setting up project toolchains, installing system-level dependencies (compilers, databases, native libs), pinning exact package versions for a team, onboarding developers, running local services (PostgreSQL, Redis, Kafka), or solving 'works on my machine' problems

## Scripting

zsh scripts; `brew install`, `brew services` for daemons; `osascript` for GUI tasks. Pitfalls: Gatekeeper quarantine (`xattr -d com.apple.quarantine`), arm64 vs Intel, code-signing/notarization.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
