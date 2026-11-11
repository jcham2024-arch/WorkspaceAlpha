# dotnet-reverse — Windows

Scope: Windows variant of the `dotnet-reverse` skill.
Load when: you are doing `dotnet-reverse` on Windows.

## Context

PowerShell-first (5.x vs 7+); cmd.exe for batch; Windows APIs/UIA for desktop automation; `%PATH%` environment.
Topic: .NET/C# binary reverse engineering: managed PE analysis, dnSpyEx debugging, de4dot deobfuscation (ConfuserEx/SmartAssembly/Babel), IL patching, NativeAOT targets, and analysis of red-team Sharp* tooling.

## Scripting

`pwsh`/`powershell` (never bashisms in .ps1); `Set-ExecutionPolicy` for scripts; CRLF line endings; case-insensitive FS. Pitfalls: Defender blocks unsigned scripts; `.ps1` line endings.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
