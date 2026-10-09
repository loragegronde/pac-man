from typing import final, override

from src.visual.dijkstra import dir_to, farthest_cell, next_cell
from src.visual.enemy import Enemy


def _behind(
    maze: list[list[int]], target: tuple[int, int], pac_dir: int
) -> tuple[int, int]:
    vec = {8: (-1, 0), 4: (0, 1), 2: (1, 0), 1: (0, -1)}
    dx, dy = vec[pac_dir]
    px, py = target
    w, h = len(maze[0]), len(maze)
    goal = target
    for i in range(1, 4):
        nx, ny = px - dx * i, py - dy * i
        if not (0 <= nx < w and 0 <= ny < h) or maze[ny][nx] == 15:
            break
        goal = (nx, ny)
    return goal


@final
class Pinky(Enemy):
    @override
    def define_pos(self) -> None:
        max_y = len(self.maze.maze) - 1
        self.maze_pos = (1, max_y)
        self.home = self.maze_pos
        self.pos = (57, max_y * 50 + 7)
        self.direction = 8
        self.state = 0.0
        self.dead = False
        self.dead_wait = 0

    @override
    def update_direction(
        self, target: tuple[int, int], pac_dir: int
    ) -> None:
        x, y = self.pos
        if x % 50 != 7 or y % 50 != 7:
            return
        goal = (
            farthest_cell(self.maze.maze, target)
            if self.state > 0
            else _behind(self.maze.maze, target, pac_dir)
        )
        nxt = next_cell(self.maze.maze, self.maze_pos, goal)
        if nxt is not None:
            self.direction = dir_to(self.maze_pos, nxt)
