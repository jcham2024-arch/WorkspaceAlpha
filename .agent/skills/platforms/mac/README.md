# Platform Variant — Mac

For skills that diverge on Mac (macOS/Darwin). Context + scripting notes.

## Pattern

Variant lives either inline (`os: mac` + body OS section) or as
`platforms/mac.md` inside the skill folder.

## Context

- POSIX base + Apple extensions (Frameworks, App Bundle, Keychain,
  Gatekeeper, Xcode); zsh default shell since Catalina.
- Paths: `/Applications`, `~/Library`, Homebrew prefix
  (`/opt/homebrew` Apple Silicon, `/usr/local` Intel).

## Scripting

- Shell: `zsh`; package manager `brew` (`brew install`, then
  `brew services` for daemons); AppleScript/`osascript` for
  GUI-level tasks.
- Pitfalls: Gatekeeper quarantine on downloaded scripts
  (`xattr -d com.apple.quarantine`), Apple Silicon arm64 vs Intel
  (Rosetta), code signing/notarization for shipped binaries.

## Top matching skills

- Filter CATEGORIZATION.csv by os=mac for today's candidates
  (xcode/homebrew/darwin keywords).

Routing: provision by `os=mac` within coding/research roles.
