from src.assets import Assets
from src.name_box import NameBox
import pygame


class GameOver:
    def __init__(
        self, assets: Assets, screen: pygame.Surface, name_box: NameBox
    ) -> None:
        self.assets: Assets = assets
        self.screen: pygame.Surface = screen
        self.name_box: NameBox = name_box

    def render(self, dt: float = 0.0) -> None:
        img = self.assets.game_over
        x = (self.screen.get_width() - img.get_width()) // 2
        y = (self.screen.get_height() - img.get_height()) // 2 - 350
        _ = self.screen.blit(img, (x, y))
        self.name_box.render(dt)
