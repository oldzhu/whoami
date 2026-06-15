"""ChromaDB vector store integration."""

import uuid
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.config import Settings


class VectorStore:
    """Persistent vector store using ChromaDB."""

    def __init__(self, persist_dir: str = "data/chroma"):
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False),
        )

    def create_collection(self, name: str) -> None:
        try:
            self.client.create_collection(name=name)
        except Exception:
            pass

    def get_collection(self, name: str):
        return self.client.get_collection(name=name)

    def list_collections(self) -> List[str]:
        return [c.name for c in self.client.list_collections()]

    def add_documents(
        self,
        collection_name: str,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in texts]
        if metadatas is None:
            metadatas = [{} for _ in texts]

        collection = self.get_collection(collection_name)
        collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )
        return ids

    def search(
        self,
        collection_name: str,
        query_embedding: List[float],
        top_k: int = 5,
        filter_metadata: Optional[Dict] = None,
    ) -> List[Dict[str, Any]]:
        collection = self.get_collection(collection_name)
        where = filter_metadata if filter_metadata else None
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
        )

        formatted = []
        if results["ids"] and results["ids"][0]:
            for i in range(len(results["ids"][0])):
                formatted.append(
                    {
                        "id": results["ids"][0][i],
                        "text": results["documents"][0][i] if results["documents"] else "",
                        "score": 1.0 - (results["distances"][0][i] if results["distances"] else 0),
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    }
                )
        return formatted

    def delete_collection(self, name: str) -> None:
        try:
            self.client.delete_collection(name=name)
        except Exception:
            pass

    def count(self, collection_name: str) -> int:
        collection = self.get_collection(collection_name)
        return collection.count()
