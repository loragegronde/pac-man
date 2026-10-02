from src.visual.blinky import Blinky
from src.assets import Mob
from src.visual.enemy import Enemy


class EnemyHandler():
    def __init__(self, img_pos, window, assets: Mob, maze) -> None:
        self.img_pos = img_pos
        self.window = window
        self.create_ghosts(assets, maze)
        self.dt: float = 0
        self.frame = 0

    def create_ghosts(self, assets: Mob, maze):
        self.ghosts: list[Enemy] = [
            Blinky(assets.blinky, assets.afraid, maze)
        ]

    def draw_ghosts(self) -> None:
        for ghost in self.ghosts:
            img_x, img_y = self.img_pos
            x, y = ghost.pos
            _ = self.window.blit(
                ghost.assets[ghost.direction][self.frame],
                (x + img_x, y + img_y),
            )

    def refresh_frame(self, dt: float = 0.0):
        self.dt += dt
        if self.dt > 0.2:
            self.frame = (self.frame + 1) % 2
            self.dt -= 0.2
        self.draw_ghosts()
