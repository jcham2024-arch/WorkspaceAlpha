# anti-sleep — Mac

Scope: Mac variant of the `anti-sleep` skill.
Load when: you are doing `anti-sleep` on Mac.

## Context

POSIX base + Apple extensions (Frameworks, Keychain, Gatekeeper, Xcode); zsh default; Homebrew prefixes.
Topic: Keep a Mac awake with caffeinate during long builds, downloads, or supervised automation runs.

## Scripting

zsh scripts; `brew install`, `brew services` for daemons; `osascript` for GUI tasks. Pitfalls: Gatekeeper quarantine (`xattr -d com.apple.quarantine`), arm64 vs Intel, code-signing/notarization.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
