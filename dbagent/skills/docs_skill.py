from __future__ import annotations

from typing import Any

from dbagent.skills.base import AbstractSkill
from dbagent.db import DB


class DocsSkill(AbstractSkill):
    """Retrieves schema documentation and table descriptions for LLM context."""

    def __init__(self, db: DB) -> None:
        self._db = db

    # ------------------------------------------------------------------
    # AbstractSkill interface
    # ------------------------------------------------------------------

    def execute(self, input: dict[str, Any]) -> dict[str, Any]:
        """Entry point: expects ``{"question": str}``, returns context dict."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def get_relevant_docs(self, question: str) -> str:
        """Return a text block of schema + descriptions relevant to *question*."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _get_schema_context(self) -> str:
        """Build a formatted string of the full DB schema."""
        raise NotImplementedError

    def _get_table_descriptions(self) -> dict[str, str]:
        """Return ``{table_name: human-readable description}``."""
        raise NotImplementedError
