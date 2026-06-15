"""Context compression for long conversations."""
from typing import List, Dict


class ContextCompressor:
    """Compresses conversation history to fit token limits."""

    def compress(self, messages: List[Dict], max_tokens: int) -> List[Dict]:
        result = []
        tokens_used = 0
        for msg in reversed(messages):
            chars = len(msg.get("content", ""))
            est_tokens = chars // 4
            if tokens_used + est_tokens > max_tokens:
                break
            result.insert(0, msg)
            tokens_used += est_tokens
        return result

    def summarize(self, messages: List[Dict]) -> str:
        if not messages:
            return ""
        roles = set(m.get("role") for m in messages)
        total_chars = sum(len(m.get("content", "")) for m in messages)
        participant = ", ".join(sorted(roles))
        return (
            f"[{len(messages)} exchanged messages ({total_chars} chars) "
            f"between {participant}]"
        )
