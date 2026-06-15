"""Text-to-speech using Coqui XTTS v2 with voice cloning."""
import logging
import os
import io
from typing import Optional

logger = logging.getLogger(__name__)


class TextToSpeech:
    """Local TTS with Coqui XTTS v2."""

    def __init__(self, models_dir: str = "models/xtts"):
        self.models_dir = models_dir
        self._model = None
        self._speaker_embeddings = {}
        self.default_speaker = None

    def _load_model(self):
        """Lazy-load the XTTS model."""
        if self._model is not None:
            return
        try:
            from TTS.api import TTS as CoquiTTS
            os.makedirs(self.models_dir, exist_ok=True)
            self._model = CoquiTTS(
                model_name="tts_models/multilingual/multi-dataset/xtts_v2",
                progress_bar=False,
            )
            logger.info("XTTS v2 model loaded")
        except ImportError:
            logger.warning("Coqui TTS not installed. Install: pip install TTS")
            self._model = None
        except Exception as e:
            logger.error(f"Failed to load XTTS model: {e}")
            self._model = None

    def register_speaker(self, speaker_id: str, sample_wav_path: str) -> bool:
        """Register a speaker from a voice sample for cloning."""
        self._load_model()
        if self._model is None:
            return False
        try:
            self._speaker_embeddings[speaker_id] = sample_wav_path
            if self.default_speaker is None:
                self.default_speaker = speaker_id
            logger.info(f"Speaker '{speaker_id}' registered")
            return True
        except Exception as e:
            logger.error(f"Failed to register speaker: {e}")
            return False

    def synthesize(
        self,
        text: str,
        speaker_id: Optional[str] = None,
        language: str = "zh",
        output_path: Optional[str] = None,
    ) -> bytes:
        """Synthesize speech from text. Returns WAV audio bytes."""
        self._load_model()
        if self._model is None:
            return b""

        speaker = speaker_id or self.default_speaker
        speaker_wav = self._speaker_embeddings.get(speaker) if speaker else None

        try:
            wav = self._model.tts(
                text=text,
                speaker_wav=speaker_wav,
                language=language,
            )

            import numpy as np
            import wave

            wav_np = np.array(wav, dtype=np.float32)
            wav_int16 = (wav_np * 32767).astype(np.int16)

            buf = io.BytesIO()
            with wave.open(buf, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(24000)
                wf.writeframes(wav_int16.tobytes())

            audio_bytes = buf.getvalue()

            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(audio_bytes)

            return audio_bytes
        except Exception as e:
            logger.error(f"TTS synthesis failed: {e}")
            return b""

    @property
    def is_ready(self) -> bool:
        self._load_model()
        return self._model is not None

    @property
    def speakers(self) -> list:
        return list(self._speaker_embeddings.keys())
