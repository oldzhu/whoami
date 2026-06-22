"""Text-to-speech using Piper TTS with multi-language voice support."""
import logging
import os
import io
import wave
from typing import Optional

logger = logging.getLogger(__name__)

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "models", "piper")
MODELS_DIR = os.path.abspath(MODELS_DIR)

VOICE_MAP = {
    "zh": os.path.join(MODELS_DIR, "zh_CN-huayan-medium.onnx"),
    "en": os.path.join(MODELS_DIR, "en_US-lessac-medium.onnx"),
}


class TextToSpeech:
    """Local TTS using Piper (lightweight, works on Python 3.12)."""

    def __init__(self):
        self._voices: dict[str, object] = {}
        self._speakers: dict[str, str] = {}  # speaker_id -> wav_path (for future cloning)
        self.default_voice = "zh"

    def _load_voice(self, lang: str):
        if lang in self._voices:
            return self._voices[lang]
        model_path = VOICE_MAP.get(lang, VOICE_MAP.get("zh", ""))
        config_path = model_path + ".json"
        if not os.path.exists(model_path):
            logger.warning(f"Voice model not found: {model_path}")
            return None
        try:
            from piper import PiperVoice
            voice = PiperVoice.load(model_path, config_path=config_path)
            self._voices[lang] = voice
            logger.info(f"Piper voice loaded: {lang}")
            return voice
        except Exception as e:
            logger.error(f"Failed to load Piper voice: {e}")
            return None

    def register_speaker(self, speaker_id: str, sample_wav_path: str) -> bool:
        """Register a voice sample (for future voice cloning)."""
        self._speakers[speaker_id] = sample_wav_path
        if not self._speakers:
            self.default_voice = speaker_id
        logger.info(f"Speaker '{speaker_id}' registered")
        return True

    def synthesize(
        self,
        text: str,
        speaker_id: Optional[str] = None,
        language: str = "zh",
        output_path: Optional[str] = None,
    ) -> bytes:
        """Synthesize speech. Returns WAV audio bytes."""
        lang = language[:2] if language else "zh"
        if lang not in VOICE_MAP:
            lang = "zh"
        model_path = VOICE_MAP.get(lang, "")
        if not os.path.exists(model_path):
            return b""
        try:
            import subprocess, sys
            result = subprocess.run(
                [sys.executable, "-m", "piper", "--model", model_path, "--output-raw", "-q"],
                input=text.encode("utf-8"), capture_output=True, timeout=30,
            )
            if result.returncode != 0 or not result.stdout:
                return b""
            raw = result.stdout
            buf = io.BytesIO()
            with wave.open(buf, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(22050)
                wf.writeframes(raw)
            audio = buf.getvalue()
            if output_path:
                os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(audio)
            return audio
        except Exception as e:
            logger.error(f"TTS failed: {e}")
            return b""

    @property
    def is_ready(self) -> bool:
        return any(os.path.exists(p) for p in VOICE_MAP.values())

    @property
    def speakers(self) -> list:
        return list(self._speakers.keys())
