# azure-search-documents-dotnet — Windows

Scope: Windows variant of the `azure-search-documents-dotnet` skill.
Load when: you are doing `azure-search-documents-dotnet` on Windows.

## Context

PowerShell-first (5.x vs 7+); cmd.exe for batch; Windows APIs/UIA for desktop automation; `%PATH%` environment.
Topic: Azure AI Search SDK for .NET (Azure.Search.Documents). Use for building search applications with full-text, vector, semantic, and hybrid search.

## Scripting

`pwsh`/`powershell` (never bashisms in .ps1); `Set-ExecutionPolicy` for scripts; CRLF line endings; case-insensitive FS. Pitfalls: Defender blocks unsigned scripts; `.ps1` line endings.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
