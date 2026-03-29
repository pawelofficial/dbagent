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
        """Open (or return existing) SQLite connection."""
        raise NotImplementedError

    def get_schema(self) -> dict[str, Any]:
        """Return full database schema as a nested dict.

        Expected shape::

            {
                "tables": {
                    "<name>": {
                        "columns": [...],
                        "primary_key": [...],
                        "foreign_keys": [...]
                    }
                }
            }
        """
        raise NotImplementedError

    def get_table_info(self, table_name: str) -> dict[str, Any]:
        """Return column/key metadata for a single table."""
        raise NotImplementedError

    def execute(self, query: str) -> list[dict[str, Any]]:
        """Execute a read-only SQL query and return rows as dicts."""
        raise NotImplementedError

    def close(self) -> None:
        """Close the underlying connection."""
        raise NotImplementedError
