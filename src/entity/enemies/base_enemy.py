import math
import arcade

from entity.player import Player

PathOrTexture = str | arcade.Path | bytes | arcade.Texture | None # type: ignore


class BaseEnemy(arcade.Sprite):

    def __init__(self, damage: float, movespeed: float, texture: PathOrTexture, attack_speed: float):
        super().__init__(texture)
        self.damage = damage
        self.movespeed = movespeed
        self.attack_speed = attack_speed
        self.attack_cd = -1.0

    def update(self, delta_time: float, player: Player, enemies_list: arcade.SpriteList[arcade.Sprite]) -> None: # type: ignore
        super().update(delta_time) # type: ignore
        self.attack_cd -= delta_time
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y

        distance = math.hypot(dx, dy)

        if distance > 0:
            dx /= distance
            dy /= distance
            if self.collides_with_sprite(player):
                self.collision_with_player(player)
            else:
                old_x = self.center_x
                old_y = self.center_y
                self.center_x += dx * self.movespeed
                self.center_y += dy * self.movespeed
                collisions = arcade.check_for_collision_with_list(self, enemies_list)
                for enemy in collisions:
                    if enemy == self:
                        continue
                    self.center_x = old_x
                    self.center_y = old_y
                    break



    def collision_with_player(self, player: Player):
        if(self.attack_cd<=0):
            player.damage(self.damage)
            self.attack_cd = self.attack_speed
