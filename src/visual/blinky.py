from typing import final, override

from src.visual.dijkstra import dir_to, farthest_cell, next_cell
from src.visual.enemy import Enemy


@final
class Blinky(Enemy):
    @override
    def define_pos(self) -> None:
        self.maze_pos = (1, 0)
        self.home = self.maze_pos
        self.pos = (57, 7)
        self.direction = 2
        self.state = 0.0
        self.dead = False
        self.dead_wait = 0

    @override
    def update_direction(
        self, target: tuple[int, int], pac_dir: int
    ) -> None:
        _ = pac_dir
        x, y = self.pos
        if x % 50 != 7 or y % 50 != 7:
            return
        goal = farthest_cell(self.maze.maze, target) if self.state > 0 else target
        nxt = next_cell(self.maze.maze, self.maze_pos, goal)
        if nxt is not None:
            self.direction = dir_to(self.maze_pos, nxt)
