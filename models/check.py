from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.item import Item
    from models.menu import Menu


class Check:
    def __init__(self, items: list[Item]) -> None:
        self.items = items

    def calculate_amount(self, menu: Menu) -> float:
        total = sum(menu.get_price(item) for item in self.items)
        print(f"  Check: total is ${total:.2f}")
        return total
