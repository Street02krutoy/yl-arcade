import arcade

from entity.player import Player


class BaseEnemy(arcade.Sprite):
    def collision_with_player(self, player: Player):
        player.hitpoints -= 1