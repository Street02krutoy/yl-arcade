class GameLevel:
    def __init__(self, enemies_amount: int):
        self.timer = 10*60
        self.enemies_remaining = enemies_amount

    def update(self, delta_time: float):
        self.timer -= delta_time
        