from __future__ import annotations

from typing import Any

from dbagent.skills.base import AbstractSkill
from dbagent.db import DB


class DataSkill(AbstractSkill):
    """Executes validated SQL and formats the result set."""

    def __init__(self, db: DB) -> None:
        self._db = db

    # ------------------------------------------------------------------
    # AbstractSkill interface
    # ------------------------------------------------------------------

    def execute(self, input: dict[str, Any]) -> dict[str, Any]:
        """Entry point: expects ``{"sql": str}``, returns data dict."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def run_query(self, sql: str) -> dict[str, Any]:
        """Execute *sql* via the DB layer and return formatted results.

        Returns::

            {
                "columns": list[str],
                "rows": list[dict],
                "row_count": int,
            }
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _format_results(
        self,
        rows: list[tuple[Any, ...]],
        columns: list[str],
    ) -> dict[str, Any]:
        """Convert raw rows + column names into the standard result dict."""
        raise NotImplementedError

    def _handle_error(self, error: Exception) -> dict[str, Any]:
        """Wrap an execution error into a structured error response."""
        raise NotImplementedError
