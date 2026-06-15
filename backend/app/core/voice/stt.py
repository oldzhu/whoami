"""Speech-to-text using faster-whisper."""
import logging
import os
import tempfile
from typing import Optional

logger = logging.getLogger(__name__)


class SpeechToText:
    """Local STT using faster-whisper."""

    def __init__(self, model_size: str = "base", device: str = "auto"):
        """
        Initialize STT with faster-whisper.

        Args:
            model_size: "tiny", "base", "small", "medium", "large-v3"
            device: "auto", "cpu", "cuda"
        """
        self.model_size = model_size
        self.device = device
        self._model = None
        self._models_dir = os.path.join("models", "whisper")

    def _load_model(self):
        """Lazy-load the whisper model."""
        if self._model is not None:
            return
        try:
            from faster_whisper import WhisperModel

            os.makedirs(self._models_dir, exist_ok=True)
            compute_type = "int8" if self.device == "cpu" else "float16"
            self._model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=compute_type,
                download_root=self._models_dir,
            )
            logger.info(
                "Whisper model '%s' loaded on %s", self.model_size, self.device
            )
        except ImportError:
            logger.warning(
                "faster-whisper not installed. Install: pip install faster-whisper"
            )
            self._model = None
        except Exception as e:
            logger.error("Failed to load whisper model: %s", e)
            self._model = None

    def transcribe_file(
        self, audio_path: str, language: Optional[str] = None
    ) -> dict:
        """
        Transcribe an audio file.

        Returns:
            dict with keys: text, language, language_probability, segments
        """
        self._load_model()
        if self._model is None:
            return {
                "text": "",
                "language": "unknown",
                "segments": [],
                "error": "Model not loaded",
            }

        segments, info = self._model.transcribe(
            audio_path, language=language, beam_size=5
        )

        text_parts = []
        segment_list = []
        for segment in segments:
            text_parts.append(segment.text)
            segment_list.append(
                {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text,
                }
            )

        return {
            "text": " ".join(text_parts).strip(),
            "language": info.language,
            "language_probability": info.language_probability,
            "segments": segment_list,
        }

    def transcribe_bytes(
        self, audio_bytes: bytes, language: Optional[str] = None
    ) -> dict:
        """
        Transcribe audio from bytes.

        Writes to a temp file, transcribes, then cleans up.
        """
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(audio_bytes)
            temp_path = f.name
        try:
            result = self.transcribe_file(temp_path, language=language)
        finally:
            os.unlink(temp_path)
        return result

    @property
    def is_ready(self) -> bool:
        """Check if model is loaded and ready."""
        self._load_model()
        return self._model is not None
