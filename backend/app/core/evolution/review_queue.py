"""Review queue for extracted facts."""
import json
import sqlite3
import uuid
import os
from typing import List, Dict, Optional
from datetime import datetime


class ReviewQueue:
    """Queue of facts pending human review."""

    def __init__(self, db_path: str = "data/review_queue.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        self.conn.execute("""CREATE TABLE IF NOT EXISTS review_queue (
            id TEXT PRIMARY KEY,
            fact_type TEXT,
            content TEXT,
            confidence REAL,
            source TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT,
            reviewed_at TEXT
        )""")
        self.conn.commit()

    def add_facts(self, facts: List[Dict]) -> List[str]:
        ids = []
        for fact in facts:
            fid = str(uuid.uuid4())[:8]
            self.conn.execute(
                "INSERT INTO review_queue (id, fact_type, content, confidence, source, created_at) "
                "VALUES (?,?,?,?,?,?)",
                (
                    fid,
                    fact.get("fact_type", "other"),
                    fact.get("content", ""),
                    fact.get("confidence", 0.5),
                    fact.get("source", ""),
                    datetime.now().isoformat(),
                ),
            )
            ids.append(fid)
        self.conn.commit()
        return ids

    def get_pending(self, limit: int = 20) -> List[Dict]:
        rows = self.conn.execute(
            "SELECT * FROM review_queue WHERE status='pending' ORDER BY confidence DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]

    def approve(self, fact_id: str) -> bool:
        self.conn.execute(
            "UPDATE review_queue SET status='approved', reviewed_at=? WHERE id=?",
            (datetime.now().isoformat(), fact_id),
        )
        self.conn.commit()
        return True

    def reject(self, fact_id: str) -> bool:
        self.conn.execute(
            "UPDATE review_queue SET status='rejected', reviewed_at=? WHERE id=?",
            (datetime.now().isoformat(), fact_id),
        )
        self.conn.commit()
        return True

    def get_approved(self) -> List[Dict]:
        rows = self.conn.execute(
            "SELECT * FROM review_queue WHERE status='approved'"
        ).fetchall()
        return [dict(r) for r in rows]
