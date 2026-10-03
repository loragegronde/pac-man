from src.visual.enemy import Enemy


class Blinky(Enemy):
    def __init__(self, assets, afraid, maze) -> None:
        super().__init__(assets, afraid, maze)
        self.direction = 2
        self.define_pos()

    def update_direction(self):
        ...

    def define_pos(self):
        self.maze_pos = (1, 0)
        self.pos = (57, 7)
