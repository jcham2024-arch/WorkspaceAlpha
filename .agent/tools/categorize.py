#!/usr/bin/env python3
"""Categorize every master skill into task type / subtype / workflow level.

Reads .agent/skills/*/SKILL.md frontmatter (name, description) and
applies an ordered rule set. Manager-leaning skills (plan/review/
orchestrate) go to manager level; execution skills go to worker.
Outputs .agent/skills/CATEGORIZATION.md (tallies) + CATEGORIZATION.csv
(1 row per skill with its category, subtype, and level).
"""
import csv
import pathlib
import re

MASTER = pathlib.Path(".agent/skills")

# Ordered rules: (task_type, [keywords], subtype)
TYPE_RULES = [
    ("project-mgmt", ["project", "task", "todo", "kanban", "scrum", "agile", "sprint", "milestone", "objective", "goal-chasing"], None),
    ("writing-content", ["write", "story", "narrative", "copy", "blog", "article", "content", "script-writing", "essay", "book", "translat", "literary"], None),
    ("media-video", ["video", "youtube", "animation", "audio", "music", "image", "picture", "thumbnail", "voiceover", "podcast", "tts", "subtitle"], None),
    ("design-ui", ["ui", "ux", "design", "figma", "layout", "typography", "color", "branding", "logo", "wireframe", "mockup"], None),
    ("frontend-web", ["html", "css", "javascript", "typescript", "react", "vue", "angular", "web", "frontend", "browser", "tailwind", "dom"], None),
    ("backend-systems", ["java", "python", "php", "go", "rust", "backend", "api", "database", "sql", "graphql", "node", "server", "refactor"], None),
    ("devops-infra", ["docker", "kubernetes", "k8s", "ci/cd", "deployment", "terraform", "aws", "cloud", "infrastructure", "linux", "devops"], None),
    ("data-ai", ["machine", "ml", "ai", "llm", "rag", "model", "data", "embedding", "prompt", "agent", "neural", "deep learning"], None),
    ("security", ["security", "pentest", "vulnerability", "exploit", "fuzzing", "hacking", "reverse", "threat", "malware", "xss"], None),
    ("testing-debug", ["debug", "test", "qa", "benchmark", "profil", "monitor", "observability", "logging", "tracing"], None),
    ("research", ["research", "search", "scrap", "extract", "web", "patent", "competitor", "market"], None),
    ("automation", ["automation", "workflow", "script", "cron", "pipeline", "integration", "mcp", "tool", "bot"], None),
    ("business", ["marketing", "sales", "legal", "finance", "business", "product", "growth", "seo", "crm", "pricing"], None),
    ("docs", ["document", "readme", "specification", "api-doc", "guide", "manual", "adr", "wiki"], None),
]

# Subtype refinement (picks the most specific substring among matches)
SUBTYPE_RULES = [
    ("video", ["video", "youtube"]),
    ("story-script", ["story", "script-writing", "narrative"]),
    ("api-design", ["api"]),
    ("html", ["html"]),
    ("css", ["css"]),
    ("javascript", ["javascript"]),
    ("typescript", ["typescript"]),
    ("java", ["java"]),
    ("python", ["python"]),
    ("php", ["php"]),
    ("devops", ["docker", "kubernetes", "ci/cd", "terraform", "deployment"]),
    ("security-offensive", ["pentest", "exploit", "fuzzing", "hacking", "reverse"]),
]

LEVEL_RULES = [
    "plan", "review", "audit", "strateg", "orchestrat", "manage",
    "organize", "triage", "priorit", "decis", "specif", "architect",
    "route", "delegat", "coordinate", "monitor", "govern",
]

def frontmatter(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    out = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip().strip("'\"")
    return out

def categorize(name, desc):
    text = f"{name} {desc}".lower()
    task = "general"
    for t, kws, _ in TYPE_RULES:
        if any(kw in text for kw in kws):
            task = t
            break
    sub = None
    for s, kws in SUBTYPE_RULES:
        if any(kw in text for kw in kws):
            sub = s
            break
    if sub is None:
        sub = task if task != "general" else "general"
    level = "manager" if any(kw in text for kw in LEVEL_RULES) else "worker"
    return task, sub, level

def main():
    rows = []
    for d in sorted(MASTER.iterdir()):
        if not d.is_dir():
            continue
        fm_path = d / "SKILL.md"
        if not fm_path.exists():
            continue
        fm = frontmatter(fm_path)
        name = fm.get("name", d.name)
        desc = fm.get("description", "")[:300]
        task, sub, level = categorize(name, desc)
        rows.append([name, task, sub, level, d.name, desc])
    with open(MASTER / "CATEGORIZATION.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["skill", "task_type", "subtype", "level", "folder", "description"])
        w.writerows(rows)
    from collections import Counter
    tc = Counter(r[1] for r in rows)
    sc = Counter((r[1], r[2]) for r in rows)
    lc = Counter(r[3] for r in rows)
    with open(MASTER / "CATEGORIZATION.md", "w", encoding="utf-8") as f:
        f.write("# Master Skill Categorization (rule-based)\n\n")
        f.write("Task types and subtypes for all 3,520 master skills "
                "(auto-classified from name + description; re-run "
                ".agent/tools/categorize.py to regenerate).\n\n")
        f.write("## Task-type tally\n\n")
        for t, n in tc.most_common():
            f.write(f"- {t}: {n}\n")
        f.write("\n## Subtypes (top 25)\n\n")
        for (t, s), n in sc.most_common(25):
            f.write(f"- {t}/{s}: {n}\n")
        f.write(f"\n## Levels\n\n- manager: {lc.get('manager', 0)}\n- worker: {lc.get('worker', 0)}\n")
        f.write("\n## Per-agent scoping\n\n")
        f.write("Profiles provision by category + level, not whole library:\n")
        f.write("- conceptualizer: project-mgmt/worker + writing-content/worker (scope)\n")
        f.write("- taskmaster: project-mgmt/manager + automation/worker (dispatch)\n")
        f.write("- coding-manager: backend-systems + frontend-web / worker (steps)\n")
        f.write("- research-manager: research / worker (steps)\n")
        f.write("- review-manager: testing-debug + security / manager (checks)\n")
    print(f"categorized {len(rows)} skills: task types={len(tc)}, levels={dict(lc)}")

if __name__ == "__main__":
    main()
