"""Owns the four ghosts and updates them each frame."""

from src.utils.assets import Mob
from src.gameplay.mobs.blinky import Blinky
from src.gameplay.mobs.clyde import Clyde
from src.gameplay.mobs.enemy import Enemy
from src.gameplay.mobs.inky import Inky
from src.gameplay.maze import Maze
from src.gameplay.mobs.pinky import Pinky


class EnemyHandler:
    """Create and tick Blinky, Clyde, Inky, and Pinky."""

    def __init__(self, assets: Mob, maze: Maze, speed: float) -> None:
        """Spawn all ghosts on the given maze.

        Args:
            assets: Sprite sets for every character.
            maze: Level maze.
            speed: Base ghost speed for this level.
        """
        afraid, dead = assets.afraid, assets.dead
        self.ghosts: list[Enemy] = [
            Blinky(assets.blinky, afraid, dead, maze, speed),
            Clyde(assets.clyde, afraid, dead, maze, speed),
            Inky(assets.inky, afraid, dead, maze, speed),
            Pinky(assets.pinky, afraid, dead, maze, speed),
        ]

    def refresh_frame(
        self, target: tuple[int, int], pac_dir: int, speed: float = 1.0
    ) -> None:
        """Update AI and movement for every ghost.

        Dead ghosts go home; others chase (faster) or flee (slower).

        Args:
            target: Pac-Man maze cell.
            pac_dir: Pac-Man direction bitmask.
            speed: Frame speed scale.
        """
        for ghost in self.ghosts:
            if ghost.dead:
                ghost.go_home()
                continue
            ghost.update_direction(target, pac_dir)
            for _ in range(1 if ghost.state > 0 else 2):
                ghost.update_pos(speed)
