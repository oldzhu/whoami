"""Build LLM context from retrieved results."""

from typing import Any, Dict, List, Optional

SYSTEM_PROMPT = """You are a digital twin AI representing a real person. Answer questions based on the provided context from their resume, projects, and knowledge base. Be authentic, helpful, and concise. If the context doesn't contain relevant information, say so honestly.

Context:
{context}

Question: {question}
Answer:"""


class ContextBuilder:
    """Builds prompts from retrieved context chunks."""

    def build(
        self,
        query: str,
        results: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        """Build the LLM prompt with retrieved context."""
        prompt = system_prompt or SYSTEM_PROMPT

        # Format context from results
        context_parts = []
        for i, r in enumerate(results):
            text = r.get("text", "")
            source = (
                r.get("metadata", {}).get("source_file")
                or r.get("source", "unknown")
            )
            context_parts.append(f"[Source {i + 1}: {source}]\n{text}")

        context = "\n\n---\n\n".join(context_parts)

        # Build messages in chat format
        messages = [
            {
                "role": "system",
                "content": prompt.format(context=context, question=query),
            },
            {"role": "user", "content": query},
        ]
        return messages
