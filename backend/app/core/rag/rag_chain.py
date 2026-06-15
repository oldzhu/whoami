"""Complete RAG chain: retrieve -> rerank -> build -> generate."""

from typing import Any, AsyncIterator, Dict, List

from ..llm import create_llm_provider
from .context_builder import ContextBuilder
from .reranker import Reranker
from .retriever import HybridRetriever


class RAGChain:
    """End-to-end RAG pipeline orchestrator."""

    def __init__(self, backend: str = "auto"):
        self.retriever = HybridRetriever()
        self.reranker = Reranker()
        self.context_builder = ContextBuilder()
        self.provider = create_llm_provider(backend)

    async def query(
        self, question: str, top_k: int = 5
    ) -> Dict[str, Any]:
        """Run a RAG query end-to-end: retrieve, rerank, build context, generate."""
        # 1. Retrieve
        results = self.retriever.search(question, top_k=top_k)

        # 2. Rerank
        results = self.reranker.rerank(question, results, top_k=3)

        # 3. Build context
        messages = self.context_builder.build(question, results)

        # 4. Generate (with fallback if LLM unavailable)
        try:
            response = await self.provider.chat(messages)
            answer = (
                response.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )
        except Exception as e:
            answer = (
                f"I found some relevant information but couldn't generate "
                f"a response. Error: {e}"
            )

        sources = [
            {
                "text": r.get("text", "")[:200],
                "source": r.get("source", ""),
                "score": r.get("rerank_score", r.get("score", 0)),
            }
            for r in results
        ]

        return {
            "answer": answer,
            "sources": sources,
            "results": results,
        }

    async def stream(self, question: str) -> AsyncIterator[str]:
        """Stream RAG response token by token."""
        results = self.retriever.search(question)
        results = self.reranker.rerank(question, results)
        messages = self.context_builder.build(question, results)
        async for token in self.provider.stream(messages):
            yield token
