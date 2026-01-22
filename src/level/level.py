import math
import random

import arcade
from entity.enemies.base_enemy import BaseEnemy
from entity.enemies.enemy_cloud import EnemyCloud
from entity.player import Player


class GameLevel:
    def __init__(self, level: int):
        self.timer = 2*60
        self.enemies_spawned = 0
        self.spawn_base = 0.98
        self.count = level
        self.spawn_multiplier = 3.0  
        self.spawn_timer = 0.5
        self.background_texture = arcade.load_texture(f"assets/surface/level_{level}.png")
        self.bg_width = self.background_texture.width
        self.bg_height = self.background_texture.height

        self.background_sprites = arcade.SpriteList()
        self.last_player_x = 0
        self.last_player_y = 0

        self.textures = ["sheep", "cloud", "ccat"][level-1]

    def get_background(self):
        return self.background_sprites
    
    def update_background_tiles(self, player: Player):
        """Update background tiles to follow player"""
        tile_x = math.floor(player.center_x / self.bg_width)
        tile_y = math.floor(player.center_y / self.bg_height)
        
        if len(self.background_sprites)==0 or tile_x != math.floor(self.last_player_x / self.bg_width) or tile_y != math.floor(self.last_player_y / self.bg_height):
            self.background_sprites.clear()
            
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    bg_sprite = arcade.Sprite(self.background_texture)
                    bg_sprite.center_x = (tile_x + dx) * self.bg_width + self.bg_width // 2
                    bg_sprite.center_y = (tile_y + dy) * self.bg_height + self.bg_height // 2
                    self.background_sprites.append(bg_sprite)
        
        self.last_player_x = player.center_x
        self.last_player_y = player.center_y

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

        