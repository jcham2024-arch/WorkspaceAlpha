# dotnet-backend — Windows

Scope: Windows variant of the `dotnet-backend` skill.
Load when: you are doing `dotnet-backend` on Windows.

## Context

PowerShell-first (5.x vs 7+); cmd.exe for batch; Windows APIs/UIA for desktop automation; `%PATH%` environment.
Topic: Build ASP.NET Core 8+ backend services with EF Core, auth, background jobs, and production API patterns.

## Scripting

`pwsh`/`powershell` (never bashisms in .ps1); `Set-ExecutionPolicy` for scripts; CRLF line endings; case-insensitive FS. Pitfalls: Defender blocks unsigned scripts; `.ps1` line endings.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
