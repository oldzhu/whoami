"""Ingestion package: document parsing, semantic chunking, and local embedding."""

from .parser import DocumentParser
from .chunker import TextChunker
from .embedder import LocalEmbedder
from .pipeline import IngestionPipeline

__all__ = ["DocumentParser", "TextChunker", "LocalEmbedder", "IngestionPipeline"]
