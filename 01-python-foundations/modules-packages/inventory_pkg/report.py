from inventory_pkg.service import Inventory  # absolute import: always names the full path


def render(inventory: Inventory) -> str:
    return "\n".join(f"{sku}: {inventory.quantity(sku)}" for sku in inventory.skus())
