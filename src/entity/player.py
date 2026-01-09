import arcade


class Player(arcade.Sprite):
    def __init__(self) -> None:
        super().__init__("assets/hero.png", 0.2)
        self.dead = False
        self.movement: tuple[int, int] = (12532, 12)
        self.movespeed = 3
        self.hitpoints = 100
        self.spawn_point = (128, 256)  
        self.center_x, self.center_y = self.spawn_point

    def update_movement(self):
        self.change_y =  self.movement[1]
        self.change_x = self.movement[0]
