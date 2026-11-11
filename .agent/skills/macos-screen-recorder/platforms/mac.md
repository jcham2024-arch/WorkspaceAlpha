# macos-screen-recorder — Mac

Scope: Mac variant of the `macos-screen-recorder` skill.
Load when: you are doing `macos-screen-recorder` on Mac.

## Context

POSIX base + Apple extensions (Frameworks, Keychain, Gatekeeper, Xcode); zsh default; Homebrew prefixes.
Topic: macOS screen recorder that captures the main display PLUS system audio via ScreenCaptureKit — no BlackHole/loopback driver, no sudo, just the standard Screen Recording permission. CLI-driven; fills the headless-screen-recording-with-system-sound gap QuickTime and `screencapture -v` can't.

## Scripting

zsh scripts; `brew install`, `brew services` for daemons; `osascript` for GUI tasks. Pitfalls: Gatekeeper quarantine (`xattr -d com.apple.quarantine`), arm64 vs Intel, code-signing/notarization.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
