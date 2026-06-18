"""Mock LLM adapter for testing — returns canned responses."""
from typing import AsyncIterator, List, Dict, Any
from .base import LLMProvider


class MockAdapter(LLMProvider):

    def __init__(self, **kwargs):
        self._ready = True

    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        user_msg = ""
        for m in messages:
            if m.get("role") == "user":
                user_msg = m.get("content", "")
        response = self._generate_response(user_msg)
        return {
            "choices": [{"message": {"role": "assistant", "content": response}}],
            "model": "mock",
            "usage": {"total_tokens": len(response)},
        }

    async def stream(self, messages: List[Dict[str, str]], **kwargs) -> AsyncIterator[str]:
        result = await self.chat(messages, **kwargs)
        text = result["choices"][0]["message"]["content"]
        for char in text:
            yield char

    async def embed(self, texts: List[str]) -> List[List[float]]:
        return [[0.1] * 384 for _ in texts]

    async def models(self) -> List[str]:
        return ["mock-model"]

    async def ping(self) -> bool:
        return True

    def _generate_response(self, msg: str) -> str:
        msg_lower = msg.lower()
        if any(w in msg_lower for w in ["hello", "hi", "你好", "hey"]):
            return "Hello! I'm your Digital Twin AI. Ask me about my projects, skills, or experience. 你好！我是你的数字分身 AI。问我任何关于项目、技能或经历的问题吧。"
        elif any(w in msg_lower for w in ["project", "项目", "work", "工作"]):
            return "I've worked on several AI projects including this Digital Twin system — a full-stack AI clone with local LLM inference, RAG knowledge retrieval, voice interaction, and multi-platform deployment (Web, Android, Desktop). Tech stack: Python FastAPI, Next.js, React Native, ChromaDB, Neo4j, and Ollama."
        elif any(w in msg_lower for w in ["skill", "技能", "tech", "技术"]):
            return "My technical skills include: Python, FastAPI, Next.js, React, TypeScript, Machine Learning, LLM/RAG systems, Docker, Neo4j, ChromaDB, and full-stack web development. I specialize in building AI-powered applications that run entirely on local open-source models."
        elif any(w in msg_lower for w in ["who", "你是谁", "about", "关于"]):
            return "I'm a Digital Twin — an AI clone that learns from personal data and interacts on behalf of my human counterpart. I run entirely on local open-source LLMs, with no cloud API dependencies. I can chat, speak, and show my work experience through this interface."
        elif any(w in msg_lower for w in ["experience", "经历", "background"]):
            return "I have experience in AI/ML development, full-stack engineering, and building self-evolving systems. Key achievements include designing RAG pipelines, implementing multi-model routing, and creating voice-enabled AI assistants."
        elif "?" in msg or "？" in msg:
            return "That's an interesting question! Based on my knowledge and experience, I'd approach this by considering the key factors and applying best practices from the field. Is there a specific aspect you'd like me to elaborate on?"
        else:
            return f"I understand you're interested in discussing '{msg[:50]}...'. As your Digital Twin, I'm here to share my knowledge and experience. What specific aspects would you like to know more about?"
