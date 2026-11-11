# apple-notes-search — Mac

Scope: Mac variant of the `apple-notes-search` skill.
Load when: you are doing `apple-notes-search` on Mac.

## Context

POSIX base + Apple extensions (Frameworks, Keychain, Gatekeeper, Xcode); zsh default; Homebrew prefixes.
Topic: Semantic + keyword search and connection-discovery across the user's own Apple Notes via the apple-notes MCP server. Use when the user wants to find, recall, or synthesize something from their notes, or surface non-obvious bridges/related notes. macOS, on-device.

## Scripting

zsh scripts; `brew install`, `brew services` for daemons; `osascript` for GUI tasks. Pitfalls: Gatekeeper quarantine (`xattr -d com.apple.quarantine`), arm64 vs Intel, code-signing/notarization.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
