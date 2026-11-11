#!/usr/bin/env python3
"""Run-log observability for agents (JSONL append + summary).

Each dispatch (manager -> implementer) or agent run records one JSON
line: timestamp, agent, profile, task summary, model tier, outcome.
Reads memory/checkpoints/ for the human resume pass; writes to
memory/runs/<date>.jsonl. Query with `summary`.

  python3 .agent/tools/run_logs.py log --agent taskmaster \
      --task "dispatch module X" --tier low-thinking --outcome ok
  python3 .agent/tools/run_logs.py summary
"""
import argparse
import datetime
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
RUNS = ROOT / "memory" / "runs"


def log(agent, task, tier="", outcome="ok", extra=None):
    RUNS.mkdir(parents=True, exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc)
    path = RUNS / f"{now.date().isoformat()}.jsonl"
    entry = {"ts": now.isoformat(), "agent": agent, "task": task,
             "tier": tier, "outcome": outcome}
    if extra:
        entry["extra"] = extra
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"logged -> {path.relative_to(ROOT)}")


def summary():
    total = 0
    by_agent = {}
    for path in sorted(RUNS.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            e = json.loads(line)
            total += 1
            a = by_agent.setdefault(e.get("agent", "?"), {"runs": 0, "ok": 0})
            a["runs"] += 1
            if e.get("outcome") == "ok":
                a["ok"] += 1
    print(f"total runs: {total}")
    for agent, v in sorted(by_agent.items()):
        print(f"  {agent}: {v['ok']}/{v['runs']} ok")


def main():
    ap = argparse.ArgumentParser(prog="run_logs.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    lp = sub.add_parser("log")
    lp.add_argument("--agent", required=True)
    lp.add_argument("--task", required=True)
    lp.add_argument("--tier", default="")
    lp.add_argument("--outcome", default="ok")
    lp.add_argument("--extra", default="")
    sub.add_parser("summary")
    args = ap.parse_args()
    if args.cmd == "log":
        log(args.agent, args.task, args.tier, args.outcome,
            json.loads(args.extra) if args.extra else None)
    else:
        summary()


if __name__ == "__main__":
    main()
