"""Real-time voice conversation orchestrator."""
import asyncio
import logging
from enum import Enum
from typing import Optional, Callable, Awaitable

from .stt import SpeechToText
from .tts import TextToSpeech

logger = logging.getLogger(__name__)


class VoiceState(Enum):
    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"


class VoiceOrchestrator:
    """Orchestrates real-time voice conversation: STT → LLM → TTS."""

    def __init__(self):
        self.stt = SpeechToText()
        self.tts = TextToSpeech()
        self.state = VoiceState.IDLE
        self._rag_chain = None
        self._interrupt = False

    @property
    def rag_chain(self):
        if self._rag_chain is None:
            from ..rag.rag_chain import RAGChain
            self._rag_chain = RAGChain()
        return self._rag_chain

    async def process_audio(
        self,
        audio_bytes: bytes,
        on_state_change: Optional[Callable[[str], Optional[Awaitable[None]]]] = None,
        on_audio_ready: Optional[Callable[[bytes], Optional[Awaitable[None]]]] = None,
    ) -> dict:
        """Process audio input → text → LLM → speech output."""
        # 1. STT: Listening
        await self._set_state(VoiceState.LISTENING, on_state_change)
        stt_result = await asyncio.to_thread(
            self.stt.transcribe_bytes, audio_bytes
        )
        text = stt_result.get("text", "")
        language = stt_result.get("language", "zh")

        if not text:
            return {"status": "no_speech", "text": ""}

        # 2. LLM: Thinking
        await self._set_state(VoiceState.THINKING, on_state_change)
        rag_result = await self.rag_chain.query(text)
        response_text = rag_result.get("answer", "")

        if self._interrupt:
            self._interrupt = False
            return {"status": "interrupted", "text": response_text[:50]}

        # 3. TTS: Speaking
        await self._set_state(VoiceState.SPEAKING, on_state_change)
        audio_output = await asyncio.to_thread(
            self.tts.synthesize, text=response_text, language=language
        )

        if on_audio_ready and audio_output:
            result = on_audio_ready(audio_output)
            if asyncio.iscoroutine(result):
                await result

        await self._set_state(VoiceState.IDLE, on_state_change)

        return {
            "status": "complete",
            "text": response_text,
            "audio_size": len(audio_output),
        }

    def process_text_to_speech(self, text: str, language: str = "zh") -> bytes:
        """Convert text directly to speech (no STT step)."""
        return self.tts.synthesize(text=text, language=language)

    def interrupt(self):
        """Interrupt current speech."""
        self._interrupt = True

    async def _set_state(
        self,
        state: VoiceState,
        callback: Optional[Callable[[str], Optional[Awaitable[None]]]] = None,
    ):
        self.state = state
        if callback:
            result = callback(state.value)
            if asyncio.iscoroutine(result):
                await result

    @property
    def is_ready(self) -> bool:
        return self.stt.is_ready or self.tts.is_ready
