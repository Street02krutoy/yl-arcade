import random

from entity.weapons.burning_weapon import BurningWeapon
from entity.weapons.circular_rotating_weapon import CircularRotatingWeapon
from inventory.item import InventoryWeapon


class WeaponList():
    def __init__(self):
        pass

    def get_random_weapon(self) -> InventoryWeapon:
        return random.choice((InventoryWeapon("Аура",BurningWeapon()), InventoryWeapon("Пила", CircularRotatingWeapon())))