from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.database import Database
    from models.item import Item
    from models.menu import Menu


class Check:
    def __init__(self, items: list[Item]) -> None:
        self.items = items
        self.total: float = 0.0

    def calculate_amount(self, menu: Menu) -> float:
        self.total = sum(menu.get_price(item) for item in self.items)
        print(f"  Check: total is ${self.total:.2f}")
        return self.total

    def save(self, db: Database) -> None:
        items_str = ", ".join(item.name for item in self.items)
        db.execute(
            "INSERT INTO checks (items, total) VALUES (?, ?)",
            (items_str, self.total),
        )
        print(f"  Check: saved to database (${self.total:.2f})")
