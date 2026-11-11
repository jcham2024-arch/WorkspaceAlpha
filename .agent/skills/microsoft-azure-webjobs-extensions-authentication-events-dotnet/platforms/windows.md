# microsoft-azure-webjobs-extensions-authentication-events-dotnet — Windows

Scope: Windows variant of the `microsoft-azure-webjobs-extensions-authentication-events-dotnet` skill.
Load when: you are doing `microsoft-azure-webjobs-extensions-authentication-events-dotnet` on Windows.

## Context

PowerShell-first (5.x vs 7+); cmd.exe for batch; Windows APIs/UIA for desktop automation; `%PATH%` environment.
Topic: Microsoft Entra Authentication Events SDK for .NET. Azure Functions triggers for custom authentication extensions.

## Scripting

`pwsh`/`powershell` (never bashisms in .ps1); `Set-ExecutionPolicy` for scripts; CRLF line endings; case-insensitive FS. Pitfalls: Defender blocks unsigned scripts; `.ps1` line endings.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
