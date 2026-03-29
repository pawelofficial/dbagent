from __future__ import annotations

from typing import Any

from dbagent.agents.base import AbstractAgent
from dbagent.db import DB
from dbagent.skills.docs_skill import DocsSkill
from dbagent.skills.sql_skill import SQLSkill
from dbagent.skills.data_skill import DataSkill
from dbagent.config import LLM_MODEL, MAX_RETRIES


class DBAgent(AbstractAgent):
    """Orchestrates skills and owns the LLM conversation loop."""

    def __init__(
        self,
        db: DB,
        model: str = LLM_MODEL,
        max_retries: int = MAX_RETRIES,
    ) -> None:
        super().__init__(model=model, max_retries=max_retries)
        self._db = db
        self._docs_skill = DocsSkill(db=db)
        self._sql_skill = SQLSkill()
        self._data_skill = DataSkill(db=db)
        self._conversation_history: list[dict[str, str]] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process(self, user_input: str) -> dict[str, Any]:
        """Full pipeline: docs -> LLM -> SQL validate -> execute -> respond.

        Steps:
            1. Retrieve schema/docs context via DocsSkill
            2. Call LLM to generate SQL
            3. Validate/sanitise via SQLSkill
            4. Execute via DataSkill
            5. Return structured result (or enter retry loop on error)
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _call_llm(self, prompt: str, context: str) -> str:
        """Send prompt + context to the configured LLM and return raw text."""
        raise NotImplementedError

    def _retry_loop(
        self,
        question: str,
        context: str,
        error: str,
    ) -> dict[str, Any]:
        """Re-prompt the LLM up to *max_retries* times on query failure."""
        raise NotImplementedError
