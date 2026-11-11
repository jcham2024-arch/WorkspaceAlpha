# context-optimization — Windows

Scope: Windows variant of the `context-optimization` skill.
Load when: you are doing `context-optimization` on Windows.

## Context

PowerShell-first (5.x vs 7+); cmd.exe for batch; Windows APIs/UIA for desktop automation; `%PATH%` environment.
Topic: Context optimization extends the effective capacity of limited context windows through strategic compression, masking, caching, and partitioning. The goal is not to magically increase context windows but to make better use of available capacity.

## Scripting

`pwsh`/`powershell` (never bashisms in .ps1); `Set-ExecutionPolicy` for scripts; CRLF line endings; case-insensitive FS. Pitfalls: Defender blocks unsigned scripts; `.ps1` line endings.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
