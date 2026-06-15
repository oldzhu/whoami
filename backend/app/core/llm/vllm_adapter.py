"""vLLM adapter using aiohttp for OpenAI-compatible API."""
import logging
from typing import AsyncIterator, List, Dict, Any
import aiohttp

from .base import LLMProvider

logger = logging.getLogger(__name__)


class VLLMAdapter(LLMProvider):
    """Adapter for vLLM server's OpenAI-compatible endpoints."""

    def __init__(self, base_url: str = "http://localhost:8000", model: str = "default"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    async def _request(self, method: str, path: str, json: Dict = None) -> Any:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method, f"{self.base_url}{path}", json=json) as resp:
                    if resp.status >= 400:
                        logger.warning(f"vLLM {method} {path} failed: {resp.status}")
                        return None
                    return await resp.json()
        except aiohttp.ClientError as e:
            logger.warning(f"vLLM connection error: {e}")
            return None

    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        model = kwargs.get("model", self.model)
        payload = {"model": model, "messages": messages, "stream": False}
        payload.update({k: v for k, v in kwargs.items() if k not in ("model", "stream")})
        result = await self._request("POST", "/v1/chat/completions", json=payload)
        if result is None:
            return {"choices": [{"message": {"content": ""}}]}
        return result

    async def stream(self, messages: List[Dict[str, str]], **kwargs) -> AsyncIterator[str]:
        model = kwargs.get("model", self.model)
        payload = {"model": model, "messages": messages, "stream": True}
        payload.update({k: v for k, v in kwargs.items() if k not in ("model", "stream")})
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/v1/chat/completions", json=payload) as resp:
                    if resp.status >= 400:
                        logger.warning(f"vLLM stream failed: {resp.status}")
                        return
                    buffer = ""
                    async for chunk in resp.content.iter_chunked(256):
                        buffer += chunk.decode()
                        while "data: " in buffer:
                            line, _, buffer = buffer.partition("\n")
                            line = line.replace("data: ", "").strip()
                            if line and line != "[DONE]":
                                import json
                                try:
                                    data = json.loads(line)
                                    delta = data.get("choices", [{}])[0].get("delta", {})
                                    content = delta.get("content", "")
                                    if content:
                                        yield content
                                except json.JSONDecodeError:
                                    continue
        except aiohttp.ClientError as e:
            logger.warning(f"vLLM stream error: {e}")

    async def embed(self, texts: List[str]) -> List[List[float]]:
        payload = {"input": texts}
        result = await self._request("POST", "/v1/embeddings", json=payload)
        if result is None:
            return [[] for _ in texts]
        data = result.get("data", [])
        return [item.get("embedding", []) for item in data]

    async def models(self) -> List[str]:
        result = await self._request("GET", "/v1/models")
        if result is None:
            return []
        return [m["id"] for m in result.get("data", [])]

    async def ping(self) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/v1/models", timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    return resp.status < 400
        except Exception:
            return False
