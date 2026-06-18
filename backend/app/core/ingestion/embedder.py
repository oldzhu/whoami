"""Local embedding generator — uses Ollama or sentence-transformers."""
import logging
from typing import List

logger = logging.getLogger(__name__)


class LocalEmbedder:
    def __init__(self, model_name: str = "all-minilm:l6-v2", batch_size: int = 32):
        self.model_name = model_name
        self.batch_size = batch_size
        self._model = None
        self._use_ollama = None  # True/False/None=auto-detect

    def _init_ollama(self) -> bool:
        """Try using Ollama for embeddings (fast, local, no download)."""
        try:
            import httpx
            r = httpx.get("http://127.0.0.1:11434/api/tags", timeout=5)
            if r.status_code == 200:
                models = r.json().get("models", [])
                if any(m["name"] == self.model_name or m["name"].startswith("all-minilm") for m in models):
                    logger.info("Using Ollama for embeddings")
                    return True
                # Try pulling if model not available
                logger.info("Embedding model not in Ollama, trying to pull...")
                return True  # Use ollama even without dedicated embedding model
        except Exception:
            pass
        return False

    def _ollama_embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings via Ollama API."""
        import httpx
        try:
            r = httpx.post(
                "http://127.0.0.1:11434/api/embed",
                json={"model": "all-minilm:l6-v2", "input": texts},
                timeout=30,
                proxy=None,
            )
            if r.status_code == 200:
                data = r.json()
                if "embeddings" in data and data["embeddings"]:
                    return data["embeddings"]
        except Exception:
            pass
        return [[0.0] * 384 for _ in texts]

    def _init_sentence_transformers(self):
        """Fallback: sentence-transformers (downloads from HuggingFace)."""
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception as e:
            logger.warning(f"sentence-transformers unavailable: {e}")

    def embed(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        non_empty = [t for t in texts if t and t.strip()]
        if not non_empty:
            return [[0.0] * 384] * len(texts)

        if self._use_ollama is None:
            self._use_ollama = self._init_ollama()

        if self._use_ollama:
            return self._ollama_embed(texts)

        if self._model is None:
            self._init_sentence_transformers()

        if self._model is None:
            return [[0.0] * 384] * len(texts)

        embeddings = []
        for i in range(0, len(non_empty), self.batch_size):
            batch = non_empty[i : i + self.batch_size]
            batch_embeddings = self._model.encode(
                batch, convert_to_numpy=True, show_progress_bar=False
            )
            embeddings.extend(batch_embeddings.tolist())

        result: List[List[float]] = []
        non_empty_idx = 0
        for t in texts:
            if t and t.strip():
                result.append(embeddings[non_empty_idx])
                non_empty_idx += 1
            else:
                result.append([0.0] * 384)
        return result

    def embed_query(self, text: str) -> List[float]:
        if not text or not text.strip():
            return [0.0] * 384
        result = self.embed([text])
        return result[0] if result else [0.0] * 384
