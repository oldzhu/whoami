from pydantic import BaseModel
from typing import Optional


class VoiceSession(BaseModel):
    id: str
    status: str = "idle"
    started_at: str


class TTSRequest(BaseModel):
    text: str
    speaker_id: Optional[str] = None
    language: Optional[str] = "zh"


class TTSResponse(BaseModel):
    audio_url: str
    duration_ms: int


class STTResult(BaseModel):
    text: str
    language: str
    confidence: float
