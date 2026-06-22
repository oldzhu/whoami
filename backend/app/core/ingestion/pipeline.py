"""Ingestion pipeline orchestrator: parse → chunk → embed."""

import os
import uuid
from typing import List, Dict, Any

from .parser import DocumentParser
from .chunker import TextChunker
from .embedder import LocalEmbedder


class IngestionPipeline:
    def __init__(
        self,
        parser: DocumentParser | None = None,
        chunker: TextChunker | None = None,
        embedder: LocalEmbedder | None = None,
    ):
        self.parser = parser or DocumentParser()
        self.chunker = chunker or TextChunker()
        self.embedder = embedder or LocalEmbedder()

    def ingest_file(self, filepath: str) -> List[Dict[str, Any]]:
        text = self.parser.parse_file(filepath)
        if not text or not text.strip():
            return []

        chunks = self.chunker.chunk_text(text)
        if not chunks:
            return []

        chunk_texts = [c["text"] for c in chunks]
        embeddings = self.embedder.embed(chunk_texts)

        results: List[Dict[str, Any]] = []
        for chunk, embedding in zip(chunks, embeddings):
            results.append({
                "chunk_id": str(uuid.uuid4()),
                "text": chunk["text"],
                "embedding": embedding,
                "metadata": {
                    "start_char": chunk["metadata"]["start_char"],
                    "end_char": chunk["metadata"]["end_char"],
                    "chunk_index": chunk["metadata"]["chunk_index"],
                },
                "source_file": os.path.basename(filepath),
            })
        return results

    def ingest_directory(self, dirpath: str) -> List[Dict[str, Any]]:
        parsed = self.parser.parse_directory(dirpath)
        results: List[Dict[str, Any]] = []
        for filename, text in parsed:
            if text.startswith("[ERROR:"):
                results.append({
                    "chunk_id": str(uuid.uuid4()),
                    "text": "",
                    "embedding": [],
                    "metadata": {"error": text},
                    "source_file": filename,
                })
                continue

            if not text.strip():
                continue

            chunks = self.chunker.chunk_text(text)
            if not chunks:
                continue

            chunk_texts = [c["text"] for c in chunks]
            try:
                embeddings = self.embedder.embed(chunk_texts)
            except Exception as e:
                for chunk in chunks:
                    results.append({
                        "chunk_id": str(uuid.uuid4()),
                        "text": chunk["text"],
                        "embedding": [],
                        "metadata": {
                            **chunk["metadata"],
                            "error": str(e),
                        },
                        "source_file": filename,
                    })
                continue

            for chunk, embedding in zip(chunks, embeddings):
                results.append({
                    "chunk_id": str(uuid.uuid4()),
                    "text": chunk["text"],
                    "embedding": embedding,
                    "metadata": {
                        "start_char": chunk["metadata"]["start_char"],
                        "end_char": chunk["metadata"]["end_char"],
                        "chunk_index": chunk["metadata"]["chunk_index"],
                    },
                    "source_file": filename,
                })
        return results

    def ingest_text(self, text: str, source: str = "direct") -> List[Dict]:
        """Ingest raw text directly (no file parsing needed)."""
        chunks = self.chunker.chunk_text(text)
        results = []
        chunk_texts = [c["text"] for c in chunks]
        try:
            embeddings = self.embedder.embed(chunk_texts)
        except Exception:
            embeddings = [[] for _ in chunks]
        for i, chunk in enumerate(chunks):
            embedding = embeddings[i] if i < len(embeddings) else []
            results.append({
                "chunk_id": str(uuid.uuid4()),
                "text": chunk["text"],
                "embedding": embedding,
                "metadata": {"source": source, "chunk_index": i},
                "source_file": source,
            })
        return results
