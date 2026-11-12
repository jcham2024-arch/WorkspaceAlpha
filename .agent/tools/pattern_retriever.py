#!/usr/bin/env python3
"""Pattern Retriever — retrieves relevant skill patterns from the GPM store.

Used by orchestrators and managers to find proven skill patterns for a given
query. Only available to orchestrator and manager roles; workers are denied.

Reads `.context/pattern-memory/gpm.json` (pattern definitions) and
`.context/pattern-memory/gpm.index` (embedding index).

Stdlib only. Uses hash-based embedding for consistency with the distiller.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
GPM_PATH = ROOT / ".context" / "pattern-memory" / "gpm.json"
GPM_INDEX_PATH = ROOT / ".context" / "pattern-memory" / "gpm.index"


class PatternRetriever:
    """Retrieves relevant skill patterns from the GPM store."""

    def __init__(self):
        self.patterns: list[dict[str, Any]] = []
        self.pattern_embeddings: dict[str, list[float]] = {}
        self._load()

    def _load(self) -> None:
        """Load the GPM registry and index."""
        if GPM_PATH.exists():
            with GPM_PATH.open("r", encoding="utf-8") as f:
                data = json.load(f)
            self.patterns = data.get("patterns", [])

        if GPM_INDEX_PATH.exists():
            with GPM_INDEX_PATH.open("r", encoding="utf-8") as f:
                index_data = json.load(f)
            # The index stores pattern embeddings keyed by pattern_id
            for pattern in self.patterns:
                pid = pattern.get("pattern_id", "")
                if pid in index_data:
                    self.pattern_embeddings[pid] = index_data[pid]

    def _encode_query(self, text: str) -> list[float]:
        """Encode query text into a deterministic embedding vector.

        Uses the same hash-based embedding as the distiller for consistency.
        """
        vec = []
        for i in range(384):
            h = hashlib.sha256(f"{text}:{i}".encode("utf-8")).digest()
            val = int.from_bytes(h[i % len(h) : i % len(h) + 1], "little") / 255.0
            vec.append(val)
        return vec

    def _cosine_similarity(self, a: list[float], b: list[float]) -> float:
        """Compute cosine similarity between two vectors."""
        if not a or not b or len(a) != len(b):
            return 0.0
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(y * y for y in b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def retrieve(
        self,
        query: str,
        *,
        role: str,
        min_score: float = 0.82,
    ) -> dict[str, Any] | None:
        """Retrieve the most relevant pattern for a query.

        Args:
            query: The query string describing the task pattern.
            role: The role requesting the pattern ("conceptualizer",
                  "taskmaster", "coder", "researcher", "reviewer").
            min_score: Minimum similarity score (0.0-1.0) required.

        Returns:
            A pattern dict with keys: pattern_id, skeleton, type_signature,
            similarity_score, or None if no pattern meets the threshold.

        Raises:
            PermissionError: If the role is not authorized (only orchestrator
                and manager roles are allowed).
        """
        # Role-based access control: only orchestrator and manager roles
        allowed_roles = {"conceptualizer", "taskmaster", "research-manager", "coding-manager", "review-manager"}
        if role not in allowed_roles:
            raise PermissionError(
                f"Pattern retrieval is restricted to orchestrator/manager roles. "
                f"Role '{role}' is not authorized."
            )

        if not self.patterns:
            return None

        query_embedding = self._encode_query(query)

        best_pattern = None
        best_score = 0.0

        for pattern in self.patterns:
            pid = pattern.get("pattern_id", "")
            if pid in self.pattern_embeddings:
                pattern_embedding = self.pattern_embeddings[pid]
                score = self._cosine_similarity(query_embedding, pattern_embedding)
            else:
                # No embedding available - use text similarity on signature
                sig = pattern.get("type_signature", "")
                query_embedding_simple = self._encode_query(sig)
                pattern_embedding = self._encode_query(sig)
                score = self._cosine_similarity(query_embedding_simple, pattern_embedding)

            if score > best_score:
                best_score = score
                best_pattern = pattern

        if best_pattern is None or best_score < min_score:
            return None

        return {
            "pattern_id": best_pattern.get("pattern_id", ""),
            "skeleton": best_pattern.get("skeleton", []),
            "type_signature": best_pattern.get("type_signature", ""),
            "similarity_score": round(best_score, 3),
            "concrete_example": best_pattern.get("concrete_example", {}),
            "support_count": best_pattern.get("support_count", 0),
            "reward_score": best_pattern.get("reward_score", 0.0),
        }


def main():
    """CLI: test the pattern retriever."""
    import argparse

    ap = argparse.ArgumentParser(description="Pattern retriever test")
    ap.add_argument("query", help="Query pattern to search for")
    ap.add_argument(
        "--role",
        default="conceptualizer",
        help="Role making the request (conceptualizer, taskmaster, researcher, reviewer, etc.)",
    )
    ap.add_argument(
        "--min-score",
        type=float,
        default=0.82,
        help="Minimum similarity score (0.0-1.0)",
    )
    args = ap.parse_args()

    retriever = PatternRetriever()
    result = retriever.retrieve(args.query, role=args.role, min_score=args.min_score)

    if result:
        print(json.dumps(result, indent=2))
    else:
        print(f"No pattern found above threshold {args.min_score}")


if __name__ == "__main__":
    main()
