from abc import ABC, abstractmethod


class Enemy(ABC):
    maze_pos: tuple[int, int]
    pos: tuple[int, int]

    def __init__(self, assets, afraid, maze) -> None:
        self.direction: int = 1
        self.assets = assets
        self.afraid = afraid
        self.maze = maze
        self.update_direction()
        self.vector: dict[int, tuple[int, int]] = {
            8: (-1, 0),
            4: (0, 1),
            2: (1, 0),
            1: (0, -1),
        }

    @abstractmethod
    def update_direction(self):
        ...

    def update_pos(self):
        maze_x, maze_y = self.maze_pos
        x, y = self.pos
        if not self.maze.maze[maze_y][maze_x] & self.direction or (
            x % 50 != 7 or y % 50 != 7
        ):
            next_x, next_y = self.vector[self.direction]
        else:
            next_x, next_y = 0, 0
        new_x, new_y = (x + next_x, y + next_y)
        if new_x % 50 == 7 and new_y % 50 == 7:
            self.maze_pos = (new_x // 50, new_y // 50)
        self.pos = (new_x, new_y)
