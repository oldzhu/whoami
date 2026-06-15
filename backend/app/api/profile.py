"""Personal profile API."""
from fastapi import APIRouter

router = APIRouter(prefix="/api/profile", tags=["profile"])

DEFAULT_PROFILE = {
    "name": "Your Name",
    "title": "AI Digital Twin",
    "summary": "A self-evolving AI digital clone powered by local open-source LLMs.",
    "skills": [
        {"name": "Python", "category": "Programming", "level": 5},
        {"name": "Machine Learning", "category": "AI", "level": 5},
        {"name": "FastAPI", "category": "Backend", "level": 4},
        {"name": "React/Next.js", "category": "Frontend", "level": 4},
        {"name": "LLM/RAG", "category": "AI", "level": 5},
    ],
    "projects": [
        {
            "name": "Digital Twin",
            "description": "AI-powered personal clone with multi-modal interaction",
            "technologies": ["Python", "FastAPI", "Next.js", "Ollama", "ChromaDB"],
        },
    ],
    "experience": [
        {
            "company": "Self-Employed",
            "role": "AI Developer",
            "description": "Building next-generation AI applications",
            "start_date": "2024",
        },
    ],
    "education": [
        {
            "institution": "University",
            "degree": "Bachelor",
            "field": "Computer Science",
            "year": 2020,
        },
    ],
}

@router.get("")
async def get_profile():
    return DEFAULT_PROFILE
