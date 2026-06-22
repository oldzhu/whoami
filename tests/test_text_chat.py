"""Text chat + auth + knowledge + RAG tests."""
import pytest
from fastapi.testclient import TestClient
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.app.main import app
from backend.app.core.auth import get_auth

client = TestClient(app)

def _fresh_auth():
    auth = get_auth()
    path = auth._auth_file
    if os.path.exists(path):
        os.remove(path)
    client.post("/api/auth/setup", json={"username": "test", "password": "test1234"})
    r = client.post("/api/auth/login", json={"username": "test", "password": "test1234"})
    return r.json()["token"]

@pytest.fixture(autouse=True)
def reset_auth():
    auth = get_auth()
    if os.path.exists(auth._auth_file):
        os.remove(auth._auth_file)

# ── Health ──
def test_health(): assert client.get("/health").json()["status"] == "ok"

# ── Auth ──
def test_auth_status_not_setup(): assert client.get("/api/auth/status").json()["setup"] == False
def test_auth_setup(): assert client.post("/api/auth/setup", json={"username": "admin1", "password": "p1234"}).status_code == 200
def test_auth_setup_twice():
    client.post("/api/auth/setup", json={"username": "admin1", "password": "p1234"})
    assert client.post("/api/auth/setup", json={"username": "admin1", "password": "p1234"}).status_code == 400
def test_auth_login_ok():
    token = _fresh_auth()
    assert len(token) > 10
def test_auth_login_bad():
    _fresh_auth()
    assert client.post("/api/auth/login", json={"username": "test", "password": "wrong"}).status_code == 401
def test_auth_reset():
    token = _fresh_auth()
    r = client.post("/api/auth/reset", json={"current_password":"test1234","new_password":"pass"}, headers={"Authorization":f"Bearer {token}"})
    assert r.json()["status"] == "password_updated"
def test_auth_reset_no_token():
    _fresh_auth()
    assert client.post("/api/auth/reset", json={"current_password":"x","new_password":"y"}).status_code == 401

# ── Profile ──
def test_profile_get(): assert "name" in client.get("/api/profile").json()
def test_profile_put_no_auth(): assert client.put("/api/profile", json={"name":"x"}).status_code == 401
def test_profile_put_auth():
    token = _fresh_auth()
    assert client.put("/api/profile", json={"name":"Test"}, headers={"Authorization":f"Bearer {token}"}).status_code == 200

# ── Chat ──
def test_chat_post(): assert client.post("/api/chat", json={"message":"hi"}).status_code in (200, 503)
def test_chat_history_no_auth(): assert client.get("/api/chat/history/x").status_code == 401
def test_chat_history_auth():
    token = _fresh_auth()
    assert client.get("/api/chat/history/x", headers={"Authorization":f"Bearer {token}"}).status_code in (404, 200)

# ── Knowledge ──
def test_knowledge_search(): assert "results" in client.get("/api/knowledge/search?q=test").json()
def test_knowledge_upload_no_auth(): assert client.post("/api/knowledge/upload").status_code in (401, 422)
def test_knowledge_stats_no_auth(): assert client.get("/api/knowledge/stats").status_code == 401
def test_knowledge_stats_auth():
    token = _fresh_auth()
    assert client.get("/api/knowledge/stats", headers={"Authorization":f"Bearer {token}"}).status_code == 200

# ── Evolution ──
def test_evolution_approve_no_auth(): assert client.post("/api/evolution/approve/x").status_code == 401
def test_evolution_pending_auth():
    token = _fresh_auth()
    assert client.get("/api/evolution/pending", headers={"Authorization":f"Bearer {token}"}).status_code == 200

# ── Router ──
def test_router_chinese():
    from backend.app.core.router.classifier import IntentClassifier
    scores = IntentClassifier().classify("你好，介绍你的项目")
    assert scores.get("chinese", 0) > 0.5
def test_router_code():
    from backend.app.core.router.classifier import IntentClassifier
    scores = IntentClassifier().classify("write a Python sort function for me")
    assert scores.get("code", 0) > 0.15

# ── RAG ──
def test_context_builder():
    from backend.app.core.rag.context_builder import ContextBuilder
    msgs = ContextBuilder().build("test", [{"text":"ctx","source":"s","score":1,"metadata":{"source_file":"f"}}])
    assert msgs[0]["role"] == "system" and "test" in msgs[1]["content"]

# ── LLM ──
def test_mock_adapter():
    from backend.app.core.llm.mock_adapter import MockAdapter
    assert MockAdapter() is not None
def test_factory_mock():
    from backend.app.core.llm import create_llm_provider
    assert create_llm_provider("mock") is not None

# ── Session ──
def test_session_manager():
    from backend.app.core.conversation.session_manager import SessionManager
    sm = SessionManager()
    sid = sm.create_session("test")
    assert len(sid) > 0
    sm.add_message(sid, "user", "hello")
    msgs = sm.get_messages(sid)
    assert len(msgs) == 1
