#!/usr/bin/env python3
"""Add an `os` column (android|windows|linux|mac|cross) to every skill
in CATEGORIZATION.csv. Whole-word matching on name + description to
avoid the substring problem ('mac' inside 'machine'). Heuristic but
explicit: cross = no OS tag found (OS-agnostic) or multiple OS tags.
Re-run after categorize.py changes."""
import csv
import pathlib
import re

CSV = pathlib.Path(".agent/skills/CATEGORIZATION.csv")
OS_PATTERNS = {
    "android": re.compile(r"\b(android|apk|kotlin|jetpack|adb|gradle|android ui)\b", re.I),
    "windows": re.compile(r"\b(windows|win32|powershell|wpf|winforms|cmd\.exe|\.net|dotnet)\b", re.I),
    "linux": re.compile(r"\b(linux|bash|zsh|docker|kubernetes|k8s|terraform|systemd|apt|dnf)\b", re.I),
    "mac": re.compile(r"\b(mac|macos|darwin|homebrew|brew|xcode)\b", re.I),
}

def classify(name, desc):
    text = f"{name} {desc}"
    hits = [os for os, pat in OS_PATTERNS.items() if pat.search(text)]
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1:
        return "cross+(" + "+".join(hits) + ")"
    return "cross"

def main():
    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    for r in rows:
        r["os"] = classify(r["skill"], r["description"])
    with CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["skill", "task_type", "subtype", "level", "os", "folder", "description"])
        w.writeheader()
        w.writerows(rows)
    from collections import Counter
    c = Counter(r["os"] for r in rows)
    print("os distribution:", dict(c.most_common()))

if __name__ == "__main__":
    main()
