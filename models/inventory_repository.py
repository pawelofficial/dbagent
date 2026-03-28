from models.database import Database
from models.inventory import Inventory
from models.item import Item


class InventoryRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

    def load_inventory(self) -> Inventory:
        rows = self._db.query("SELECT name, price, availability FROM items")
        items = [
            Item(row["name"], price=row["price"], availability=bool(row["availability"]))
            for row in rows
        ]
        print(f"  InventoryRepository: loaded {len(items)} items from DB")
        return Inventory(items)
