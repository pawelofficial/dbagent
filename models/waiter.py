from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.check import Check
    from models.client import Client
    from models.database import Database
    from models.inventory import Inventory
    from models.item import Item
    from models.menu import Menu
    from models.order import Order


class Waiter:
    def __init__(self, name: str) -> None:
        self.name = name
        self._current_order: Order | None = None

    def greets(self, client: Client) -> None:
        print(f"  {self.name}: Welcome, {client.name}!")

    def receive_order(self, order: Order) -> None:
        self._current_order = order
        print(f"  {self.name}: Got it, one moment.")

    def _check_availability(self, item: Item, inventory: Inventory) -> bool:
        available = inventory.check_availability(item)
        status = "available" if available else "not available"
        print(f"  {self.name}: {item.name} is {status}.")
        return available

    def check_and_add(self, item: Item, order: Order, inventory: Inventory) -> bool:
        if not self._check_availability(item, inventory):
            print(f"  {self.name}: Sorry, {item.name} is unavailable.")
            return False
        order.add_item(item)
        return True

    def confirm(self, client: Client) -> None:
        print(f"  {self.name}: {client.name}, your order is confirmed!")

    def give_check(self, client: Client, check: Check) -> None:
        print(f"  {self.name}: Here is your check, {client.name}.")

    def prepare_check(self, order: Order, menu: Menu, db: Database | None = None) -> Check:
        from models.check import Check
        check = Check(order.items)
        check.calculate_amount(menu)
        if db is not None:
            check.save(db)
        return check
