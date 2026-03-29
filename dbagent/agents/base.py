from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AbstractAgent(ABC):
    """Base class for all agents."""

    def __init__(self, model: str, max_retries: int = 3) -> None:
        self._model = model
        self._max_retries = max_retries

    @abstractmethod
    def process(self, user_input: str) -> dict[str, Any]:
        """Accept natural-language input and return a structured response.

        Returns a dict with at least::

            {
                "answer": str,
                "sql": str | None,
                "data": dict | None,
                "error": str | None,
            }
        """
        ...
