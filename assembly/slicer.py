#!/usr/bin/env python3
"""Slicer — extracts exact byte-range slices from manifest nodes.

Read-only consumer of the manifest. Given a node ID and byte_range, returns
the exact slice with sha256 verification. Raises SliceOutOfBounds if the
range is malformed or outside file bounds.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / ".context" / "manifest.json"


class SliceOutOfBounds(Exception):
    """Raised when a byte_range is malformed or exceeds file bounds."""
    pass


class Slicer:
    """Reads exact byte ranges from manifest nodes with sha256 verification."""

    def __init__(self):
        self._manifest = None
        self._nodes = None

    def _load_manifest(self):
        if self._manifest is None:
            if not MANIFEST_PATH.exists():
                raise FileNotFoundError(
                    f"missing {MANIFEST_PATH.relative_to(ROOT)} — run python3 build.py first"
                )
            with MANIFEST_PATH.open("r", encoding="utf-8") as f:
                self._manifest = json.load(f)
            self._nodes = {n["id"]: n for n in self._manifest.get("nodes", [])}
        return self._manifest, self._nodes

    def slice_node(self, node_id: str) -> bytes:
        """Return the exact byte slice for a manifest node, with sha256 verification.

        Raises SliceOutOfBounds if:
        - node_id not found in manifest
        - byte_range is missing or malformed (start < 0, end <= start, end > file size)
        - sha256 verification fails (manifest corrupted)
        """
        self._load_manifest()
        node = self._nodes.get(node_id)
        if node is None:
            raise SliceOutOfBounds(f"unknown node: {node_id}")

        content_ref = node.get("content_ref", "")
        byte_range = node.get("byte_range")
        expected_sha = node.get("sha256")

        if byte_range is None:
            raise SliceOutOfBounds(f"node {node_id} has no byte_range")

        start, end = byte_range
        if start < 0:
            raise SliceOutOfBounds(
                f"node {node_id}: byte_range start {start} is negative"
            )
        if end <= start:
            raise SliceOutOfBounds(
                f"node {node_id}: byte_range end {end} <= start {start}"
            )

        file_path = ROOT / content_ref
        if not file_path.exists():
            raise SliceOutOfBounds(
                f"node {node_id}: content file missing: {content_ref}"
            )

        data = file_path.read_bytes()
        if end > len(data):
            raise SliceOutOfBounds(
                f"node {node_id}: byte_range end {end} exceeds file size {len(data)}"
            )

        chunk = data[start:end]

        # Verify sha256
        actual_sha = hashlib.sha256(chunk).hexdigest()
        if expected_sha and actual_sha != expected_sha:
            raise SliceOutOfBounds(
                f"node {node_id}: sha256 mismatch — expected {expected_sha}, got {actual_sha}"
            )

        return chunk

    def slice_node_text(self, node_id: str) -> str:
        """Return the byte slice decoded as UTF-8 text."""
        chunk = self.slice_node(node_id)
        return chunk.decode("utf-8", errors="replace")

    def estimate_tokens(self, node_id: str) -> int:
        """Return the estimated token count for a node (bytes // 4)."""
        self._load_manifest()
        node = self._nodes.get(node_id)
        if node is None:
            return 0
        return node.get("est_tokens", 0)


def main():
    """CLI: slice a manifest node and print the result."""
    import argparse

    ap = argparse.ArgumentParser(description="Slice a manifest node by byte range")
    ap.add_argument("node_id", help="Manifest node ID")
    args = ap.parse_args()

    slicer = Slicer()
    try:
        chunk = slicer.slice_node(args.node_id)
        sys.stdout.buffer.write(chunk)
    except SliceOutOfBounds as exc:
        print(f"SLICE OUT OF BOUNDS: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
