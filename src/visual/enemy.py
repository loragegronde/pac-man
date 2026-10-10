from abc import ABC, abstractmethod

import pygame

from src.visual.dijkstra import dir_to, next_cell
from src.visual.maze import Maze

type GhostSprites = dict[int, list[pygame.Surface]]
type AfraidSprites = dict[str, list[pygame.Surface]]
type DeadSprites = dict[int, pygame.Surface]


class Enemy(ABC):
    maze_pos: tuple[int, int]
    home: tuple[int, int]
    pos: tuple[int, int]

    def __init__(
        self,
        assets: GhostSprites,
        afraid: AfraidSprites,
        dead: DeadSprites,
        maze: Maze,
    ) -> None:
        self.direction: int = 1
        self.state: float = 0.0
        self.dead: bool = False
        self.dead_wait: int = 0
        self.assets: GhostSprites = assets
        self.afraid: AfraidSprites = afraid
        self.dead_assets: DeadSprites = dead
        self.maze: Maze = maze
        self.vector: dict[int, tuple[int, int]] = {
            8: (-1, 0),
            4: (0, 1),
            2: (1, 0),
            1: (0, -1),
        }
        self.define_pos()

    def update_pos(self) -> None:
        mx, my = self.maze_pos
        x, y = self.pos
        if not self.maze.maze[my][mx] & self.direction or (
            x % 50 != 7 or y % 50 != 7
        ):
            dx, dy = self.vector[self.direction]
        else:
            dx, dy = 0, 0
        nx, ny = x + dx, y + dy
        if nx % 50 == 7 and ny % 50 == 7:
            self.maze_pos = (nx // 50, ny // 50)
        self.pos = (nx, ny)

    def go_home(self) -> None:
        if self.maze_pos == self.home:
            self.define_pos()
            return
        nxt = next_cell(self.maze.maze, self.maze_pos, self.home)
        if nxt is None:
            self.define_pos()
            return
        self.direction = dir_to(self.maze_pos, nxt)
        self.dead_wait += 1
        t = self.dead_wait / 12
        x0, y0 = self.maze_pos[0] * 50 + 7, self.maze_pos[1] * 50 + 7
        x1, y1 = nxt[0] * 50 + 7, nxt[1] * 50 + 7
        self.pos = (int(x0 + (x1 - x0) * t), int(y0 + (y1 - y0) * t))
        if self.dead_wait < 12:
            return
        self.dead_wait = 0
        self.maze_pos = nxt
        self.pos = (x1, y1)
        if self.maze_pos == self.home:
            self.define_pos()

    @abstractmethod
    def define_pos(self) -> None: ...

    @abstractmethod
    def update_direction(
        self, target: tuple[int, int], pac_dir: int
    ) -> None: ...
