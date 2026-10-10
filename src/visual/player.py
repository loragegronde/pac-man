import pygame

from src.assets import Mob
from src.visual.maze import Maze


class Player:
    def __init__(self, maze: Maze, assets: Mob) -> None:
        self.maze: Maze = maze
        self.define_start_pos()
        self.direction: int = 2
        self.next_direction: int = 2
        self.mov: int = 1
        self.dt: float = 0.0
        self.spawn: list[pygame.Surface] = assets.pac_man_spawn
        self.movement: dict[int, list[pygame.Surface]] = assets.pac
        self.opposite: dict[int, int] = {1: 4, 2: 8, 4: 1, 8: 2}
        self.vector: dict[int, tuple[int, int]] = {
            8: (-1, 0),
            4: (0, 1),
            2: (1, 0),
            1: (0, -1),
        }

    def define_start_pos(self) -> None:
        max_x = len(self.maze.maze[0])
        max_y = len(self.maze.maze)
        self.maze_pos: tuple[int, int] = ((max_x - 1) // 2, (max_y - 1) // 2)
        self.pos: tuple[float, float] = (
            self.maze_pos[0] * 50 + 7,
            self.maze_pos[1] * 50 + 7,
        )

    def update_pos(self, speed: float) -> None:
        self.define_movement()
        maze_x, maze_y = self.maze_pos
        x, y = self.pos
        if not self.maze.maze[maze_y][maze_x] & self.direction or (
            x % 50 != 7 or y % 50 != 7
        ):
            next_x, next_y = self.vector[self.direction]
        else:
            next_x, next_y = 0, 0
        next_cell = (
            maze_x * 50 + (next_x * 50) + 7,
            maze_y * 50 + (next_y * 50) + 7,
        )
        next_x *= speed
        next_y *= speed
        new_x, new_y = (x + next_x, y + next_y)
        self.pos = (
            max((new_x, new_y), next_cell)
            if self.direction in {1, 8}
            else min((new_x, new_y), next_cell)
        )

    def define_movement(self) -> None:
        x, y = self.pos
        if x % 50 == 7 and y % 50 == 7:
            self.maze_pos = (int(x // 50), int(y // 50))
        if (
            self.direction == self.next_direction
            or self.direction == self.opposite[self.next_direction]
        ):
            self.direction = self.next_direction
            return
        maze_x, maze_y = self.maze_pos
        if (
            (
                not self.maze.maze[maze_y][maze_x] & self.next_direction
                or self.maze.maze[maze_y][maze_x] & self.direction
            )
            and x % 50 == 7
            and y % 50 == 7
        ):
            self.direction = self.next_direction
