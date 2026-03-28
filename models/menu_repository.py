from models.database import Database
from models.menu import Menu


class MenuRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

    def load_menu(self) -> Menu:
        rows = self._db.query("SELECT item_name, price FROM menu")
        prices = {row["item_name"]: row["price"] for row in rows}
        print(f"  MenuRepository: loaded {len(prices)} menu items from DB")
        return Menu(prices)
