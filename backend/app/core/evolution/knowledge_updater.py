"""Apply approved facts to the knowledge base."""
import logging
from .review_queue import ReviewQueue
from ..storage.vector_store import VectorStore
from ..storage.graph_store import GraphStore
from ..ingestion.embedder import LocalEmbedder

logger = logging.getLogger(__name__)


class KnowledgeUpdater:
    """Applies reviewed and approved facts to vector and graph stores."""

    def __init__(self):
        self.review_queue = ReviewQueue()
        self.vector_store = VectorStore()
        self.graph_store = GraphStore()
        self.embedder = LocalEmbedder()

    def apply_approved(self) -> dict:
        approved = self.review_queue.get_approved()
        if not approved:
            return {"applied": 0}

        texts = [f["content"] for f in approved]
        embeddings = [self.embedder.embed_query(t) for t in texts]
        metadatas = [
            {"source": "evolution", "fact_type": f["fact_type"]}
            for f in approved
        ]

        self.vector_store.create_collection("knowledge_base")
        self.vector_store.add_documents(
            "knowledge_base", texts, embeddings, metadatas
        )

        logger.info(f"Applied {len(approved)} facts to knowledge base")
        return {"applied": len(approved)}
