from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AbstractSkill(ABC):
    """Base class for agent skills."""

    @abstractmethod
    def execute(self, input: dict[str, Any]) -> dict[str, Any]:
        """Run the skill and return a structured result."""
        ...
