# Platform Variant — Windows

For skills that diverge on Windows. Context + scripting notes.

## Pattern

Variant lives either inline (frontmatter `os: windows` + body OS
section) or as `platforms/windows.md` inside the skill folder.

## Context

- PowerShell-first (Windows PowerShell 5.x vs PowerShell 7+);
  POSIX shells via WSL for bash; cmd.exe for batch.
- Paths: drvletter (`C:\...`), environment variables (`%OS%`).

## Scripting

- Shell: `pwsh` or `powershell` (never bashisms in .ps1).
- Pits: execution policy (`Set-ExecutionPolicy`), case-insensitive
  but case-preserving filesystems, line endings (CRLF), Windows
  Defender blocking unsigned scripts.

## Top matching skills

- windows-desktop-e2e — WPF/WinForms/Win32/Qt UI Automation
- azure-ai-agents-persistent-dotnet — .NET agents

Routing: provision by `os=windows` within coding/research roles.
