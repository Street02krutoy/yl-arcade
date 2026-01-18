import math
from pathlib import Path
from arcade import SpriteList, Texture
from entity.enemies.base_enemy import BaseEnemy
from entity.player import Player
from entity.weapons.base_weapon import BaseWeapon


class BurningWeapon(BaseWeapon):
    def __init__(self, path_or_texture: str | Path | bytes | Texture = "assets/circle.png", damage: float = 1, radius: float = 50, attack_rate: float = 1) -> None:
        super().__init__(path_or_texture, damage)
        self.set_stat("radius", radius)
        self.set_stat("scale", 1)
        self.set_stat("attack_rate", attack_rate)
        self.angle = math.pi

    def update(self, delta_time: float, enemies_list: SpriteList[BaseEnemy], player: Player):
        self.scale = self.get_stat("scale")/10
        self.center_x = player.center_x 
        self.center_y = player.center_y 
        super().update(delta_time, enemies_list, player)
