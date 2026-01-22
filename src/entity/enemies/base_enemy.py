import math
import arcade

from entity.player import Player



class BaseEnemy(arcade.Sprite):
    def __init__(self, damage: float, movespeed: float, texture: str, attack_speed: float, hp: float, player: Player):
        super().__init__()
        self._damage = damage
        self.movespeed = movespeed
        self.attack_speed = attack_speed
        self.max_hp = hp
        self.hp = hp
        self.player = player
        self.attack_cd = -1.0
        self.hurt_timer = -1.0


        self.textures = []
        self.textures.append(arcade.load_texture(f"assets/enemy/{texture}/idle.png"))
        self.textures.append(arcade.load_texture(f"assets/enemy/{texture}/hurt.png"))

        self.texture = self.textures[0]

    def draw_health_bar(self):
        bar_width = self.width
        bar_height = 6
        health_ratio = max(0, self.hp / self.max_hp)

        x = self.center_x - bar_width / 2
        y = self.center_y - self.height / 2 - 6

        arcade.draw_lbwh_rectangle_filled(
                x,
                y,
                bar_width,
                bar_height,
            arcade.color.DARK_RED
        )

        arcade.draw_lbwh_rectangle_filled(
            x,
            y,
            bar_width * health_ratio,
            bar_height,
            arcade.color.GREEN
        )

    def update(self, delta_time: float, enemies_list: arcade.SpriteList[arcade.Sprite]) -> None: # type: ignore
        if self.hp <= 0:
            self.kill()
        self.attack_cd -= delta_time
        if self.hurt_timer > 0:
            self.hurt_timer -= delta_time
            if self.hurt_timer <= 0:
                self.texture = self.textures[0]

        dx = self.player.center_x - self.center_x
        dy = self.player.center_y - self.center_y

        distance = math.hypot(dx, dy)

        if distance > 0:
            dx /= distance # sin
            dy /= distance # cos 
            if self.collides_with_sprite(self.player):
                self.collision_with_player()
            else:
                self.center_x += dx * self.movespeed
                self.center_y += dy * self.movespeed
                collisions = arcade.check_for_collision_with_list(self, enemies_list)
                for enemy in collisions:
                    if enemy == self:
                        continue
                    push_x = self.center_x - enemy.center_x
                    push_y = self.center_y - enemy.center_y
                    dist = math.hypot(push_x, push_y)
                    if dist > 0: 
                        push_x /= dist
                        push_y /= dist
                        self.center_x += push_x * 1.5
                        self.center_y += push_y * 1.5
                    break
        super().update(delta_time) # type: ignore
        
    
    def damage(self, amount: float):
        self.hurt_timer = 1.0
        self.texture = self.textures[1]

        self.hp -= amount
        
    def kill(self) -> None:
        self.player.add_xp(1)
        return super().kill()

    def collision_with_player(self):
        if(self.attack_cd<=0):
            self.player.damage(self._damage)
            self.attack_cd = self.attack_speed
