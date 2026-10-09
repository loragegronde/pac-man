from src.visual.enemy import Enemy


class Clyde(Enemy):
    def __init__(self, assets, afraid, maze) -> None:
        super().__init__(assets, afraid, maze)
        self.direction = 2
        self.define_pos()

    def update_direction(self):
        ...

    def define_pos(self):
        max_x = len(self.maze.maze[0]) - 1
        self.maze_pos = (max_x, 1)
        self.pos = (max_x * 50 + 7, 57)
        self.state = 0
