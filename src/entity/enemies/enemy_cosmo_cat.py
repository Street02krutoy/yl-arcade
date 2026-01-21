import math
import random
import arcade

from entity.enemies.base_enemy import BaseEnemy
from entity.player import Player

PathOrTexture = str | arcade.Path | bytes | arcade.Texture | None  # type: ignore


class EnemyCloud(BaseEnemy):
    def __init__(self, player: Player):
        super().__init__(1.5, random.randint(2, 3), "cat", 0.6, 5, player)