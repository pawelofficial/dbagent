from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.item import Item


class Menu:
    def __init__(self, prices: dict[str, float]) -> None:
        self.prices = prices

    def get_price(self, item: Item) -> float:
        return self.prices.get(item.name, 0.0)
