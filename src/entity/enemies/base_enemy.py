import arcade

from entity.player import Player

PathOrTexture = str | arcade.Path | bytes | arcade.Texture | None # type: ignore


class BaseEnemy(arcade.Sprite):

    def __init__(self, damage: int, movespeed: int, texture: PathOrTexture):
        super().__init__(texture)
        self.damage = damage
        self.movespeed = movespeed
    def collision_with_player(self, player: Player):
        player.hitpoints -= self.damage