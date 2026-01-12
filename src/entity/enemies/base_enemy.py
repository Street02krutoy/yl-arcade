import math
import arcade

from entity.player import Player

PathOrTexture = str | arcade.Path | bytes | arcade.Texture | None # type: ignore


class BaseEnemy(arcade.Sprite):

    def __init__(self, damage: float, movespeed: float, texture: PathOrTexture):
        super().__init__(texture)
        self.damage = damage
        self.movespeed = movespeed

    def update(self, delta_time: float, player: Player) -> None:
        super().update(delta_time) # type: ignore
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y

        # Distance
        distance = math.hypot(dx, dy)

        if distance > 0:
            # Normalize direction
            dx /= distance
            dy /= distance

            # Move enemy toward player
            self.center_x += dx * self.movespeed
            self.center_y += dy * self.movespeed
        if self.collides_with_sprite(player):
            self.collision_with_player(player)

    def collision_with_player(self, player: Player):
        player.damage(self.damage)
        self.center_x -= self.movespeed*10
        self.center_y -= self.movespeed*10