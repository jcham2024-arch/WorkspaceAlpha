#!/usr/bin/env python3
"""Single-command pipeline runner for the baselayer workspace.

  python3 .agent/tools/run.py <command>

Commands:
  build        seed + build + validate.py
  validate     validate.py only
  categorize   categorize.py + classify_os.py (refresh master catalog)
  platforms    build_platforms.py (regen OS companions) + split pass
  provision    provision.py --profile <role> (default conceptualizer)
  sync-knowledge  knowledge.py sync (refresh DB + index)
  audit        audit.py (skill schema compliance, exit 1 on failure)

Subprocess-based; each step prints its output. Run from the
workspace root (auto-detected from this file's location).
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = sys.executable  # python3


def run(cmd, *args):
    proc = subprocess.run([PY, str(ROOT / cmd), *args], cwd=ROOT)
    return proc.returncode


COMMANDS = {
    "build": lambda a: run(".wiki/seed.py") or run(".wiki/build.py") or run("validate.py"),
    "validate": lambda a: run("validate.py"),
    "categorize": lambda a: run(".agent/tools/categorize.py") or run(".agent/tools/classify_os.py"),
    "platforms": lambda a: run(".agent/tools/build_platforms.py") or
        run(".agent/tools/split_references.py", "--min-lines", "500", "--apply"),
    "provision": lambda a: run(".harness/sync_active.py", "--profile", a.profile) or
        run(".harness/gen_skills_index.py"),
    "sync-knowledge": lambda a: run(".agent/tools/knowledge.py", "sync"),
    "audit": lambda a: run(".agent/tools/audit.py"),
}


def main():
    ap = argparse.ArgumentParser(prog="run.py")
    ap.add_argument("command", choices=sorted(COMMANDS))
    ap.add_argument("--profile", default="conceptualizer")
    args = ap.parse_args()
    rc = COMMANDS[args.command](args)
    sys.exit(rc)


if __name__ == "__main__":
    main()
