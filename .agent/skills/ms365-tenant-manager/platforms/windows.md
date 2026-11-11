# ms365-tenant-manager — Windows

Scope: Windows variant of the `ms365-tenant-manager` skill.
Load when: you are doing `ms365-tenant-manager` on Windows.

## Context

PowerShell-first (5.x vs 7+); cmd.exe for batch; Windows APIs/UIA for desktop automation; `%PATH%` environment.
Topic: Use for Microsoft 365 tenant administration (Entra ID users, Exchange Online, Teams, licenses, Conditional Access, compliance reports). Plans setup with tenant_setup.py, bulk-manages users with user_management.py and generates PowerShell with powershell_generator.py.

## Scripting

`pwsh`/`powershell` (never bashisms in .ps1); `Set-ExecutionPolicy` for scripts; CRLF line endings; case-insensitive FS. Pitfalls: Defender blocks unsigned scripts; `.ps1` line endings.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
