import math
import random

import arcade
from entity.enemies.base_enemy import BaseEnemy
from entity.player import Player


class GameLevel:
    def __init__(self, enemies_amount: int):
        self.timer = 10*60
        self.enemies_remaining = enemies_amount
        self.spawn_rate = enemies_amount/self.timer
        self.spawn_timer = self.spawn_rate

    def update(self, delta_time: float, player: Player, enemies_list: arcade.SpriteList[BaseEnemy]):
        self.spawn_timer -= delta_time
        if self.spawn_timer <= 0:
            self.spawn_enemy(player, enemies_list)
            self.spawn_timer = self.spawn_rate
        self.timer -= delta_time

    def spawn_enemy(self, player: Player, enemies_list: arcade.SpriteList[BaseEnemy]):
        distance = random.randint(100, 500)
        angle = random.uniform(0, 2 * math.pi)
        enemy_damage = random.randint(6, 12)

        enemy = BaseEnemy(enemy_damage, 12 - enemy_damage, "assets/deadass.png", enemy_damage/2)

        enemy.center_x = math.sin(angle)*distance+player.center_x
        enemy.center_y = math.cos(angle)*distance+player.center_y
        if(enemy.collides_with_list(enemies_list)):
            self.spawn_enemy(player, enemies_list)
        else:
            enemies_list.append(enemy)

        