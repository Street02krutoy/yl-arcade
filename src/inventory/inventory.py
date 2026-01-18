from inventory.item import InventoryWeapon


class Inventory():
    def __init__(self) -> None:
        self._inv: set[InventoryWeapon] = set()

    def add(self, item: InventoryWeapon):
        self._inv.add(item)
    
    def get(self):
        return self._inv