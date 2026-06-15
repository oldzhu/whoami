"""SQLite-backed conversation session CRUD."""
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class SessionManager:
    """Manages conversation sessions with SQLite persistence."""

    SCHEMA = """
    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY, title TEXT DEFAULT '',
        created_at TEXT, updated_at TEXT
    );
    CREATE TABLE IF NOT EXISTS messages (
        id TEXT PRIMARY KEY, session_id TEXT,
        role TEXT, content TEXT, timestamp TEXT,
        FOREIGN KEY(session_id) REFERENCES sessions(id)
    );
    """

    def __init__(self, db_path: str = "data/sessions.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_db(self):
        with self._connect() as conn:
            conn.executescript(self.SCHEMA)

    def create_session(self, title: str = "") -> str:
        session_id = uuid.uuid4().hex
        now = datetime.now().isoformat()
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO sessions (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
                (session_id, title, now, now),
            )
        return session_id

    def get_session(self, session_id: str) -> Optional[Dict]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM sessions WHERE id = ?", (session_id,)
            ).fetchone()
            if not row:
                return None
            session = dict(row)
            messages = conn.execute(
                "SELECT * FROM messages WHERE session_id = ? ORDER BY timestamp ASC",
                (session_id,),
            ).fetchall()
            session["messages"] = [dict(m) for m in messages]
            return session

    def list_sessions(self) -> List[Dict]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM sessions ORDER BY updated_at DESC"
            ).fetchall()
            return [dict(r) for r in rows]

    def add_message(self, session_id: str, role: str, content: str) -> Dict:
        msg_id = uuid.uuid4().hex
        timestamp = datetime.now().isoformat()
        now = timestamp
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO messages (id, session_id, role, content, timestamp) VALUES (?, ?, ?, ?, ?)",
                (msg_id, session_id, role, content, timestamp),
            )
            conn.execute(
                "UPDATE sessions SET updated_at = ? WHERE id = ?",
                (now, session_id),
            )
        return {
            "id": msg_id,
            "session_id": session_id,
            "role": role,
            "content": content,
            "timestamp": timestamp,
        }

    def delete_session(self, session_id: str):
        with self._connect() as conn:
            conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
            conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))

    def get_messages(self, session_id: str, limit: int = 50) -> List[Dict]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM messages WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?",
                (session_id, limit),
            ).fetchall()
            return [dict(r) for r in reversed(rows)]
