#!/usr/bin/env python3
"""Record build provenance: script hashes and output hashes.

Usage: python3 tools/record_provenance.py
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROVENANCE = ROOT / ".context" / "provenance.json"


def file_hash(path: pathlib.Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    scripts = {
        "seed.py": ROOT / ".wiki" / "seed.py",
        "build.py": ROOT / ".wiki" / "build.py",
        "validate.py": ROOT / "validate.py",
    }
    outputs = {
        "graph.json": ROOT / ".context" / "graph.json",
        "manifest.json": ROOT / ".context" / "manifest.json",
        "wiki/index.html": ROOT / ".wiki" / "index.html",
    }

    prov = {
        "script_hashes": {name: file_hash(p) for name, p in scripts.items()},
        "output_hashes": {name: file_hash(p) for name, p in outputs.items()},
        "generated_at": "2026-11-10",
    }

    PROVENANCE.parent.mkdir(parents=True, exist_ok=True)
    PROVENANCE.write_text(json.dumps(prov, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                          encoding="utf-8")
    print(f"Provenance written to {PROVENANCE}")


if __name__ == "__main__":
    main()
