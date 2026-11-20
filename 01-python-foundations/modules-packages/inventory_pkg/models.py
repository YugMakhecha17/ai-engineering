from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    sku: str
    quantity: int
