from src.assets import Assets
from src.name_box import NameBox
import pygame


class Victory:
    def __init__(
        self,
        assets: Assets,
        screen: pygame.Surface,
        name_box: NameBox,
        screen_w: int,
        screen_h: int,
    ) -> None:
        self.assets: Assets = assets
        self.screen: pygame.Surface = screen
        self.name_box: NameBox = name_box
        self.screen_w = screen_w
        self.screen_h = screen_h

    def render(self, dt: float = 0.0) -> None:
        a = self.assets
        x = (self.screen_w - a.victory_w) // 2
        y = (self.screen_h - a.victory_h) // 2 - 350
        _ = self.screen.blit(a.victory, (x, y))
        self.name_box.render(dt)
