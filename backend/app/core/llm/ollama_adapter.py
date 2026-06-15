"""Ollama adapter using aiohttp to call Ollama REST API."""
import logging
from typing import AsyncIterator, List, Dict, Any
import aiohttp

from .base import LLMProvider

logger = logging.getLogger(__name__)


class OllamaAdapter(LLMProvider):
    """Adapter for Ollama's native REST API, returning OpenAI-compatible responses."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    async def _request(self, method: str, path: str, json: Dict = None) -> Any:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method, f"{self.base_url}{path}", json=json) as resp:
                    if resp.status >= 400:
                        logger.warning(f"Ollama {method} {path} failed: {resp.status}")
                        return None
                    return await resp.json()
        except aiohttp.ClientError as e:
            logger.warning(f"Ollama connection error: {e}")
            return None

    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        model = kwargs.get("model", self.model)
        payload = {"model": model, "messages": messages, "stream": False}
        payload.update({k: v for k, v in kwargs.items() if k not in ("model", "stream")})
        result = await self._request("POST", "/api/chat", json=payload)
        if result is None:
            return {"choices": [{"message": {"content": ""}}]}
        return {
            "choices": [{"message": {"content": result.get("message", {}).get("content", "")}}],
            "model": result.get("model", model),
        }

    async def stream(self, messages: List[Dict[str, str]], **kwargs) -> AsyncIterator[str]:
        model = kwargs.get("model", self.model)
        payload = {"model": model, "messages": messages, "stream": True}
        payload.update({k: v for k, v in kwargs.items() if k not in ("model", "stream")})
        import json as _json
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/api/chat", json=payload) as resp:
                    if resp.status >= 400:
                        logger.warning(f"Ollama stream failed: {resp.status}")
                        return
                    while True:
                        line = await resp.content.readline()
                        if not line:
                            break
                        line_str = line.decode().strip()
                        if line_str:
                            try:
                                data = _json.loads(line_str)
                                chunk = data.get("message", {}).get("content", "")
                                if chunk:
                                    yield chunk
                            except _json.JSONDecodeError:
                                continue
        except aiohttp.ClientError as e:
            logger.warning(f"Ollama stream error: {e}")

    async def embed(self, texts: List[str]) -> List[List[float]]:
        model = f"{self.model}-embed" if hasattr(self, "model") else "nomic-embed-text"
        embeddings = []
        for text in texts:
            result = await self._request("POST", "/api/embeddings", json={"model": model, "prompt": text})
            if result is None:
                embeddings.append([])
            else:
                embeddings.append(result.get("embedding", []))
        return embeddings

    async def models(self) -> List[str]:
        result = await self._request("GET", "/api/tags")
        if result is None:
            return []
        return [m["name"] for m in result.get("models", [])]

    async def ping(self) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/tags", timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    return resp.status < 400
        except Exception:
            return False
