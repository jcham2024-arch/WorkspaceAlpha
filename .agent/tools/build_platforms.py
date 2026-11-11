#!/usr/bin/env python3
"""Generate per-OS companion files for OS-tagged skills.

For every master skill whose `os` tag (CATEGORIZATION.csv) matches
one of android|windows|linux|mac (minus cross), write
`platforms/<os>.md` inside the skill folder using the OS template +
a topic line from the skill's frontmatter. Also appends an
"## Platform variants" section to SKILL.md linking the companions.
Cross (OS-agnostic) skills are untouched — they already work anywhere.
Re-run any time; existing companions are preserved.
"""
import csv
import pathlib
import re

MASTER = pathlib.Path(".agent/skills")
CSV = MASTER / "CATEGORIZATION.csv"

OS_TEMPLATES = {
    "android": {
        "context": "Kotlin/Compose-first. Android lifecycle (Activity, Service, WorkManager), internal/cache/scoped storage, permission model.",
        "scripting": "Shell + ADB; `./gradlew assembleDebug`, `adb install`, `logcat`, `adb shell dumpsys`. Pitfalls: Doze/App Standby background limits, emulator-vs-device drift, scoped-storage restrictions.",
    },
    "windows": {
        "context": "PowerShell-first (5.x vs 7+); cmd.exe for batch; Windows APIs/UIA for desktop automation; `%PATH%` environment.",
        "scripting": "`pwsh`/`powershell` (never bashisms in .ps1); `Set-ExecutionPolicy` for scripts; CRLF line endings; case-insensitive FS. Pitfalls: Defender blocks unsigned scripts; `.ps1` line endings.",
    },
    "linux": {
        "context": "bash/zsh default; systemd services; POSIX paths; distro package managers (apt/dnf/pacman).",
        "scripting": "`#!/bin/sh` POSIX scripts, `set -euo pipefail` for bash; docker/podman for isolation. Pitfalls: distro drift, missing jq/python3, SELinux/AppArmor in hardened hosts.",
    },
    "mac": {
        "context": "POSIX base + Apple extensions (Frameworks, Keychain, Gatekeeper, Xcode); zsh default; Homebrew prefixes.",
        "scripting": "zsh scripts; `brew install`, `brew services` for daemons; `osascript` for GUI tasks. Pitfalls: Gatekeeper quarantine (`xattr -d com.apple.quarantine`), arm64 vs Intel, code-signing/notarization.",
    },
}

def frontmatter_topic(skill_path):
    text = skill_path.read_text(encoding="utf-8", errors="replace")
    name = skill_path.parent.name
    desc = ""
    if text.startswith("---\n"):
        m = re.search(r"^name:\s*(.+)$", text[:600], re.M)
        if m:
            name = m.group(1).strip().strip("'\"")
        m = re.search(r"^description:\s*(.+)$", text[:2000], re.M)
        if m:
            desc = m.group(1).strip().strip('"').strip("'")
    return name, desc

def companion(skill, os_, name, desc, tmpl):
    return f"""# {name} — {os_.title()}

Scope: {os_.title()} variant of the `{skill}` skill.
Load when: you are doing `{name}` on {os_.title()}.

## Context

{tmpl["context"]}
Topic: {desc}

## Scripting

{tmpl["scripting"]}

## Pitfalls

- Adapt the base skill's generic steps to the OS commands above.
- Verify in a shell loop before committing OS-specific chunks.

## Notes

- Base skill: SKILL.md (topic instructions, OS-agnostic).
- Generated variant; hand-tune after first task use.
"""

def main():
    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    made = skills_touched = 0
    for r in rows:
        os_tag = (r.get("os") or "cross").lower()
        if os_tag == "cross":
            continue
        # parse cross+(a+b) combos
        if os_tag.startswith("cross+("):
            oses = os_tag[len("cross+("):-1].split("+")
        else:
            oses = [os_tag]
        folder = MASTER / r["folder"]
        if not folder.is_dir():
            continue
        sm = folder / "SKILL.md"
        topic_name, desc = frontmatter_topic(sm)
        pd = folder / "platforms"
        pd.mkdir(exist_ok=True)
        created_for_skill = False
        for os_ in oses:
            f = pd / f"{os_}.md"
            if f.exists():
                continue
            f.write_text(companion(r["skill"], os_, topic_name, desc, OS_TEMPLATES[os_]), encoding="utf-8")
            made += 1
            created_for_skill = True
        if created_for_skill:
            # append a Platform variants section to SKILL.md if missing
            text = sm.read_text(encoding="utf-8")
            if "## Platform variants" not in text:
                links = "\n".join(f"- [{o.title()}](platforms/{o}.md)" for o in oses)
                sm.write_text(text.rstrip() + "\n\n## Platform variants\n\n" +
                              "OS-specific companions for this skill:\n\n" + links + "\n", encoding="utf-8")
            skills_touched += 1
    print(f"companions created: {made} across {skills_touched} skills")

if __name__ == "__main__":
    main()
