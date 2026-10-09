from src.visual.enemy import Enemy


class Inky(Enemy):
    def __init__(self, assets, afraid, maze) -> None:
        super().__init__(assets, afraid, maze)
        self.direction = 4
        self.define_pos()

    def update_direction(self):
        ...

    def define_pos(self):
        max_x = len(self.maze.maze[0]) - 1
        max_y = len(self.maze.maze) - 1
        self.maze_pos = (max_x, max_y)
        self.pos = ((max_x - 1) * 50 + 7, (max_y) * 50 + 7)
        self.state = 0
