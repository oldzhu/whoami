"""Voice pipeline unit tests — STT, TTS, orchestrator."""
import sys, os, io, wave
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_stt_import():
    from backend.app.core.voice.stt import SpeechToText
    stt = SpeechToText()
    assert stt.model_size == "base"

def test_stt_model_ready():
    from backend.app.core.voice.stt import SpeechToText
    stt = SpeechToText()
    assert stt.is_ready

def test_tts_import():
    from backend.app.core.voice.tts import TextToSpeech
    tts = TextToSpeech()

def test_tts_model_ready():
    from backend.app.core.voice.tts import TextToSpeech
    tts = TextToSpeech()
    assert tts.is_ready

def test_tts_synthesize_zh():
    from backend.app.core.voice.tts import TextToSpeech
    tts = TextToSpeech()
    audio = tts.synthesize("你好", language="zh")
    assert len(audio) > 1000  # Real audio > 1KB

def test_tts_synthesize_en():
    from backend.app.core.voice.tts import TextToSpeech
    tts = TextToSpeech()
    audio = tts.synthesize("Hello world", language="en")
    assert len(audio) > 1000

def test_tts_valid_wav():
    from backend.app.core.voice.tts import TextToSpeech
    tts = TextToSpeech()
    audio = tts.synthesize("test", language="en")
    buf = io.BytesIO(audio)
    with wave.open(buf, "rb") as wf:
        assert wf.getnchannels() == 1
        assert wf.getsampwidth() == 2
        assert wf.getframerate() == 22050
        frames = wf.readframes(wf.getnframes())
        assert len(frames) > 0

def test_tts_unknown_lang_fallback():
    from backend.app.core.voice.tts import TextToSpeech
    tts = TextToSpeech()
    audio = tts.synthesize("test", language="fr")
    assert len(audio) > 1000  # Falls back to zh

def test_tts_missing_model():
    from backend.app.core.voice.tts import TextToSpeech
    import backend.app.core.voice.tts as tts_mod
    original = dict(tts_mod.VOICE_MAP)
    tts_mod.VOICE_MAP = {"fr": "/nonexistent/model.onnx"}
    try:
        tts = TextToSpeech()
        audio = tts.synthesize("test", language="fr")
        assert audio == b""
    finally:
        tts_mod.VOICE_MAP = original

def test_voice_api_status():
    from fastapi.testclient import TestClient
    from backend.app.main import app
    client = TestClient(app)
    r = client.get("/api/voice/status")
    assert r.status_code == 200

def test_speaker_registration():
    from backend.app.core.voice.tts import TextToSpeech
    tts = TextToSpeech()
    assert tts.register_speaker("test_speaker", "/tmp/test.wav")
    assert "test_speaker" in tts.speakers
