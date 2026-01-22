import random
from arcade import gui

from entity.player import Player
from entity.weapons.weapon_list import WeaponList
from inventory.inventory import Inventory
from inventory.item import InventoryWeapon

LOC = {"radius":"радиус",
"scale": "размер",
"attack_rate": "скорость атаки",
"speed": "скорость", "damage": "урон"}

class LevelUpLayout(gui.UIBoxLayout):
    def __init__(self, player: Player, screen_size: tuple[int, int], inventory: Inventory):
        self.player = player
        self.inventory = inventory
        # Vertical layout (one column)
        super().__init__( # type: ignore
            x=int(screen_size[0]/2-110),
            y=int(screen_size[1]/2-75),
            vertical=True,
            space_between=12
        )
        self.items = []
        self.stats: list[tuple[str, float]] = []

        # Buttons
        self.button_1 = gui.UIFlatButton(
            text="Button 1",
            width=220,
            height=50
        )
        self.button_2 = gui.UIFlatButton(
            text="Button 2",
            width=220,
            height=50
        )
        self.button_3 = gui.UIFlatButton(
            text="Button 3",
            width=220,
            height=50
        )

        self.button_1.on_click = lambda event: self.on_click(event,0)
        self.button_2.on_click = lambda event: self.on_click(event,1)
        self.button_3.on_click = lambda event: self.on_click(event,2)

        # Add buttons to layout
        self.add(self.button_1)
        self.add(self.button_2)
        self.add(self.button_3)

    def on_click(self, event: gui.UIOnClickEvent, button_index: int) -> None:
        if self.player.unspent_score > 0:
            self.player.unspent_score -= 1
            if not self.items[button_index] in self.inventory.get():
                self.inventory.add(self.items[button_index])
            else:
                self.items[button_index].weapon.set_stat(self.stats[button_index][0], self.items[button_index].weapon.get_stat(self.stats[button_index][0])+self.stats[button_index][1])
            self.update_items()
        print(f"Button {button_index} clicked")


    def update_items(self):
        inv = self.inventory.get()
        self.items = random.sample(tuple(inv), min(len(inv),3))
        print(self.stats)

        self.stats = list(map(lambda x: (x.weapon.get_random_stat(), random.randint(5, 20)/10), self.items))

        while len(self.items) != 3:
            self.items.append(WeaponList().get_random_weapon())
            self.stats.append(("new", 0))        


        self.button_1.text = button_text(self.items[0], self.stats[0])
        self.button_2.text = button_text(self.items[1], self.stats[1])
        self.button_3.text = button_text(self.items[2], self.stats[2])

        pass

    
def button_text(item: InventoryWeapon, stat: tuple[str, float]):
    if stat[0] == "new":
        return f"Создать {item.name}"
    return f"{item.name}: {LOC[stat[0]]} +{stat[1]} "