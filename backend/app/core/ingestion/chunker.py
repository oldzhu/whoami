"""Semantic text chunker with configurable size and overlap."""

import re
from typing import List, Dict, Any, Tuple


class TextChunker:
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        if overlap >= chunk_size:
            raise ValueError(
                f"Overlap ({overlap}) must be smaller than chunk_size ({chunk_size})"
            )
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str) -> List[Dict[str, Any]]:
        if not text or not text.strip():
            return []

        segments = self._split_into_segments(text.strip())
        chunks: List[Dict[str, Any]] = []
        current_chunk = ""
        chunk_start_char = 0
        segment_boundaries: List[Tuple[int, int, str]] = []

        for seg_text, seg_start in segments:
            seg_end = seg_start + len(seg_text)
            segment_boundaries.append((seg_start, seg_end, seg_text))

        for seg_start, seg_end, seg_text in segment_boundaries:
            candidate = current_chunk + ("\n\n" if current_chunk else "") + seg_text
            if len(candidate) > self.chunk_size and current_chunk:
                chunks.append(self._build_chunk(current_chunk, chunk_start_char, len(chunks)))
                char_span = len(current_chunk)
                current_chunk = self._build_overlap_prefix(current_chunk)
                chunk_start_char = chunk_start_char + char_span - len(current_chunk)
                current_chunk = current_chunk + ("\n\n" if current_chunk else "") + seg_text
            else:
                if current_chunk:
                    current_chunk += "\n\n" + seg_text
                else:
                    current_chunk = seg_text
                    chunk_start_char = seg_start

        if current_chunk.strip():
            chunks.append(self._build_chunk(current_chunk, chunk_start_char, len(chunks)))

        return chunks

    def _split_into_segments(self, text: str) -> List[Tuple[str, int]]:
        segments: List[Tuple[str, int]] = []
        pos = 0
        for para in re.split(r"\n\s*\n", text):
            para_start = pos
            para_text = para.strip()
            if not para_text:
                pos += len(para) + 2
                continue
            if len(para_text) <= self.chunk_size:
                segments.append((para_text, text.index(para_text, para_start)))
            else:
                for sentence in self._split_sentences(para_text):
                    sent_start = text.index(sentence, para_start)
                    segments.append((sentence, sent_start))
                    para_start = sent_start + len(sentence)
            pos = para_start + len(para_text)
        return segments

    def _split_sentences(self, text: str) -> List[str]:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        result: List[str] = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            if len(sentence) > self.chunk_size:
                result.extend(self._split_words(sentence))
            else:
                result.append(sentence)
        return result

    def _split_words(self, text: str) -> List[str]:
        words = text.split()
        chunks: List[str] = []
        for i in range(0, len(words), self.chunk_size // 5):
            chunk = " ".join(words[i : i + self.chunk_size // 5])
            if chunk.strip():
                chunks.append(chunk)
        return chunks

    def _build_overlap_prefix(self, chunk: str) -> str:
        words = chunk.split()
        if len(words) <= self.overlap // 5:
            return chunk
        overlap_words = max(1, self.overlap // 5)
        return " ".join(words[-overlap_words:])

    def _build_chunk(self, text: str, start_char: int, index: int) -> Dict[str, Any]:
        return {
            "text": text,
            "metadata": {
                "start_char": start_char,
                "end_char": start_char + len(text),
                "chunk_index": index,
            },
        }
