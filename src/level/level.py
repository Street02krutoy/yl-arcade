class GameLevel:
    def __init__(self):
        self.timer = 10*60

    def update(self, delta_time: float):
        self.timer -= delta_time
        