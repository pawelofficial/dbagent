from __future__ import annotations

from typing import Any

from dbagent.skills.base import AbstractSkill


class SQLSkill(AbstractSkill):
    """Validates, parses, and sanitises SQL before execution."""

    # ------------------------------------------------------------------
    # AbstractSkill interface
    # ------------------------------------------------------------------

    def execute(self, input: dict[str, Any]) -> dict[str, Any]:
        """Entry point: expects ``{"sql": str}``, returns validation result."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def validate(self, sql: str) -> bool:
        """Return True if *sql* is syntactically valid and read-only."""
        raise NotImplementedError

    def parse(self, sql: str) -> dict[str, Any]:
        """Parse *sql* and return structural metadata (tables, columns, etc.)."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _is_read_only(self, sql: str) -> bool:
        """Return True if *sql* contains only SELECT / PRAGMA / EXPLAIN."""
        raise NotImplementedError

    def _sanitize(self, sql: str) -> str:
        """Strip dangerous patterns and normalise whitespace."""
        raise NotImplementedError
