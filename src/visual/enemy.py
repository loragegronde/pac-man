"""Base class shared by all ghosts."""

from abc import ABC, abstractmethod
from typing import TypeAlias

import pygame

from src.visual.pathfinding import dir_to, next_cell
from src.visual.maze import Maze

GhostSprites: TypeAlias = dict[int, list[pygame.Surface]]
AfraidSprites: TypeAlias = dict[str, list[pygame.Surface]]
DeadSprites: TypeAlias = dict[int, pygame.Surface]


class Enemy(ABC):
    """Abstract ghost: move, flee, and return home when eaten."""

    maze_pos: tuple[int, int]
    home: tuple[int, int]
    pos: tuple[int | float, int | float]

    def __init__(
        self,
        assets: GhostSprites,
        afraid: AfraidSprites,
        dead: DeadSprites,
        maze: Maze,
        speed: float,
    ) -> None:
        """Store sprites, maze, and speed, then spawn the ghost.

        Args:
            assets: Directional walk frames.
            afraid: Scared / flashing frames.
            dead: Eyes-only frames.
            maze: Current level maze.
            speed: Movement speed multiplier.
        """
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
        self.speed: float = speed

    def update_pos(self, speed: float = 1.0) -> None:
        """Move one step in the current direction.

        Args:
            speed: Extra frame speed scale.
        """
        mx, my = self.maze_pos
        x, y = self.pos
        if not self.maze.maze[my][mx] & self.direction or (
            x % 50 != 7 or y % 50 != 7
        ):
            dx, dy = self.vector[self.direction]
        else:
            dx, dy = 0, 0
        next_cell = (
            mx * 50 + (dx * 50) + 7,
            my * 50 + (dy * 50) + 7,
        )
        nx = x + dx * speed * self.speed
        ny = y + dy * speed * self.speed
        self.pos = (
            max((nx, ny), next_cell)
            if self.direction in {1, 8}
            else min((nx, ny), next_cell)
        )
        x, y = self.pos
        if x % 50 == 7 and y % 50 == 7:
            self.maze_pos = (int(nx) // 50, int(ny) // 50)

    def go_home(self) -> None:
        """Walk cell by cell back to the spawn point, then revive."""
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
    def define_pos(self) -> None:
        """Reset spawn cell, pixel position, and alive state."""
        ...

    @abstractmethod
    def update_direction(
        self, target: tuple[int, int], pac_dir: int
    ) -> None:
        """Pick the next direction from Pac-Man's cell and facing.

        Args:
            target: Pac-Man maze cell.
            pac_dir: Pac-Man direction bitmask.
        """
        ...
