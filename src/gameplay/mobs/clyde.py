"""Clyde: aims a few cells ahead of Pac-Man."""

from typing import final
from typing_extensions import override

from src.gameplay.mobs.pathfinding import dir_to, farthest_cell, next_cell
from src.gameplay.mobs.enemy import Enemy


def _ahead(
    maze: list[list[int]], target: tuple[int, int], pac_dir: int
) -> tuple[int, int]:
    """Cell up to 3 steps in front of Pac-Man.

    Args:
        maze: Bitmask grid.
        target: Pac-Man cell.
        pac_dir: Pac-Man direction bitmask.

    Returns:
        Farthest walkable cell in that direction, or ``target``.
    """
    vec = {8: (-1, 0), 4: (0, 1), 2: (1, 0), 1: (0, -1)}
    dx, dy = vec[pac_dir]
    px, py = target
    w, h = len(maze[0]), len(maze)
    goal = target
    for i in range(1, 4):
        nx, ny = px + dx * i, py + dy * i
        if not (0 <= nx < w and 0 <= ny < h) or maze[ny][nx] == 15:
            break
        goal = (nx, ny)
    return goal


@final
class Clyde(Enemy):
    """Orange ghost that targets ahead of Pac-Man."""

    @override
    def define_pos(self) -> None:
        """Spawn near the top-right corner."""
        max_x = len(self.maze.maze[0]) - 1
        self.maze_pos = (max_x, 1)
        self.home = self.maze_pos
        self.pos = (max_x * 50 + 7, 57)
        self.direction = 2
        self.state = 0.0
        self.dead = False
        self.dead_wait = 0

    @override
    def update_direction(self, target: tuple[int, int], pac_dir: int) -> None:
        """Chase ahead of Pac-Man, or flee when scared.

        Args:
            target: Pac-Man maze cell.
            pac_dir: Pac-Man direction bitmask.
        """
        x, y = self.pos
        if x % 50 != 7 or y % 50 != 7:
            return
        goal = (
            farthest_cell(self.maze.maze, target)
            if self.state > 0
            else _ahead(self.maze.maze, target, pac_dir)
        )
        nxt = next_cell(self.maze.maze, self.maze_pos, goal)
        if nxt is not None:
            self.direction = dir_to(self.maze_pos, nxt)
