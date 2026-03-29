from __future__ import annotations

import sqlite3


class Database:
    def __init__(self, connection_string: str = ":memory:") -> None:
        self.connection_string = connection_string
        self._conn: sqlite3.Connection | None = None

    def connect(self) -> None:
        self._conn = sqlite3.connect(self.connection_string)
        self._conn.row_factory = sqlite3.Row

    def query(self, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
        if self._conn is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        cursor = self._conn.execute(sql, params)
        return cursor.fetchall()

    def execute(self, sql: str, params: tuple = ()) -> None:
        if self._conn is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        self._conn.execute(sql, params)
        self._conn.commit()

    def seed(self) -> None:
        """Create tables and insert sample restaurant data."""
        self.execute(
            "CREATE TABLE IF NOT EXISTS items ("
            "  name TEXT PRIMARY KEY,"
            "  price REAL NOT NULL,"
            "  availability INTEGER NOT NULL"
            ")"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS menu ("
            "  item_name TEXT PRIMARY KEY,"
            "  price REAL NOT NULL"
            ")"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS checks ("
            "  id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "  items TEXT NOT NULL,"
            "  total REAL NOT NULL"
            ")"
        )
        sample_items = [
            ("pizza", 12.50, 1),
            ("pasta", 9.00, 1),
            ("sushi", 15.00, 0),
        ]
        for name, price, avail in sample_items:
            self.execute(
                "INSERT OR IGNORE INTO items (name, price, availability) VALUES (?, ?, ?)",
                (name, price, avail),
            )
            self.execute(
                "INSERT OR IGNORE INTO menu (item_name, price) VALUES (?, ?)",
                (name, price),
            )
