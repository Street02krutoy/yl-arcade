import math
from pathlib import Path
from arcade import SpriteList, Texture
from entity.enemies.base_enemy import BaseEnemy
from entity.player import Player
from entity.weapons.base_weapon import BaseWeapon


class CircularRotatingWeapon(BaseWeapon):
    def __init__(self, path_or_texture: str | Path | bytes | Texture = "assets/weapons/axe.png", damage: float = 3, radius: float = 1000, speed: float = 1) -> None:
        super().__init__(path_or_texture, damage)
        self.set_stat("radius", radius/1000)
        self.set_stat("scale", 10)
        self.set_stat("attack_rate", 5)
        self.set_stat("speed", speed*10)
        self.angle = math.pi
        self.radians = 0
        

    def update(self, delta_time: float, enemies_list: SpriteList[BaseEnemy], player: Player):
        self.scale = self.get_stat("scale")/10
        self.radians += math.pi*delta_time*self.get_stat("speed")/10
        self.center_x = player.center_x + (self.get_stat("radius")*1000*math.cos(self.radians))
        self.center_y = player.center_y + (self.get_stat("radius")*1000*math.sin(self.radians))
        super().update(delta_time, enemies_list, player)
