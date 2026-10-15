"""Inky: wanders with random open directions."""

import random
from typing import final
from typing_extensions import override

from src.gameplay.mobs.enemy import Enemy


@final
class Inky(Enemy):
    """Cyan ghost that picks a random path at each junction."""

    @override
    def define_pos(self) -> None:
        """Spawn in the bottom-right corner."""
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
    def update_direction(self, target: tuple[int, int], pac_dir: int) -> None:
        """Choose a random open direction (prefer not turning back).

        Args:
            target: Unused (kept for the shared API).
            pac_dir: Unused (kept for the shared API).
        """
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
