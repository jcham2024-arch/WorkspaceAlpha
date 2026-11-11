#!/usr/bin/env python3
"""Provision shim — the real sync is the harness bridge (.harness/sync_active.py).

Agent-facing entry point for profile provisioning. Forwards argv to
the harness-owned bridge (the one explicit peer call between the
agent system and the harness runtime).
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if __name__ == "__main__":
    sys.exit(subprocess.run([sys.executable, str(ROOT / ".harness" / "sync_active.py"), *sys.argv[1:]], cwd=ROOT).returncode)
