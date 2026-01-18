import random
from arcade import gui

from entity.player import Player
from entity.weapons.weapon_list import WeaponList
from inventory.inventory import Inventory


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
            self.inventory.add(self.items[button_index])
            self.update_items()
        print(f"Button {button_index} clicked")


    def update_items(self):
        inv = self.inventory.get()
        self.items = random.sample(tuple(inv), min(len(inv),3))

        while len(self.items) != 3:
            self.items.append(WeaponList().get_random_weapon())

        self.button_1.text = self.items[0].name
        self.button_2.text = self.items[1].name
        self.button_3.text = self.items[2].name

        pass