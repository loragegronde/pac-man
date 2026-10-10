from src.assets import Mob
from src.visual.blinky import Blinky
from src.visual.clyde import Clyde
from src.visual.enemy import Enemy
from src.visual.inky import Inky
from src.visual.maze import Maze
from src.visual.pinky import Pinky


class EnemyHandler:
    def __init__(self, assets: Mob, maze: Maze) -> None:
        afraid, dead = assets.afraid, assets.dead
        self.ghosts: list[Enemy] = [
            Blinky(assets.blinky, afraid, dead, maze),
            Clyde(assets.clyde, afraid, dead, maze),
            Inky(assets.inky, afraid, dead, maze),
            Pinky(assets.pinky, afraid, dead, maze),
        ]

    def refresh_frame(self, target: tuple[int, int], pac_dir: int) -> None:
        for ghost in self.ghosts:
            if ghost.dead:
                ghost.go_home()
                continue
            ghost.update_direction(target, pac_dir)
            for _ in range(1 if ghost.state > 0 else 2):
                ghost.update_pos()
