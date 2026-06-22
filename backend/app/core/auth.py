"""Simple local authentication with SHA256 password hashing and session TTL."""
import hashlib
import json
import os
import uuid
import time
from typing import Optional

AUTH_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "auth.json")
SESSION_TTL = 3600  # 1 hour


def _resolve_auth_path() -> str:
    return os.path.abspath(AUTH_FILE)


class SimpleAuth:
    """Simple password-based auth with in-memory session store."""

    def __init__(self):
        self._sessions: dict[str, tuple[str, float]] = {}  # token -> (username, expiry)
        self._auth_file = _resolve_auth_path()

    def is_setup(self) -> bool:
        return os.path.exists(self._auth_file)

    def setup(self, username: str, password: str) -> bool:
        if self.is_setup():
            return False
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        os.makedirs(os.path.dirname(self._auth_file), exist_ok=True)
        with open(self._auth_file, "w") as f:
            json.dump({"username": username, "password_hash": password_hash}, f)
        return True

    def verify(self, username: str, password: str) -> bool:
        if not self.is_setup():
            return False
        with open(self._auth_file) as f:
            data = json.load(f)
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return data["username"] == username and data["password_hash"] == password_hash

    def create_session(self, username: str) -> str:
        token = str(uuid.uuid4())
        self._sessions[token] = (username, time.time() + SESSION_TTL)
        return token

    def verify_session(self, token: str) -> bool:
        entry = self._sessions.get(token)
        if entry is None:
            return False
        _, expiry = entry
        if time.time() > expiry:
            del self._sessions[token]
            return False
        return True

    def iter_session(self, token: str) -> Optional[str]:
        entry = self._sessions.get(token)
        if entry is None:
            return None
        username, expiry = entry
        if time.time() > expiry:
            del self._sessions[token]
            return None
        return username

    def reset_password(self, username: str, new_password: str) -> bool:
        with open(self._auth_file) as f:
            data = json.load(f)
        data["password_hash"] = hashlib.sha256(new_password.encode()).hexdigest()
        with open(self._auth_file, "w") as f:
            json.dump(data, f)
        return True


_auth_instance: Optional[SimpleAuth] = None


def get_auth() -> SimpleAuth:
    global _auth_instance
    if _auth_instance is None:
        _auth_instance = SimpleAuth()
    return _auth_instance
