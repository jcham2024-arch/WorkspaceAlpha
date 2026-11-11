#!/usr/bin/env python3
"""Audit the master skill library against the schema (read-only).

Checks per skill in .agent/skills/<name>/SKILL.md:
  - frontmatter present (--- ... ---)
  - frontmatter name matches folder name (or is suffixed by design)
  - description present and <= 60 words
  - body <= 500 lines
  - references/ files present (if any) carry the standard header
    (Scope: / Load when:)

Exit code 1 if any FAILURE-severity issue exists. Run via run.py audit.
"""
import argparse
import json
import pathlib
import re
import sys

MASTER = pathlib.Path(".agent/skills")


def main():
    ap = argparse.ArgumentParser(description="Audit master skill library (read-only)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    dirs = [d for d in sorted(MASTER.iterdir())
            if d.is_dir() and d.name != "_quarantine" and (d / "SKILL.md").exists()]
    fails, warns, ok = [], [], 0
    for d in dirs:
        sm = d / "SKILL.md"
        issues = []
        if not sm.exists():
            fails.append((d.name, "missing SKILL.md"))
            continue
        text = sm.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---\n") or text.find("\n---", 4) < 0:
            fails.append((d.name, "missing frontmatter"))
            continue
        fm = text[: text.find("\n---", 4)]
        name_m = re.search(r"^name:\s*(.+)$", fm, re.M)
        desc_m = re.search(r"^description:\s*(.+)$", fm, re.M)
        nm = name_m.group(1).strip().strip("'\"") if name_m else ""
        if nm != d.name and "__" not in d.name:
            warns.append((d.name, f"name mismatch frontmatter={nm!r}"))
        if not desc_m:
            fails.append((d.name, "missing description"))
        else:
            words = len(desc_m.group(1).strip().split())
            if words > 60:
                warns.append((d.name, f"description {words} words (>60)"))
        n = len(text.splitlines())
        if n > 500:
            fails.append((d.name, f"body {n} lines (>500)"))
        rd = d / "references"
        if rd.exists():
            for r in rd.glob("**/*.md"):
                rt = r.read_text(encoding="utf-8", errors="replace")[:700]
                if "Scope:" not in rt or "Load when:" not in rt:
                    warns.append((d.name, f"reference missing standard header: {r.name}"))
                    break
        ok += 1

    if args.json:
        print(json.dumps({"skills": ok, "fails": fails, "warnings": warns}, indent=2))
    else:
        print(f"skills checked: {ok}")
        print(f"failures: {len(fails)}")
        for name, msg in fails[:15]:
            print(f"  FAIL {name}: {msg}")
        print(f"warnings: {len(warns)}")
        suffixed = sum(1 for name, _ in warns if "__" in name)
        genuine = [(n_, m) for n_, m in warns if "__" not in n_]
        print(f"  (suffixed provenance dupes: {suffixed}; genuine: {len(genuine)})")
        for name, msg in genuine[:10]:
            print(f"  WARN {name}: {msg}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
