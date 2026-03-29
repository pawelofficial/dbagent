from __future__ import annotations

import sqlite3
import uuid
from datetime import datetime
from typing import Any


class ChatStore:
    """SQLite-backed persistence for chat sessions and messages."""

    def __init__(self, db_path: str) -> None:
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._init_db()

    def _init_db(self) -> None:
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS chats (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT NOT NULL REFERENCES chats(id),
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_messages_chat
                ON messages(chat_id);
        """)

    def create_chat(self, title: str = "New chat") -> str:
        chat_id = uuid.uuid4().hex[:12]
        now = datetime.utcnow().isoformat()
        self._conn.execute(
            "INSERT INTO chats (id, title, created_at) VALUES (?, ?, ?)",
            (chat_id, title, now),
        )
        self._conn.commit()
        return chat_id

    def list_chats(self) -> list[dict[str, Any]]:
        rows = self._conn.execute("""
            SELECT c.id, c.title, c.created_at,
                   COUNT(m.id) AS message_count
            FROM chats c
            LEFT JOIN messages m ON m.chat_id = c.id
            GROUP BY c.id
            ORDER BY c.created_at DESC
        """).fetchall()
        return [dict(r) for r in rows]

    def get_chat(self, chat_id: str) -> dict[str, Any] | None:
        row = self._conn.execute(
            "SELECT id, title, created_at FROM chats WHERE id = ?",
            (chat_id,),
        ).fetchone()
        if row is None:
            return None
        chat = dict(row)
        msgs = self._conn.execute(
            "SELECT role, content, timestamp FROM messages "
            "WHERE chat_id = ? ORDER BY id",
            (chat_id,),
        ).fetchall()
        chat["messages"] = [dict(m) for m in msgs]
        return chat

    def add_message(
        self,
        chat_id: str,
        role: str,
        content: str,
        timestamp: str | None = None,
    ) -> None:
        ts = timestamp or datetime.utcnow().isoformat()
        self._conn.execute(
            "INSERT INTO messages (chat_id, role, content, timestamp) "
            "VALUES (?, ?, ?, ?)",
            (chat_id, role, content, ts),
        )
        self._conn.commit()

    def update_title(self, chat_id: str, title: str) -> None:
        self._conn.execute(
            "UPDATE chats SET title = ? WHERE id = ?",
            (title, chat_id),
        )
        self._conn.commit()

    def chat_exists(self, chat_id: str) -> bool:
        row = self._conn.execute(
            "SELECT 1 FROM chats WHERE id = ?", (chat_id,)
        ).fetchone()
        return row is not None

    def close(self) -> None:
        self._conn.close()
