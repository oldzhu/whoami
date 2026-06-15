"""Conversation memory with sliding context window."""
from typing import List, Dict
from .session_manager import SessionManager


SYSTEM_PROMPT = (
    "You are a digital twin AI. Answer based on the user's personal knowledge "
    "and style. Be helpful, authentic, and concise."
)


class ConversationMemory:
    """Manages conversation context window for LLM interactions."""

    def __init__(self, session_manager: SessionManager, max_tokens: int = 4000):
        self.session_manager = session_manager
        self.max_tokens = max_tokens

    def estimate_tokens(self, messages: List[Dict]) -> int:
        total_chars = sum(len(m.get("content", "")) for m in messages)
        return total_chars // 4

    def prepare_context(self, session_id: str, new_message: str) -> List[Dict]:
        recent = self.session_manager.get_messages(session_id)
        context = [{"role": "system", "content": SYSTEM_PROMPT}]
        context.extend(
            {"role": m["role"], "content": m["content"]} for m in recent
        )

        reserved = self.estimate_tokens(context) + (len(new_message) // 4)
        while reserved > self.max_tokens and len(context) > 1:
            context.pop(1)
            reserved = self.estimate_tokens(context) + (len(new_message) // 4)

        return context
