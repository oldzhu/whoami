"""Voice conversation API."""
import json
import logging
import os
import shutil
import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, UploadFile, File, Depends
from ..core.voice import SpeechToText, TextToSpeech
from ..core.voice.orchestrator import VoiceOrchestrator
from ..middleware import auth_required

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/voice", tags=["voice"])

_orchestrator = None
VOICE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "voice"))


def _get_orch():
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = VoiceOrchestrator()
    return _orchestrator


@router.websocket("/conversation")
async def voice_conversation(websocket: WebSocket):
    """Real-time voice conversation via WebSocket."""
    await websocket.accept()
    orch = _get_orch()
    tts = TextToSpeech()

    await websocket.send_text(json.dumps({
        "type": "ready",
        "stt": orch.stt.is_ready,
        "tts": orch.tts.is_ready,
    }))

    async def on_state_change(state: str):
        await websocket.send_text(json.dumps({"type": "state", "state": state}))

    try:
        while True:
            data = await websocket.receive()

            if "text" in data:
                msg = json.loads(data["text"]) if isinstance(data["text"], str) else data
                if isinstance(msg, str):
                    msg = json.loads(msg)
            elif "bytes" in data:
                audio_bytes = data["bytes"]

                result = await orch.process_audio(
                    audio_bytes,
                    on_state_change=on_state_change,
                )

                await websocket.send_text(json.dumps({
                    "type": "result",
                    "text": result.get("text", ""),
                    "status": result.get("status", "complete"),
                }))
            else:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Send binary audio data or text JSON",
                }))

    except WebSocketDisconnect:
        logger.info("Voice WebSocket disconnected")


@router.get("/status")
async def voice_status():
    """Get voice pipeline status."""
    orch = _get_orch()
    return {
        "stt_ready": orch.stt.is_ready,
        "tts_ready": orch.tts.is_ready,
        "tts_speakers": orch.tts.speakers,
    }


@router.post("/speaker")
async def upload_speaker_sample(
    file: UploadFile = File(...),
    username: str = Depends(auth_required),
):
    os.makedirs(VOICE_DIR, exist_ok=True)
    speaker_id = str(uuid.uuid4())[:8]
    ext = os.path.splitext(file.filename or "sample.wav")[1] or ".wav"
    file_path = os.path.join(VOICE_DIR, f"{speaker_id}{ext}")
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    orch = _get_orch()
    tts = orch.tts
    success = tts.register_speaker(speaker_id, file_path)
    return {
        "speaker_id": speaker_id,
        "status": "registered" if success else "registration_failed",
        "username": username,
    }
