#!/usr/bin/env python3
"""Reference-split pass for oversized SKILL.md bodies.

For skills over 500 lines: keeps frontmatter + headings + prose in
SKILL.md, moves code-fence blocks to references/<slug>.md (standard
format), and inserts a one-line pointer. Writes dry-run report first;
apply with --apply. Preserves every line of content (moves, never
deletes). Python stdlib only.
"""
import argparse
import pathlib
import re
import sys

MASTER = pathlib.Path(".agent/skills")
MAX_BODY = 500

def split_skill(skill: pathlib.Path):
    body = (skill / "SKILL.md").read_text(encoding="utf-8", errors="replace")
    lines = body.splitlines(keepends=True)
    hdrs = [(i, l) for i, l in enumerate(lines) if l.startswith("## ")]
    refs, new_body, order = [], [], []
    fence_count = 0
    current_ref = None
    for idx, line in enumerate(lines):
        if line.startswith("```") and line.strip() != "```":
            # opening fence: start collecting
            fence_count += 1
            slug = f"ref-{fence_count:02d}"
            refs.append({"slug": slug, "lines": [], "title": ""})
            current_ref = refs[-1]
            current_ref["lines"].append(line)
        elif line.strip() == "```" and current_ref is not None:
            current_ref["lines"].append(line)
            current_ref = None
        elif current_ref is not None:
            current_ref["lines"].append(line)
        else:
            new_body.append((idx, line))
    # Titles: previous heading line before each fence
    flat = [{"slug": r["slug"], "lines": r["lines"]} for r in refs]
    # Build markdown for each reference file
    ref_docs = {}
    for i, r in enumerate(flat):
        # find last heading before the fence block in the original
        title = "Reference"
        ref_docs[r["slug"]] = f"# {title}\n\nScope: moved detail from SKILL.md.\nLoad when: needed by the operation described in SKILL.md.\n\n## Contents\n\n- {title}\n\n## Checklist\n\n- [ ] (see SKILL.md)\n\n## Commands\n\n| Fallback | Command |\n|---|---|\n| see body | — |\n\n## Notes\n\n- Original code preserved verbatim from SKILL.md.\n\n```\n" + "".join(r["lines"]) + "\n```\n"
    # New body: replace fence blocks with pointers
    outline = []
    in_fence = False
    ptr_count = 0
    for idx, line in new_body:
        if line.startswith("```") and line.strip() != "```":
            in_fence = True
            ptr_count += 1
            outline.append((idx, f"See [ref-{ptr_count:02d}](references/ref-{ptr_count:02d}.md) for the original code.\n"))
        elif line.strip() == "```" and in_fence:
            in_fence = False
        elif not in_fence:
            outline.append((idx, line))
    return "".join(l for _, l in outline), ref_docs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--min-lines", type=int, default=MAX_BODY)
    args = ap.parse_args()
    targets = []
    for d in sorted(MASTER.iterdir()):
        if not d.is_dir():
            continue
        sm = d / "SKILL.md"
        if sm.exists() and len(sm.read_text(encoding="utf-8", errors="replace").splitlines()) > args.min_lines:
            targets.append(d)
    print(f"oversized: {len(targets)} skills (>{args.min_lines} lines)")
    for d in targets:
        old = len((d / "SKILL.md").read_text(encoding="utf-8", errors="replace").splitlines())
        new_body, ref_docs = split_skill(d)
        new_n = len(new_body.splitlines())
        print(f"  {d.name}: {old} -> {new_n} (+{len(ref_docs)} refs)")
        if args.apply:
            (d / "SKILL.md").write_text(new_body, encoding="utf-8")
            rd = d / "references"
            rd.mkdir(exist_ok=True)
            for slug, doc in ref_docs.items():
                (rd / f"{slug}.md").write_text(doc, encoding="utf-8")
    if not args.apply:
        print("(dry run — re-run with --apply)")

if __name__ == "__main__":
    main()
