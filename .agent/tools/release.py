#!/usr/bin/env python3
"""Versioned factory release pipeline (validate -> audit -> regenerate -> tag).

  python3 .agent/tools/release.py --check      # dry-run: validate, print state
  python3 .agent/tools/release.py              # full: validate, regenerate
                                               # (registry + cards), snapshot,
                                               # and write the release manifest

A release snapshots the CURRENT factory state (.agent/agents.json,
.agent/agent-cards.json, CATEGORIZATION counts, skill/profile tallies)
under .agent/releases/<version>/. Raw .agent files are never committed;
the snapshot manifest is what a git tag points at.
"""
import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
PY = sys.executable


def run(cmd, *args):
    proc = subprocess.run([PY, str(ROOT / cmd), *args], cwd=ROOT, capture_output=True, text=True)
    print(proc.stdout.strip())
    if proc.stderr.strip():
        print(proc.stderr.strip())
    return proc.returncode


def main():
    ap = argparse.ArgumentParser(prog="release.py")
    ap.add_argument("--check", action="store_true", help="dry-run: validate only")
    args = ap.parse_args()

    if run("validate.py") != 0:
        sys.exit("release aborted: validation failed")
    if args.check:
        print("release CHECK passed (validate + state printed below)")
        print("would release:", factory_version())
        return

    if run(".agent/tools/audit.py") != 0:
        sys.exit("release aborted: audit found failures")
    if run(".agent/tools/registry.py") != 0:
        sys.exit("regeneration failed")
    if run(".agent/tools/agent_cards.py") != 0:
        sys.exit("cards generation failed")

    version = factory_version()
    out_dir = ROOT / ".agent" / "releases" / version
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "version": version,
        "registry_agents": count_registry_agents(),
        "cards": count_cards(),
        "master_skills": count_master_skills(),
        "generated_by": ".agent/tools/release.py",
        "note": "snapshot references the live .agent files; tag this version in git for permanence.",
    }
    (out_dir / "RELEASE.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"released v{version} (snapshot: {out_dir.relative_to(ROOT)}/RELEASE.json)")


def factory_version():
    data = json.loads((ROOT / ".agent" / "models.json").read_text(encoding="utf-8"))
    return data.get("version", "0.1.0")


def count_registry_agents():
    return len(json.loads((ROOT / ".agent" / "agents.json").read_text(encoding="utf-8"))["agents"])


def count_cards():
    return len(json.loads((ROOT / ".agent" / "agent-cards.json").read_text(encoding="utf-8"))["cards"])


def count_master_skills():
    return sum(1 for d in (ROOT / ".agent" / "skills").iterdir() if d.is_dir() and (d / "SKILL.md").exists())


if __name__ == "__main__":
    main()
