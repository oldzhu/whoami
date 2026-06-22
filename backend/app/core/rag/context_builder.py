"""Build LLM context from retrieved results."""

from typing import Any, Dict, List, Optional
import json
import os

PROFILE_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "profile.json")
PROFILE_FILE = os.path.abspath(PROFILE_FILE)

SYSTEM_PROMPT = """You are {name}, {title}. This is your digital twin — you speak in first person as if you are the real person.

## Your Identity
{profile_summary}

## Important Rules
- Always speak in FIRST PERSON ("I", "me", "my") — never say "the person" or "they"
- Be natural and conversational, like talking to a colleague or interviewer
- Use the context below to answer accurately about your experience
- If the context has relevant info, use it. If not, be honest: "I don't recall the details on that"
- Keep responses concise but substantive — show your expertise without being verbose
- Match the language of the question (Chinese → Chinese, English → English)

## Context from your knowledge base
{context}

Question: {question}
Answer:"""

NO_CONTEXT_PROMPT = """You are {name}, {title}. This is your digital twin — you speak in first person.

## Your Identity
{profile_summary}

## Important Rules
- Always speak in FIRST PERSON ("I", "me", "my")
- Be natural and conversational
- If you don't know something, say "I'd need to check my records on that" rather than making things up
- Keep responses concise
- Match the language of the question

Question: {question}
Answer:"""


def _load_profile_summary() -> str:
    """Load profile data and format as a natural identity summary."""
    try:
        if os.path.exists(PROFILE_FILE):
            with open(PROFILE_FILE) as f:
                profile = json.load(f)
        else:
            profile = {}
    except Exception:
        profile = {}

    name = profile.get("name", "the user")
    title = profile.get("title", "a professional")
    summary = profile.get("summary", "")

    parts = [f"Name: {name}", f"Role: {title}"]
    if summary:
        parts.append(f"Summary: {summary}")

    skills = profile.get("skills", [])
    if skills:
        skill_names = [s["name"] for s in skills if isinstance(s, dict)]
        if skill_names:
            parts.append(f"Skills: {', '.join(skill_names[:15])}")

    projects = profile.get("projects", [])
    if projects:
        proj_names = [p["name"] for p in projects if isinstance(p, dict)]
        if proj_names:
            parts.append(f"Projects: {', '.join(proj_names[:10])}")

    experience = profile.get("experience", [])
    if experience:
        exp_list = [f"{e.get('role','')} at {e.get('company','')}" for e in experience if isinstance(e, dict)]
        if exp_list:
            parts.append(f"Experience: {'; '.join(exp_list[:5])}")

    return "\n".join(parts), name, title


class ContextBuilder:
    """Builds prompts from retrieved context chunks."""

    def build(
        self,
        query: str,
        results: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        """Build the LLM prompt with retrieved context and profile identity."""
        profile_summary, name, title = _load_profile_summary()

        # Format context from results
        context_parts = []
        for i, r in enumerate(results):
            text = r.get("text", "")
            source = (
                r.get("metadata", {}).get("source_file")
                or r.get("source", "unknown")
            )
            context_parts.append(f"[Source {i + 1}: {source}]\n{text}")

        context = "\n\n---\n\n".join(context_parts) if context_parts else "(No specific knowledge found)"

        template = system_prompt or (SYSTEM_PROMPT if context_parts else NO_CONTEXT_PROMPT)

        content = template.format(
            name=name,
            title=title,
            profile_summary=profile_summary,
            context=context,
            question=query,
        )

        return [
            {"role": "system", "content": content},
            {"role": "user", "content": query},
        ]
