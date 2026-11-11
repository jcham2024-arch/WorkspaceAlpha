# swiftui-expert-skill — Mac

Scope: Mac variant of the `swiftui-expert-skill` skill.
Load when: you are doing `swiftui-expert-skill` on Mac.

## Context

POSIX base + Apple extensions (Frameworks, Keychain, Gatekeeper, Xcode); zsh default; Homebrew prefixes.
Topic: Write, review, and refactor SwiftUI for iOS or macOS, covering data flow, view composition, performance, identity, environment, localization, animation, API migration, and Instruments traces.

## Scripting

zsh scripts; `brew install`, `brew services` for daemons; `osascript` for GUI tasks. Pitfalls: Gatekeeper quarantine (`xattr -d com.apple.quarantine`), arm64 vs Intel, code-signing/notarization.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
