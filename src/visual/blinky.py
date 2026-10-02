from src.visual.enemy import Enemy


class Blinky(Enemy):
    def __init__(self, assets, afraid, maze) -> None:
        super().__init__(assets, afraid, maze)
        self.maze_pos = (0, 0)
        self.pos = (57, 7)
        self.direction = 4

    def update_direction(self):
        ...
