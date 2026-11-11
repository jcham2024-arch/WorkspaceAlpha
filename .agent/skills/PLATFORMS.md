# Platforms — OS-Specific Variants

Cross-platform default: 3,344 of 3,518 skills are OS-agnostic
(`os = cross` in CATEGORIZATION.csv). OS-specific skills carry an
`os` value + supporting files. Two attachment patterns:

## Pattern A — inline `os` tag (preferred for most skills)

Add to the skill's frontmatter:

    os: android|windows|linux|mac

and note OS context in the body with a dedicated section:
OS context (semantics, paths, APIs), OS scripting (best shell +
commands), OS pitfalls. One SKILL.md per skill, OS variants
concern only that skill's topic.

## Pattern B — `platforms/` companion (when a skill spans OSes)

A skill that is portable but OS-flavoured gets companion files
inside ITS folder:

    skills/<name>/platforms/
      android.md   (context + scripting for Android)
      windows.md   (context + scripting for Windows)
      linux.md     (context + scripting for Linux)
      mac.md       (context + scripting for Mac)

Linked from SKILL.md: "For Android: See platforms/android.md."
Variants are plain references — one level deep, standard header.

## Per-OS quick stock

- android/ — Android specifics (Kotlin, Jetpack, ADB, Gradle)
  Top matches: android-jetpack-compose-expert, android-cli,
  android-ui-journey-testing.
- windows/ — cmd/PowerShell scripting, .NET, UIA. Top matches:
  windows-desktop-e2e, azure-ai-agents-persistent-dotnet.
- linux/ — bash/zsh, Docker, systemd, distro package managers.
- mac/ — macOS, Homebrew, Xcode, Darwin specifics.

Routing: profiles provision by `task_type + level + os` (the `os`
column), e.g. "coding-manager → frontend-web/worker, os=android".
Never provision all 4 variants unless the task explicitly spans
them — pick the smallest OS set the task needs.
