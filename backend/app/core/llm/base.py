"""Abstract base for LLM providers."""
from abc import ABC, abstractmethod
from typing import AsyncIterator, List, Dict, Any, Optional


class LLMProvider(ABC):
    """Abstract interface for LLM inference backends."""

    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Send a chat completion request. Returns OpenAI-compatible response."""
        ...

    @abstractmethod
    async def stream(self, messages: List[Dict[str, str]], **kwargs) -> AsyncIterator[str]:
        """Stream chat completion tokens."""
        ...

    @abstractmethod
    async def embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts."""
        ...

    @abstractmethod
    async def models(self) -> List[str]:
        """List available models."""
        ...

    @abstractmethod
    async def ping(self) -> bool:
        """Health check - returns True if backend is responsive."""
        ...
