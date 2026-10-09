from src.visual.blinky import Blinky
from src.visual.clyde import Clyde
from src.visual.inky import Inky
from src.visual.pinky import Pinky
from src.assets import Mob
from src.visual.enemy import Enemy


class EnemyHandler:
    def __init__(self, assets: Mob, maze) -> None:
        self.create_ghosts(assets, maze)
        self.dt: float = 0
        self.frame = 0

    def create_ghosts(self, assets: Mob, maze):
        self.ghosts: list[Enemy] = [
            Blinky(assets.blinky, assets.afraid, maze),
            Clyde(assets.clyde, assets.afraid, maze),
            Inky(assets.inky, assets.afraid, maze),
            Pinky(assets.pinky, assets.afraid, maze),
        ]

    def refresh_frame(self):
        for i, ghost in enumerate(self.ghosts):
            for _ in range(2):
                ghost.update_pos()
