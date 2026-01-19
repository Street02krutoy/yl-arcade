import arcade


class Player(arcade.Sprite):
    def __init__(self) -> None:
        super().__init__("assets/hero completed.png", 1)
        self.dead = False
        self.movement: tuple[int, int] = (0, 0)
        self.movespeed = 3
        self.hitpoints = 100
        self.max_hp = self.hitpoints
        self.spawn_point = (128, 256)  
        self.xp = 0
        self.level = 0
        self.unspent_score = 0
        self.xp_to_next_lvl = 1
        self.center_x, self.center_y = self.spawn_point
        self.textures = [arcade.load_texture("assets/hero completed.png"), ]

    def update_movespeed_with_keys(self, keys: set[int]):
        if arcade.key.A in keys:
            self.update_movespeed(-self.movespeed, self.movement[1])
            self.scale_x = 1
        if arcade.key.S in keys:
            self.update_movespeed(self.movement[0], -self.movespeed)
        if arcade.key.D in keys:
            self.update_movespeed(self.movespeed, self.movement[1])
            self.scale_x = -1
        if arcade.key.W in keys:
            self.update_movespeed(self.movement[0], self.movespeed)
    
    def update_movespeed(self, x: int, y: int):
        self.movement = (x, y)

    def add_xp(self, xp_amount: int):
        self.xp+=xp_amount
        if self.xp >= self.xp_to_next_lvl: # type: ignore
            self.level += 1
            self.unspent_score += 1
            old_xp = self.xp - self.xp_to_next_lvl
            self.xp = 0
            self.xp_to_next_lvl = round(1.5 ** self.level)
            self.add_xp(old_xp)

        

    def reset(self):
        self.hitpoints = 100
        self.movespeed = 3
        self.center_x, self.center_y = self.spawn_point

    def damage(self, amount: float): 
        self.hitpoints -= amount


    def update_movement(self, delta_time: float):
        self.change_y =  self.movement[1]
        self.change_x = self.movement[0]
        self.movement = (0, 0)
