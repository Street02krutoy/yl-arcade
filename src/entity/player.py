import arcade


class Player(arcade.Sprite):
    def __init__(self) -> None:
        super().__init__("assets/hero.png", 0.2)
        self.dead = False
        self.movement: tuple[int, int] = (0, 0)
        self.movespeed = 3
        self.hitpoints = 100
        self.spawn_point = (128, 256)  
        self.center_x, self.center_y = self.spawn_point

    def update_movespeed_with_keys(self, keys: set[int]):
        if arcade.key.A in keys:
            self.update_movespeed(-self.movespeed, self.movement[1])
        if arcade.key.S in keys:
            self.update_movespeed(self.movement[0], -self.movespeed)
        if arcade.key.D in keys:
            self.update_movespeed(self.movespeed, self.movement[1])
        if arcade.key.W in keys:
            self.update_movespeed(self.movement[0], self.movespeed)
    
    def update_movespeed(self, x: int, y: int):
        self.movement = (x, y)


    def update_movement(self):
        self.change_y =  self.movement[1]
        self.change_x = self.movement[0]
        self.movement = (0, 0)
