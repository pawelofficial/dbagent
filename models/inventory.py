from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.item import Item


class Inventory:
    def __init__(self, items: list[Item]) -> None:
        self.items = items

    def check_availability(self, item: Item) -> bool:
        for stocked in self.items:
            if stocked.name == item.name and stocked.availability:
                return True
        return False
