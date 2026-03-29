from __future__ import annotations

import sqlite3
from typing import Any

from dbagent.config import DB_PATH


class DB:
    """SQLite connection wrapper with schema introspection."""

    def __init__(self, db_path: str = DB_PATH) -> None:
        self._db_path = db_path
        self._connection: sqlite3.Connection | None = None

    def connect(self) -> sqlite3.Connection:
        if self._connection is None:
            self._connection = sqlite3.connect(
                self._db_path, check_same_thread=False
            )
            self._connection.row_factory = sqlite3.Row
            self._connection.execute("PRAGMA foreign_keys=ON")
        return self._connection

    def get_schema(self) -> dict[str, Any]:
        conn = self.connect()
        tables_raw = conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name NOT LIKE 'sqlite_%' "
            "ORDER BY name"
        ).fetchall()

        tables: dict[str, Any] = {}
        for (name,) in tables_raw:
            tables[name] = self.get_table_info(name)

        return {"tables": tables}

    def get_table_info(self, table_name: str) -> dict[str, Any]:
        conn = self.connect()

        columns = []
        pk_cols = []
        for row in conn.execute(f"PRAGMA table_info('{table_name}')").fetchall():
            col = {
                "name": row["name"],
                "type": row["type"],
                "notnull": bool(row["notnull"]),
                "default": row["dflt_value"],
            }
            columns.append(col)
            if row["pk"]:
                pk_cols.append(row["name"])

        fk_rows = conn.execute(
            f"PRAGMA foreign_key_list('{table_name}')"
        ).fetchall()
        foreign_keys = [
            {"from": fk["from"], "table": fk["table"], "to": fk["to"]}
            for fk in fk_rows
        ]

        return {
            "columns": columns,
            "primary_key": pk_cols,
            "foreign_keys": foreign_keys,
        }

    def execute(self, query: str) -> list[dict[str, Any]]:
        conn = self.connect()
        cursor = conn.execute(query)
        if cursor.description is None:
            return []
        cols = [d[0] for d in cursor.description]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None
