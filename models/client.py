from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.item import Item
    from models.order import Order
    from models.waiter import Waiter


class Client:
    def __init__(self, name: str) -> None:
        self.name = name

    def greets(self, waiter: Waiter) -> None:
        print(f"  {self.name}: Hello, {waiter.name}!")

    def orders_item(self, item: Item) -> Item:
        print(f"  {self.name}: I'd like the {item.name}, please.")
        return item

    def place_order(self, order: Order, waiter: Waiter) -> None:
        print(f"  {self.name}: Here is my order.")
        waiter.receive_order(order)

    def ask_for_check(self, waiter: Waiter) -> None:
        print(f"  {self.name}: Can I get the check?")
