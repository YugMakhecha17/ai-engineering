"""Entry point for `python -m inventory_pkg`."""

from . import Inventory
from .report import render


def main() -> None:
    inventory = Inventory()
    inventory.add("widget", 3)
    inventory.add("gadget", 1)
    inventory.add("widget", 2)
    print(render(inventory))


if __name__ == "__main__":  # False when this module is imported, True when run as the program
    main()
