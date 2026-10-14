from src.assets import Assets
from src.name_box import NameBox
import pygame


class GameOver:
    SCORE_COLOR: tuple[int, int, int] = (255, 220, 80)

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
        self.screen_w: int = screen_w
        self.screen_h: int = screen_h

    def render(self, score: int, dt: float = 0.0) -> None:
        a = self.assets
        x = (self.screen_w - a.game_over_w) // 2
        y = (self.screen_h - a.game_over_h) // 2 - 350
        _ = self.screen.blit(a.game_over, (x, y))

        label = a.font_medium.render("SCORE", True, (200, 200, 210))
        value = a.font_large.render(str(score), True, self.SCORE_COLOR)
        mid_y = self.screen_h // 2 + 150
        value_w = max(1, len(str(score))) * a.CHAR_W_LARGE
        _ = self.screen.blit(
            label, ((self.screen_w - a.SCORE_LABEL_W) // 2, mid_y)
        )
        _ = self.screen.blit(
            value,
            ((self.screen_w - value_w) // 2, mid_y + 45),
        )

        self.name_box.render(dt)
