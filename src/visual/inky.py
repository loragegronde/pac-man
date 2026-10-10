import random
from typing import final, override

from src.visual.enemy import Enemy


@final
class Inky(Enemy):
    @override
    def define_pos(self) -> None:
        max_x = len(self.maze.maze[0]) - 1
        max_y = len(self.maze.maze) - 1
        self.maze_pos = (max_x, max_y)
        self.home = self.maze_pos
        self.pos = (max_x * 50 + 7, max_y * 50 + 7)
        self.direction = 4
        self.state = 0.0
        self.dead = False
        self.dead_wait = 0

    @override
    def update_direction(
        self, target: tuple[int, int], pac_dir: int
    ) -> None:
        _ = target, pac_dir
        x, y = self.pos
        if x % 50 != 7 or y % 50 != 7:
            return
        mx, my = self.maze_pos
        open_dirs = [d for d in (1, 2, 4, 8) if not self.maze.maze[my][mx] & d]
        if not open_dirs:
            return
        opp = {1: 4, 2: 8, 4: 1, 8: 2}[self.direction]
        fwd = [d for d in open_dirs if d != opp]
        self.direction = random.choice(fwd or open_dirs)
