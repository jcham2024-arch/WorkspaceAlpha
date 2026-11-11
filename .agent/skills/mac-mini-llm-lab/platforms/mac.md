# mac-mini-llm-lab — Mac

Scope: Mac variant of the `mac-mini-llm-lab` skill.
Load when: you are doing `mac-mini-llm-lab` on Mac.

## Context

POSIX base + Apple extensions (Frameworks, Keychain, Gatekeeper, Xcode); zsh default; Homebrew prefixes.
Topic: Configure a Mac mini as a reliable local LLM server with remote access,

## Scripting

zsh scripts; `brew install`, `brew services` for daemons; `osascript` for GUI tasks. Pitfalls: Gatekeeper quarantine (`xattr -d com.apple.quarantine`), arm64 vs Intel, code-signing/notarization.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
