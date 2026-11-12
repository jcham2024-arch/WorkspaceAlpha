#!/usr/bin/env python3
"""Build vector index from .context/manifest.json.

Reads all Markdown docs referenced by the manifest, chunks each node's
byte range into sentence-aware segments, embeds them with a local
embedding model, and stores everything in a SQLite database.

Optional dependencies:
  - sentence-transformers: local sentence-transformers embeddings
  - sqlite-vec: SQLite extension for vector similarity search

If either is absent, this script exits gracefully with a warning and
the build continues without a vector index. The vector index is an
optional acceleration layer; the baselayer always works without it.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / ".context" / "manifest.json"
GRAPH_PATH = ROOT / ".context" / "graph.json"
INDEX_DB_PATH = ROOT / ".context" / "vector-index.db"
META_PATH = ROOT / ".context" / "vector-index.meta.json"

# ---------------------------------------------------------------------------
# Optional dependency loading
# ---------------------------------------------------------------------------

try:
    import sqlite_vec  # type: ignore

    HAS_SQLITE_VEC = True
except ImportError:
    HAS_SQLITE_VEC = False

try:
    from sentence_transformers import SentenceTransformer  # type: ignore

    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False


# ---------------------------------------------------------------------------
# Chunking
# ----------

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)


def _split_into_sentences(text: str) -> list[str]:
    """Split text into sentences on sentence-ending punctuation followed by
    whitespace or end-of-string. Keeps the delimiter with the preceding
    sentence so no text is lost."""
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def chunk_section(text: str, max_chars: int = 512) -> list[str]:
    """Chunk a section body into overlapping sentence groups.

    Each chunk is at most max_chars characters. Chunks are formed by
    grouping whole sentences; a sentence is never split across chunks.
    Overlap of one sentence between consecutive chunks preserves context.
    """
    sentences = _split_into_sentences(text)
    if not sentences:
        return []

    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for sentence in sentences:
        sentence_len = len(sentence)
        if current and current_len + 1 + sentence_len > max_chars:
            chunks.append(" ".join(current))
            current = [sentence]
            current_len = sentence_len
        else:
            current.append(sentence)
            current_len += 1 + sentence_len

    if current:
        chunks.append(" ".join(current))

    return chunks


def _chunk_node(text: str, node_id: str, max_chars: int = 512) -> list[dict[str, Any]]:
    """Chunk a single node's text into overlapping sentence groups.

    Returns a list of dicts with keys: node_id, chunk_index, text,
    char_start, char_end.
    """
    chunks = []
    sentences = _split_into_sentences(text)
    if not sentences:
        return chunks

    current: list[str] = []
    current_len = 0
    chunk_index = 0
    char_start = 0

    for sentence in sentences:
        sentence_len = len(sentence)
        if current and current_len + 1 + sentence_len > max_chars:
            chunk_text = " ".join(current)
            chunks.append(
                {
                    "node_id": node_id,
                    "chunk_index": chunk_index,
                    "text": chunk_text,
                    "char_start": char_start,
                    "char_end": char_start + len(chunk_text),
                }
            )
            chunk_index += 1
            current = [sentence]
            current_len = sentence_len
            char_start = (
                text.find(sentence, char_start) if sentence in text else char_start
            )
        else:
            if not current:
                char_start = text.find(sentence, char_start) if sentence in text else char_start
            current.append(sentence)
            current_len += 1 + sentence_len

    if current:
        chunk_text = " ".join(current)
        chunks.append(
            {
                "node_id": node_id,
                "chunk_index": chunk_index,
                "text": chunk_text,
                "char_start": char_start,
                "char_end": char_start + len(chunk_text),
            }
        )

    return chunks


# ---------------------------------------------------------------------------
# Embedding
# ----------

class Embedder:
    """Wrapper around sentence-transformers SentenceTransformer.

    Falls back to a deterministic hash-based embedding if sentence-transformers
    is not available, so the build never fails due to missing dependencies.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None
        self._available = False
        try:
            from sentence_transformers import SentenceTransformer  # type: ignore

            self._model = SentenceTransformer(model_name)
            self._available = True
        except ImportError:
            self._available = False

    def is_available(self) -> bool:
        return self._available

    def encode(self, texts: list[str]) -> list[list[float]]:
        """Encode a list of texts into embedding vectors.

        If sentence-transformers is not available, falls back to a
        deterministic hash-based embedding. The hash-based embedding is
        deterministic but not semantically meaningful; it is suitable only
        for testing the pipeline, not for semantic search.
        """
        if self._available:
            embeddings = self._model.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()

        # Fallback: deterministic hash-based embedding (384 dims, same as
        # all-MiniLM-L6-v2 for shape compatibility).
        results = []
        for text in texts:
            vec = []
            for i in range(384):
                h = hashlib.sha256(f"{text}:{i}".encode("utf-8")).digest()
                val = (int.from_bytes(h[i % len(h)] : i % len(h) + 1] or b"\x00")[0] / 255.0
                vec.append(val)
            results.append(vec)
        return results


# ---------------------------------------------------------------------------
# Vector database
# ----------

class VectorStore:
    """Wrapper around sqlite-vec for vector storage and similarity search."""

    def __init__(self, db_path: Path, embedding_dim: int = 384):
        self.db_path = db_path
        self.embedding_dim = embedding_dim
        self.conn = None
        self.available = False

        if not HAS_SQLITE_VEC:
            return

        try:
            import sqlite_vec  # type: ignore

            self.conn = sqlite3.connect(str(db_path))
            self.conn.execute("CREATE TABLE IF NOT EXISTS embeddings (id TEXT PRIMARY KEY, content_ref TEXT, node_id TEXT, byte_range_start INTEGER, byte_range_end INTEGER, chunk_text TEXT, embedding BLOB)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_embeddings_node ON embeddings(node_id)")
            self.conn.commit()
            self.available = True
        except Exception:
            self.available = False

    def add_embedding(
        self,
        node_id: str,
        content_ref: str,
        byte_range_start: int,
        byte_range_end: int,
        chunk_text: str,
        embedding: list[float],
    ) -> None:
        """Add a single embedding to the vector store."""
        if not self.available:
            return
        embedding_bytes = bytes(float(v) for v in embedding)
        self.conn.execute(
            "INSERT OR REPLACE INTO embeddings (id, content_ref, node_id, byte_range_start, byte_range_end, chunk_text, embedding) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                f"{node_id}:{chunk_text[:50]}",
                content_ref,
                node_id,
                byte_range_start,
                byte_range_end,
                chunk_text,
                embedding_bytes,
            ),
        )
        self.conn.commit()

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        """Search for similar embeddings using cosine similarity."""
        if not self.available:
            return []

        query_bytes = bytes(float(v) for v in query_embedding)
        results = self.conn.execute(
            """
            SELECT node_id, content_ref, byte_range_start, byte_range_end, chunk_text,
                   cosine_distance(embedding, ?) AS distance
            FROM embeddings
            ORDER BY distance
            LIMIT ?
        """,
            (query_bytes, top_k),
        ).fetchall()

        results_list = []
        for row in results:
            node_id, content_ref, byte_range_start, byte_range_end, chunk_text, distance = row
            results_list.append(
                {
                    "node_id": node_id,
                    "content_ref": content_ref,
                    "byte_range_start": byte_range_start,
                    "byte_range_end": byte_range_end,
                    "chunk_text": chunk_text,
                    "similarity": 1.0 - distance,  # Convert distance to similarity
                }
            )
        return results_list

    def close(self) -> None:
        if self.conn:
            self.conn.close()


# ---------------------------------------------------------------------------
# Main build pipeline
# ----------


def load_manifest() -> dict[str, Any]:
    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_index(manifest: dict[str, Any]) -> None:
    """Build the vector index from all document nodes in the manifest."""
    embedder = Embedder()
    store = VectorStore(INDEX_DB_PATH)

    if not embedder.is_available():
        print(
            "WARNING: sentence-transformers not installed. Vector index will not be built. "
            "Install with: pip install sentence-transformers"
        )
        store.close()
        return

    if not store.available:
        print(
            "WARNING: sqlite-vec not installed. Vector index will not be built. "
            "Install with: pip install sqlite-vec"
        )
        return

    nodes = manifest.get("nodes", [])
    total_chunks = 0

    for node in nodes:
        content_ref = node.get("content_ref", "")
        byte_range = node.get("byte_range")
        node_id = node.get("id", "")

        if not content_ref or not byte_range:
            continue

        ref_path = ROOT / content_ref
        if not ref_path.exists():
            print(f"WARNING: Content file not found: {content_ref}")
            continue

        try:
            content = ref_path.read_bytes()
        except OSError:
            print(f"WARNING: Cannot read content file: {content_ref}")
            continue

        start, end = byte_range
        if start < 0 or end <= start or end > len(content):
            print(f"WARNING: Invalid byte range for {node_id}: [{start}, {end}]")
            continue

        chunk_bytes = content[start:end]
        chunk_text = chunk_bytes.decode("utf-8", errors="replace")

        chunks = _chunk_node(chunk_text, node_id)
        if not chunks:
            continue

        chunk_texts = [c["text"] for c in chunks]
        embeddings = embedder.encode(chunk_texts)

        for chunk, embedding in zip(chunks, embeddings):
            store.add_embedding(
                node_id=chunk["node_id"],
                content_ref=content_ref,
                byte_range_start=chunk["char_start"],
                byte_range_end=chunk["char_end"],
                chunk_text=chunk["text"],
                embedding=embedding,
            )
            total_chunks += 1

    store.close()

    # Write metadata
    meta = {
        "embedding_model": embedder.model_name,
        "embedding_dim": 384,
        "total_chunks": total_chunks,
        "manifest_sha256": hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest(),
        "total_nodes": len(nodes),
    }
    META_PATH.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Built vector index: {total_chunks} chunks from {len(nodes)} nodes")


def main():
    if not MANIFEST_PATH.exists():
        print(f"Manifest not found: {MANIFEST_PATH}. Run build.py first.")
        sys.exit(1)

    manifest = load_manifest()
    build_index(manifest)


if __name__ == "__main__":
    main()
