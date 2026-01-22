import math
import random

import arcade
from entity.enemies.base_enemy import BaseEnemy
from entity.enemies.enemy_cloud import EnemyCloud
from entity.player import Player


class GameLevel:
    def __init__(self, level: int):
        self.timer = 10*60
        self.enemies_spawned = 0
        self.spawn_base = 0.98
        self.count = level
        self.spawn_multiplier = 10.0  
        self.spawn_timer = 0.5
        self.background = arcade.Sprite(f"assets/surface/level_{level}.png")
        self.background.center_x = 640
        self.background.center_y = 360
        self.textures = ["sheep", "cloud", "ccat"][level-1]

    def get_background(self):
        return self.background

    def update(self, delta_time: float, player: Player, enemies_list: arcade.SpriteList[BaseEnemy]):
        self.spawn_timer -= delta_time
        if self.spawn_timer <= 0:
            self.spawn_enemy(player, enemies_list)
            self.enemies_spawned += 1
            self.spawn_timer = self.spawn_multiplier * (self.spawn_base ** self.enemies_spawned)
        self.timer -= delta_time


    def spawn_enemy(self, player: Player, enemies_list: arcade.SpriteList[BaseEnemy]):
        distance = random.randint(250, 1000)
        angle = random.uniform(0, 2 * math.pi)


        enemy = BaseEnemy(random.uniform(4, 8)*self.count/2,random.uniform(4, 8)*self.count/2, self.textures, random.uniform(4, 8)*self.count/2, random.uniform(4, 8)*self.count/2, player)

        enemy.center_x = math.sin(angle)*distance+player.center_x
        enemy.center_y = math.cos(angle)*distance+player.center_y
        if(enemy.collides_with_list(enemies_list)):
            self.spawn_enemy(player, enemies_list)
        else:
            enemies_list.append(enemy)

        