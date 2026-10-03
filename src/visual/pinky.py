from src.visual.enemy import Enemy


class Pinky(Enemy):
    def __init__(self, assets, afraid, maze) -> None:
        super().__init__(assets, afraid, maze)
        self.direction = 8
        self.define_pos()

    def update_direction(self):
        ...

    def define_pos(self):
        max_y = len(self.maze.maze) - 1
        self.maze_pos = (0, max_y - 1)
        self.pos = (7, (max_y - 1) * 50 + 7)
