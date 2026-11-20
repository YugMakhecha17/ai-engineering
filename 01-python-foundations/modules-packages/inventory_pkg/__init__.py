"""inventory_pkg: a tiny package demonstrating modules, relative imports and __main__.

Importing a package executes this file once. Keep it cheap and side-effect free,
and use it to define the public API.
"""

from .models import Item
from .service import Inventory

__all__ = ["Inventory", "Item"]
