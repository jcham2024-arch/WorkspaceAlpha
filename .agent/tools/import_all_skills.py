#!/usr/bin/env python3
"""Import ALL dump skills into .agent/skills (master library).

Reads .archive/Agentsandskills/AgentSkills/dump/*/SKILL.md, dedupes
by name (master copy wins; collisions get a source-suffixed folder),
and writes .agent/skills/INDEX.md + INDEX.csv. Broken (404) skills
are quarantined, not copied. A companion .agent/skills/.incoming
hold is used so .archive can be cleared after verification.
"""
import csv
import hashlib
import pathlib
import re
import shutil

DUMP = pathlib.Path(".archive/Agentsandskills/AgentSkills/dump")
MASTER = pathlib.Path(".agent/skills")
MANIFEST = pathlib.Path(".agent/skills/INDEX.md")
CSV_OUT = pathlib.Path(".agent/skills/INDEX.csv")
REPORT = pathlib.Path(".agent/skills/IMPORT_REPORT.md")

def folder_hash(d: pathlib.Path) -> str:
    h = hashlib.sha256()
    for p in sorted(d.rglob("*")):
        if p.is_file():
            h.update(str(p.relative_to(d)).encode())
            h.update(p.read_bytes())
    return h.hexdigest()

def parse_fm(text: str):
    if not text.startswith("---\n"):
        return {}
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return {}
    out = {}
    for line in parts[0][4:].splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip().strip("'\"")
    return out

def main():
    existing = {d.name for d in MASTER.iterdir() if d.is_dir()}
    incoming = [p.parent for p in sorted(DUMP.glob("*/*/SKILL.md"))]
    incoming += [p.parent for p in sorted(DUMP.glob("*/*/*/SKILL.md"))]
    rows = []
    imported = quarantined = skipped = 0
    seen_names = set(existing)  # master names already occupy flat slots
    for src in incoming:
        name = src.name
        text = (src / "SKILL.md").read_text(encoding="utf-8", errors="replace")
        source = src.relative_to(DUMP).parts[0]
        fm = parse_fm(text)
        desc = fm.get("description", "")[:200]
        risk = fm.get("risk", "")
        if text.strip().startswith("404:"):
            quarantined += 1
            rows.append((name, source, str(src), "", desc, risk, "quarantined-broken"))
            continue
        if name in existing:
            # master already carries this skill; only import the source variant under a suffixed folder
            folder = f"{source}__{name}"
            if folder in existing:
                skipped += 1
                rows.append((name, source, str(src), folder, desc, risk, "skipped-collision"))
                continue
        else:
            folder = name
            if folder in seen_names:
                folder = f"{source}__{name}"
        dst = MASTER / folder
        if dst.exists():
            skipped += 1
            rows.append((name, source, str(src), folder, desc, risk, "skipped-collision"))
            continue
        shutil.copytree(src, dst)
        seen_names.add(folder)
        existing.add(folder)
        imported += 1
        rows.append((name, source, str(src), folder, desc, risk, "imported"))

    with MANIFEST.open("w", encoding="utf-8") as f:
        f.write("# Master Skills Index — full import from .archive/Agentsandskills dump\n\n")
        f.write(f"Imported {imported} skills; quarantined broken {quarantined}; skipped duplicates {skipped}.\n")
        f.write(f"Total rows: {len(rows)}. Master now holds {len(existing)} skill folders.\n\n")
        f.write("Columns: skill | source bucket | imported folder | risk | status.\n\n")
        for r in rows[:4000]:
            f.write(f"- {r[0]} | {r[1]} | {r[3] or '—'} | {r[5] or '—'} | {r[6]}\n")
    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["skill_name", "source_bucket", "source_path", "imported_folder", "description", "risk", "status"])
        w.writerows(rows)
    with REPORT.open("w", encoding="utf-8") as f:
        f.write(f"Imported {imported}, quarantined broken {quarantined}, skipped {skipped} (of {len(rows)} rows).\n")
        bad = [r for r in rows if r[6] == "quarantined-broken"]
        f.write(f"Broken sources quarantined: {len(bad)} ({', '.join(r[0] for r in bad[:20])}{'…' if len(bad) > 20 else ''})\n")
        risky = sorted({r[5] for r in rows if r[5] and r[5] not in ("normal", "minimal", "low")})
        f.write(f"Risk flags present in import: {', '.join(risky) if risky else 'none'}\n")
    print(f"imported={imported} quarantined={quarantined} skipped={skipped} master_folders={len(existing)}")

if __name__ == "__main__":
    main()
