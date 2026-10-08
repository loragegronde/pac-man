from src.visual.maze import Maze


class Player:
    def __init__(self, maze: Maze, assets) -> None:
        self.maze = maze
        self.define_start_pos()
        self.direction = 2
        self.next_direction = 2
        self.mov = 1
        self.dt = 0
        self.spawn = assets.pac_man_spawn
        self.movement = assets.pac
        self.frame = 0
        self.opposite = {1: 4, 2: 8, 4: 1, 8: 2}
        self.vector: dict[int, tuple[int, int]] = {
            8: (-1, 0),
            4: (0, 1),
            2: (1, 0),
            1: (0, -1),
        }

    def define_start_pos(self):
        max_x = len(self.maze.maze[0])
        max_y = len(self.maze.maze)
        self.maze_pos = (max_x // 2, max_y // 2)
        self.pos = (self.maze_pos[0] * 50 + 7, self.maze_pos[1] * 50 + 7)

    def update_pos(self, dt: float = 0.0, update: bool = True):
        self.dt += dt
        self.define_movement()
        maze_x, maze_y = self.maze_pos
        x, y = self.pos
        if (
            not self.maze.maze[maze_y][maze_x] & self.direction
            or (x % 50 != 7 or y % 50 != 7)
        ) and update:
            next_x, next_y = self.vector[self.direction]
        else:
            next_x, next_y = 0, 0
        new_x, new_y = (x + next_x, y + next_y)
        self.pos = (new_x, new_y)
        if self.dt > 0.3:
            if self.frame >= 2:
                self.mov = -1
            if self.frame <= 0:
                self.mov = 1
            self.frame = self.frame + self.mov % 3
            self.dt -= 0.3

    def define_movement(self):
        x, y = self.pos
        if x % 50 == 7 and y % 50 == 7:
            self.maze_pos = (x // 50, y // 50)
        if (
            self.direction == self.next_direction
            or self.direction == self.opposite[self.next_direction]
        ):
            self.direction = self.next_direction
            return
        maze_x, maze_y = self.maze_pos
        if (
            not self.maze.maze[maze_y][maze_x] & self.next_direction
            and x % 50 == 7
            and y % 50 == 7
        ):
            self.direction = self.next_direction
