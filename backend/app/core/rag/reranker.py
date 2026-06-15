"""Cross-encoder reranker for improving retrieval quality."""

from typing import Any, Dict, List


class Reranker:
    """Re-ranks retrieval results using cross-attention scoring.

    For MVP, uses heuristic scoring based on term overlap.
    Can be upgraded to a cross-encoder model (e.g. sentence-transformers).
    """

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        self._model = None

    def rerank(
        self, query: str, results: List[Dict[str, Any]], top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """Re-rank results by query-text term overlap and original score."""
        query_lower = query.lower()
        query_terms = set(query_lower.split())

        for r in results:
            text = r.get("text", "").lower()
            text_terms = set(text.split())
            overlap = len(query_terms & text_terms)
            r["rerank_score"] = r.get("score", 0) * 0.5 + overlap * 0.5

        results.sort(key=lambda x: x.get("rerank_score", 0), reverse=True)
        return results[:top_k]
