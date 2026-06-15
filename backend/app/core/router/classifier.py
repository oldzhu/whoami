"""Simple rule-based intent classifier for model routing."""
import re
from typing import Dict


class IntentClassifier:
    """Classify user messages to determine which model to use."""

    PATTERNS: Dict[str, list] = {
        "code": [
            r'\b(code|program|function|class|debug|bug|error|python|javascript|typescript|java|rust|golang|api|algorithm|git|sql|docker|react|next\.js)\b',
            r'```',
            r'import ',
            r'def ',
            r'function ',
            r'how (to|do I|can I) (write|implement|code|program|fix|debug|build|create)',
        ],
        "chinese": [
            r'[\u4e00-\u9fff]',
        ],
        "technical": [
            r'\b(llm|ai|machine learning|neural|transformer|model|training|inference|embedding|rag|vector|database)\b',
            r'\b(architecture|design pattern|system design|scal|performance)\b',
        ],
        "casual": [
            r'\b(hi|hello|hey|how are you|what\'?s up|good morning|good evening)\b',
        ],
    }

    def classify(self, message: str) -> Dict[str, float]:
        """Return classification scores for each category."""
        message_lower = message.lower()
        scores = {}
        for category, patterns in self.PATTERNS.items():
            score = 0.0
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    score += 1.0
            scores[category] = min(score / max(len(patterns), 1), 1.0)

        cjk_count = sum(1 for c in message if '\u4e00' <= c <= '\u9fff')
        if len(message) > 0 and cjk_count / len(message) > 0.2:
            scores["chinese"] = max(scores.get("chinese", 0), 0.8)

        return scores
