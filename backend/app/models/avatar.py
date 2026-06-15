from pydantic import BaseModel
from typing import Optional, List


class AvatarConfig(BaseModel):
    photo_url: Optional[str] = None
    animation_type: str  # "musetalk" | "sadtalker"
    idle_animation: bool


class AnimationState(BaseModel):
    speaking: bool
    expression: str
    lip_sync_data: Optional[List[float]] = None


class LipSyncFrame(BaseModel):
    time: float
    phoneme: str
    intensity: float


class LipSyncData(BaseModel):
    audio_url: str
    frames: List[LipSyncFrame]
