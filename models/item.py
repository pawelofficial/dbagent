class Item:
    def __init__(self, name: str, price: float = 0.0, availability: bool = True) -> None:
        self.name = name
        self.price = price
        self.availability = availability

    def __repr__(self) -> str:
        return f"Item({self.name!r}, price={self.price}, available={self.availability})"
