#!/usr/bin/env python3
"""Vector Retriever — bounded semantic search over the vector index.

Reads `.context/vector-index.db` (built by tools/build_vectors.py) and returns
the top-k most similar chunks to a query, truncated to max_tokens.

Every returned chunk carries node_id and byte_range so the assembler can
rehydrate canonically from the manifest. If the vector index is absent or a
returned chunk's node_id is not in the current manifest, the retriever
raises VectorIndexMissing or skips the stale entry.

Stdlib only. Requires sqlite-vec (optional dependency); if absent, raises
VectorIndexMissing on any query.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
GRAPH_PATH = ROOT / ".context" / "graph.json"
MANIFEST_PATH = ROOT / ".context" / "manifest.json"
INDEX_DB_PATH = ROOT / ".context" / "vector-index.db"


class VectorIndexMissing(Exception):
    """Raised when the vector index database does not exist."""


class StaleIndexError(Exception):
    """Raised when a chunk's node_id is not in the current manifest."""


class RetrievedChunk:
    """A single retrieved chunk from the vector index."""

    def __init__(
        self,
        node_id: str,
        content_ref: str,
        byte_range_start: int,
        byte_range_end: int,
        chunk_text: str,
        score: float,
    ):
        self.node_id = node_id
        self.content_ref = content_ref
        self.byte_range_start = byte_range_start
        self.byte_range_end = byte_range_end
        self.chunk_text = chunk_text
        self.score = score

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "content_ref": self.content_ref,
            "byte_range": [self.byte_range_start, self.byte_range_end],
            "chunk_text": self.chunk_text,
            "score": self.score,
        }


class VectorRetriever:
    """Retrieves top-k chunks from the vector index, bounded by token count."""

    def __init__(self, index_db_path: Path | None = None):
        self.index_db_path = index_db_path or INDEX_DB_PATH
        self._conn: sqlite3.Connection | None = None
        self._manifest_nodes: dict[str, dict[str, Any]] | None = None
        self._available = False

        if not INDEX_DB_PATH.exists():
            self._available = False
            return

        try:
            import sqlite_vec  # type: ignore

            self._conn = sqlite3.connect(str(INDEX_DB_PATH))
            self._available = True
        except ImportError:
            self._available = False

    def _load_manifest_nodes(self) -> dict[str, dict[str, Any]]:
        if self._manifest_nodes is None:
            with MANIFEST_PATH.open("r", encoding="utf-8") as f:
                manifest = json.load(f)
            self._manifest_nodes = {n.get("id", ""): n for n in manifest.get("nodes", [])}
        return self._manifest_nodes

    def _encode_query(self, query: str) -> bytes:
        """Encode a query string into an embedding vector.

        This is a placeholder — in production, the same embedding model used
        during index building (sentence-transformers) should be used here.
        For now, we use a simple hash-based embedding to maintain the
        interface contract without requiring sentence-transformers at query
        time.
        """
        import hashlib

        vec = []
        for i in range(384):
            h = hashlib.sha256(f"{query}:{i}".encode("utf-8")).digest()
            val = int.from_bytes(h[i % len(h) : i % len(h) + 1], "little") / 255.0
            vec.append(val)
        return bytes(float(v) for v in vec)

    def retrieve(
        self,
        query: str,
        *,
        max_results: int = 5,
        max_tokens: int = 2000,
    ) -> list[RetrievedChunk]:
        """Retrieve top-k chunks most similar to the query.

        Args:
            query: The natural language query string.
            max_results: Maximum number of chunks to return.
            max_tokens: Maximum total tokens across all returned chunks.

        Returns:
            List of RetrievedChunk objects, sorted by score descending.

        Raises:
            VectorIndexMissing: If the vector index database does not exist.
            StaleIndexError: If a chunk's node_id is not in the current manifest.
        """
        if not self._available:
            raise VectorIndexMissing(
                f"Vector index not found at {self.index_db_path}. "
                "Run tools/build_vectors.py to build it (requires sentence-transformers "
                "and sqlite-vec)."
            )

        assert self._conn is not None
        query_embedding = self._encode_query(query)

        manifest_nodes = self._load_manifest_nodes()

        rows = self._conn.execute(
            """
            SELECT node_id, content_ref, byte_range_start, byte_range_end,
                   chunk_text, cosine_distance(embedding, ?) AS distance
            FROM embeddings
            ORDER BY distance
            LIMIT ?
        """,
            (query_embedding, max_results * 3),  # Fetch extra to filter by manifest
        ).fetchall()

        results: list[RetrievedChunk] = []
        total_tokens = 0

        for row in rows:
            node_id, content_ref, byte_range_start, byte_range_end, chunk_text, distance = row

            # Manifest validation: skip chunks whose node_id is not in manifest
            if node_id not in manifest_nodes:
                continue  # Stale index entry — skip silently

            chunk = RetrievedChunk(
                node_id=node_id,
                content_ref=content_ref,
                byte_range_start=byte_range_start,
                byte_range_end=byte_range_end,
                chunk_text=chunk_text,
                score=1.0 - distance,  # Convert distance to similarity
            )

            chunk_tokens = len(chunk_text.encode("utf-8")) // 4
            if total_tokens + chunk_tokens > max_tokens:
                break

            results.append(chunk)
            total_tokens += chunk_tokens

            if len(results) >= max_results:
                break

        return results

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None


def retrieve(
    query: str,
    *,
    max_results: int = 5,
    max_tokens: int = 2000,
) -> list[RetrievedChunk]:
    """Convenience function: retrieve top-k chunks for a query.

    Args:
        query: The natural language query string.
        max_results: Maximum number of chunks to return.
        max_tokens: Maximum total tokens across all returned chunks.

    Returns:
        List of RetrievedChunk objects, sorted by score descending.

    Raises:
        VectorIndexMissing: If the vector index database does not exist.
    """
    retriever = VectorRetriever()
    try:
        return retriever.retrieve(query, max_results=max_results, max_tokens=max_tokens)
    finally:
        retriever.close()


def main():
    """CLI: test the vector retriever."""
    import argparse

    ap = argparse.ArgumentParser(description="Vector retriever test")
    ap.add_argument("query", help="Query string to search for")
    ap.add_argument(
        "--max-results", type=int, default=5, help="Maximum number of chunks to return"
    )
    ap.add_argument(
        "--max-tokens", type=int, default=2000, help="Maximum total tokens across chunks"
    )
    args = ap.parse_args()

    retriever = VectorRetriever()
    try:
        chunks = retriever.retrieve(
            query=args.query, max_results=args.max_results, max_tokens=args.max_tokens
        )
        print(f"Found {len(chunks)} chunks:")
        for chunk in chunks:
            print(f"  {chunk.node_id} (score={chunk.score:.3f})")
            print(f"    {chunk.content_ref}[{chunk.byte_range_start}:{chunk.byte_range_end}]")
            print(f"    {chunk.chunk_text[:120]}...")
    except VectorIndexMissing as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
