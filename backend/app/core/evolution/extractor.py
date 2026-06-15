"""Extract new facts from conversations."""
import json
import logging
import re
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class FactExtractor:
    """Extracts structured facts from conversation messages."""

    def __init__(self):
        self.extraction_prompt = """Extract new personal facts from the conversation. Return a JSON list.

For each fact, include:
- fact_type: "skill", "experience", "project", "preference", "education", "contact", "other"
- content: the extracted fact as a natural language statement
- confidence: 0.0 to 1.0 (how certain you are this is a real fact)
- source_message_id: the message that contained this fact

Only extract NEW facts that the user explicitly stated. Do NOT extract:
- Questions asked by the user
- General conversation that doesn't contain personal information
- Facts that are already known

Conversation:
{conversation}

Facts:"""

    async def extract(self, messages: List[Dict]) -> List[Dict]:
        """Extract facts from a list of messages."""
        conv_text = ""
        for msg in messages[-20:]:  # Last 20 messages
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            conv_text += f"{role}: {content}\n"

        facts = self._keyword_extraction(conv_text)
        return facts

    def _keyword_extraction(self, text: str) -> List[Dict]:
        """Simple keyword-based fact extraction (MVP)."""
        facts = []
        text_lower = text.lower()

        skill_keywords = [
            "python", "javascript", "react", "fastapi", "machine learning",
            "docker", "kubernetes", "sql", "aws", "gcp", "azure",
        ]
        for skill in skill_keywords:
            if skill in text_lower:
                facts.append({
                    "fact_type": "skill",
                    "content": f"Knows {skill}",
                    "confidence": 0.8,
                    "source": "keyword_extraction",
                })

        project_patterns = [
            r"worked on (.+?)(?:\.|,| and)",
            r"built (.+?)(?:\.|,| using)",
            r"project.*?called (.+?)(?:\.|,)",
        ]
        for pattern in project_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                if len(match) > 3:
                    facts.append({
                        "fact_type": "project",
                        "content": f"Worked on: {match.strip()}",
                        "confidence": 0.6,
                        "source": "keyword_extraction",
                    })

        return facts
