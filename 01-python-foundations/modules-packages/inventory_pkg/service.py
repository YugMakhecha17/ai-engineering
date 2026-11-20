from .models import Item  # relative import: resolved against this module's package


class Inventory:
    def __init__(self) -> None:
        self._items: dict[str, Item] = {}

    def add(self, sku: str, quantity: int) -> None:
        if quantity < 1:
            raise ValueError("quantity must be >= 1")
        existing = self._items.get(sku)
        total = quantity + (existing.quantity if existing else 0)
        self._items[sku] = Item(sku, total)

    def quantity(self, sku: str) -> int:
        item = self._items.get(sku)
        return item.quantity if item else 0

    def skus(self) -> list[str]:
        return sorted(self._items)
