import math
import random
import arcade

from entity.enemies.base_enemy import BaseEnemy
from entity.player import Player


class EnemyCloud(BaseEnemy):
    def __init__(self, player: Player):
        super().__init__(1.5, random.randint(2, 3), "cloud", 0.6, 5, player)


