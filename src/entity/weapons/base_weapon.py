import random
import arcade

from entity.enemies.base_enemy import BaseEnemy
from entity.player import Player


class BaseWeapon(arcade.Sprite):
    def __init__(self, path_or_texture: str | arcade.Path | bytes | arcade.Texture, damage: float) -> None: # type: ignore
        super().__init__(path_or_texture, 0.1)
        self.damage = damage
        self._stats: dict[str, float] = {}
        self.hit_timers: dict[BaseEnemy, float] = {}

    def get_stats(self) -> dict[str, float]:
        return self._stats

    def get_stat(self, name: str) -> float:
        return self._stats[name]

    def set_stat(self, name: str, value: float) -> None:
        self._stats[name] = value

    def scale_random_stat(self) -> None:
        stat= random.choice(list(self._stats.keys()))
        print(stat)
        self._stats[stat] += random.uniform(0.8, 1.2)

    def update(self, delta_time: float, enemies_list: arcade.SpriteList[BaseEnemy], player: Player): # type: ignore
        super().update(delta_time) # type: ignore
        for enemy in list(self.hit_timers):
            self.hit_timers[enemy] -= delta_time
            if self.hit_timers[enemy] <= 0:
                del self.hit_timers[enemy]
        collisions = arcade.check_for_collision_with_list(self, enemies_list)
        for enemy in collisions:
            if not self.hit_timers.get(enemy):
                print(self.get_stats())
                self.hit_timers[enemy] = 1/self.get_stat("attack_rate")
                enemy.damage(self.damage)
          
