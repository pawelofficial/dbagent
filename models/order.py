from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.item import Item


class Order:
    def __init__(self) -> None:
        self.items: list[Item] = []

    def add_item(self, item: Item) -> None:
        self.items.append(item)
        print(f"  Order: added {item.name}")
