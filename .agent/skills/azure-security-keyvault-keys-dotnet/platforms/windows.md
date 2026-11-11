# azure-security-keyvault-keys-dotnet — Windows

Scope: Windows variant of the `azure-security-keyvault-keys-dotnet` skill.
Load when: you are doing `azure-security-keyvault-keys-dotnet` on Windows.

## Context

PowerShell-first (5.x vs 7+); cmd.exe for batch; Windows APIs/UIA for desktop automation; `%PATH%` environment.
Topic: Azure Key Vault Keys SDK for .NET. Client library for managing cryptographic keys in Azure Key Vault and Managed HSM. Use for key creation, rotation, encryption, decryption, signing, and verification.

## Scripting

`pwsh`/`powershell` (never bashisms in .ps1); `Set-ExecutionPolicy` for scripts; CRLF line endings; case-insensitive FS. Pitfalls: Defender blocks unsigned scripts; `.ps1` line endings.

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
