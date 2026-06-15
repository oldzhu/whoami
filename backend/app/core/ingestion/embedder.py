"""Local embedding generator using sentence-transformers."""

from typing import List


class LocalEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", batch_size: int = 32):
        self.model_name = model_name
        self.batch_size = batch_size
        self._model = None

    @property
    def model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError:
                raise ImportError(
                    "sentence-transformers is not installed. "
                    "Install it: pip install sentence-transformers"
                )
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def embed(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        non_empty = [t for t in texts if t and t.strip()]
        if not non_empty:
            return [[0.0] * self._dim()] * len(texts)

        embeddings = []
        for i in range(0, len(non_empty), self.batch_size):
            batch = non_empty[i : i + self.batch_size]
            batch_embeddings = self.model.encode(
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
                result.append([0.0] * self._dim())
        return result

    def embed_query(self, text: str) -> List[float]:
        if not text or not text.strip():
            return [0.0] * self._dim()
        embedding = self.model.encode(
            [text], convert_to_numpy=True, show_progress_bar=False
        )
        return embedding[0].tolist()

    def _dim(self) -> int:
        return self.model.get_sentence_embedding_dimension()
