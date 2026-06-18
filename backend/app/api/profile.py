"""Personal profile API."""
import json
import os
from fastapi import APIRouter, Depends
from ..middleware import auth_required

router = APIRouter(prefix="/api/profile", tags=["profile"])

PROFILE_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "profile.json")
PROFILE_FILE = os.path.abspath(PROFILE_FILE)

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


def _load_profile():
    saved = None
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE) as f:
            saved = json.load(f)
    if saved:
        # Merge with defaults so missing fields are filled in
        merged = dict(DEFAULT_PROFILE)
        merged.update(saved)
        return merged
    return DEFAULT_PROFILE


def _save_profile(data: dict):
    os.makedirs(os.path.dirname(PROFILE_FILE), exist_ok=True)
    with open(PROFILE_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@router.get("")
async def get_profile():
    return _load_profile()


@router.put("")
async def put_profile(body: dict, username: str = Depends(auth_required)):
    _save_profile(body)
    return {"status": "saved", "username": username}


@router.post("")
async def post_profile(body: dict, username: str = Depends(auth_required)):
    _save_profile(body)
    return {"status": "saved", "username": username}
