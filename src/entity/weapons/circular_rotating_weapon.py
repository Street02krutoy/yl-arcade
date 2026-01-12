import math
from pathlib import Path
from arcade import SpriteList, Texture
from entity.enemies.base_enemy import BaseEnemy
from entity.player import Player
from entity.weapons.base_weapon import BaseWeapon


class CircularRotatingWeapon(BaseWeapon):
    def __init__(self, path_or_texture: str | Path | bytes | Texture, damage: float, radius: float, speed: float = 1) -> None:
        super().__init__(path_or_texture, damage)
        self.radius = radius
        self._speed = speed
        self.angle = math.pi

    def update(self, delta_time: float, enemies_list: SpriteList[BaseEnemy], player: Player):
        self.angle += math.pi*delta_time*self._speed
        self.center_x = player.center_x + ((self.radius)*math.cos(self.angle))
        self.center_y = player.center_y + ((self.radius)*math.sin(self.angle))
        super().update(delta_time, enemies_list, player)
