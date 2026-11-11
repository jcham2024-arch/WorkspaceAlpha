#!/usr/bin/env python3
"""Knowledge system CLI + DB sync (stdlib only).

Persists session knowledge in human-readable Markdown (memory/) and
makes it searchable via SQLite FTS5 (.context/knowledge.db) + a tiny
JSON index (memory/index.json).

Commands:
  add --kind {work,error,lesson,decision} --title <text> [--tags a,b]
      append an entry to the matching file, then sync
  sync            rebuild DB + index from memory files
  search <query>  keyword search (FTS5, fallback substring)
  last --kind work [-n 5]   recent entries of one kind

Entry format in files: append-only bullets
  - YYYY-MM-DD | kind: title | tags: a,b
    continuation lines indented 2 spaces
Kinds map to files:
  work -> memory/JOURNAL.md
  error -> memory/ERRORS.md
  lesson -> memory/LESSONS.md
  decision -> memory/DECISIONS.md
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEM = ROOT / "memory"
DB = ROOT / ".context" / "knowledge.db"
INDEX = MEM / "index.json"

KIND_FILE = {
    "work": MEM / "JOURNAL.md",
    "error": MEM / "ERRORS.md",
    "lesson": MEM / "LESSONS.md",
    "decision": MEM / "DECISIONS.md",
}
ENTRY_RE = re.compile(r"^-\s+(\d{4}-\d{2}-\d{2})\s*\|\s*(\w+):\s*(.*?)\s*\|\s*tags:\s*(.*)$")

HEADER = {
    "work": "# Work Journal\n\nSummaries of completed work. Append-only; newest first is NOT required — append at the end, sync after.\n\n## Entries\n",
    "error": "# Problems Registry\n\nErrors found, root cause, fix, recurrence watch. Append-only.\n\n## Entries\n",
    "lesson": "# Lessons\n\nDistilled principles to apply in future sessions. Append-only; corrections are new entries.\n\n## Entries\n",
    "decision": "# Decisions\n\nADR-lite: decision + context + rationale. Append-only.\n\n## Entries\n",
}


def ensure_files():
    for kind, path in KIND_FILE.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(HEADER[kind], encoding="utf-8")


def parse_entries(path: Path):
    entries, current = [], None
    if not path.exists():
        return entries
    kind_guess = None
    for name, k in KIND_FILE.items():
        if path == k:
            kind_guess = name
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ENTRY_RE.match(line)
        if m:
            current = {"date": m.group(1), "kind": m.group(2), "title": m.group(3),
                       "tags": [t.strip() for t in m.group(4).split(",") if t.strip()],
                       "body": "", "file": str(path.relative_to(ROOT))}
            entries.append(current)
            continue
        if current and line.startswith("  "):
            current["body"] += "\n" + line.strip()
    return entries


def sync():
    ensure_files()
    entries = []
    for path in KIND_FILE.values():
        entries.extend(parse_entries(path))
    DB.parent.mkdir(parents=True, exist_ok=True)
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE entries (
        date TEXT, kind TEXT, title TEXT, body TEXT, tags TEXT, file TEXT)""")
    try:
        con.execute("CREATE VIRTUAL TABLE entries_fts USING fts5(title, body, tags, content='')")
        has_fts = True
    except sqlite3.OperationalError:
        has_fts = False
    for e in entries:
        con.execute("INSERT INTO entries VALUES (?,?,?,?,?,?)",
                    (e["date"], e["kind"], e["title"], e["body"], ",".join(e["tags"]), e["file"]))
        if has_fts:
            con.execute("INSERT INTO entries_fts(rowid, title, body, tags) VALUES (?,?,?,?)",
                        (len(entries), e["title"], e["body"], ",".join(e["tags"])))
    con.commit()
    con.close()
    INDEX.write_text(json.dumps(
        {"version": 1, "entries": [
            {"date": e["date"], "kind": e["kind"], "title": e["title"], "tags": e["tags"]}
            for e in entries], "count": len(entries)},
        indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"knowledge: {len(entries)} entries synced ({kinds(entries)})")


def kinds(entries):
    from collections import Counter
    return ", ".join(f"{k}:{v}" for k, v in Counter(e["kind"] for e in entries).most_common())


def add(kind, title, tags, body):
    ensure_files()
    entry = (kind, title, tags, body)
    today = datetime.date.today().isoformat()
    path = KIND_FILE[kind]
    line = f"- {today} | {kind}: {title} | tags: {','.join(tags) if tags else 'misc'}\n"
    if body:
        line += f"  {body.replace(chr(10), chr(10) + '  ')}\n"
    with path.open("a", encoding="utf-8") as f:
        f.write(line)
    sync()
    print(f"added {kind}: {title}")


def _search_fallback(q):
    con = sqlite3.connect(DB)
    rows = con.execute("SELECT date, kind, title, body, tags FROM entries").fetchall()
    con.close()
    out = [r for r in rows if q.lower() in (r[2] + " " + r[3] + " " + (r[4] or "")).lower()]
    return out


def search(query, limit=10):
    if not DB.exists():
        sync()
    con = sqlite3.connect(DB)
    try:
        rows = con.execute(
            "SELECT date, kind, title, body, tags FROM entries_fts"
            " WHERE entries_fts MATCH ? LIMIT ?", (query, limit)).fetchall()
        mode = "fts"
    except sqlite3.OperationalError:
        rows = _search_fallback(query)[:limit] if True else []
        mode = "substring"
    con.close()
    for r in rows:
        print(f"[{r[0]} {r[1]}] {r[2]}")
        if r[3]:
            print("  " + r[3].replace("\n", "\n  ")[:300])
    if not rows:
        print("no matches for:", query)


def last(kind, n=5):
    con = sqlite3.connect(DB)
    rows = con.execute(
        "SELECT date, title, body, tags FROM entries WHERE kind=? ORDER BY date DESC, rowid DESC LIMIT ?",
        (kind, n)).fetchall()
    con.close()
    for r in rows:
        print(f"[{r[0]}] {r[1]}")
        if r[2]:
            print("  " + r[2].replace("\n", "\n  ")[:300])


def main():
    ap = argparse.ArgumentParser(prog="knowledge.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pa = sub.add_parser("add")
    pa.add_argument("--kind", required=True, choices=list(KIND_FILE))
    pa.add_argument("--title", required=True)
    pa.add_argument("--body", default="")
    pa.add_argument("--tags", default="")
    sub.add_parser("sync")
    ps = sub.add_parser("search")
    ps.add_argument("query")
    pl = sub.add_parser("last")
    pl.add_argument("--kind", required=True)
    pl.add_argument("-n", type=int, default=5)
    args = ap.parse_args()

    if args.cmd == "add":
        add(args.kind, args.title, [t for t in args.tags.split(",") if t.strip()], args.body)
    elif args.cmd == "sync":
        sync()
    elif args.cmd == "search":
        search(args.query)
    elif args.cmd == "last":
        last(args.kind, args.n)


if __name__ == "__main__":
    main()
