
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pygame

ASSETS_DIR = Path("assets")


def crop(
    sheet: pygame.Surface, x: int, y: int, w: int, h: int
) -> pygame.Surface:
    image = pygame.Surface((w, h), pygame.SRCALPHA)
    _ = image.blit(sheet, (0, 0), (x, y, w, h))
    return image


def scale_nearest(src: pygame.Surface, w: int, h: int) -> pygame.Surface:
    out = pygame.Surface((w, h), pygame.SRCALPHA)
    sw, sh = src.get_size()
    if sw <= 0 or sh <= 0 or w <= 0 or h <= 0:
        return out
    src_rgba = src.convert_alpha()
    for y in range(h):
        sy = y * sh // h
        for x in range(w):
            sx = x * sw // w
            r, g, b, a = src_rgba.get_at((sx, sy))
            if r < 12 and g < 12 and b < 12:
                out.set_at((x, y), (0, 0, 0, 0))
            else:
                out.set_at((x, y), (r, g, b, a))
    return out


@dataclass
class MenuLayout:
    title_x: int
    title_y: int
    play_x: int
    play_y: int
    hint_x: int
    hint_y: int
    panel_x: int
    panel_y: int
    panel_w: int
    panel_h: int
    up_arrow: pygame.Rect
    down_arrow: pygame.Rect


class Assets:

    TITLE_W: int = 1500
    TITLE_H: int = 340

    PLAY_W: int = 440
    PLAY_H: int = 123
    
    PANEL_W: int = 680
    VISIBLE_ROWS: int = 10
    ROW_H: int = 42
    BANNER_INSET: int = 64
    BORDER_RADIUS: int = 22
    BORDER_OUTER: tuple[int, int, int] = (255, 220, 60)
    BORDER_INNER: tuple[int, int, int] = (255, 170, 50)

    RANK_OX: int = 36
    NAME_OX: int = 100
    SCORE_RIGHT_PAD: int = 48
    LIST_TOP_GAP: int = 18
    BANNER_TOP: int = 22
    ARROW_W: int = 44
    ARROW_H: int = 32
    ARROW_GAP: int = 16
    ARROW_BOTTOM: int = 48

    def __init__(self, root: Path = ASSETS_DIR) -> None:
        self.root: Path = root

        self.title: pygame.Surface = self._load("title.png")
        self.play: pygame.Surface = self._load("play.png")
        self.play_hovered: pygame.Surface = self._load("play_hovered.png")
        self.highscores_banner_raw: pygame.Surface = self._load(
            "highscores.png"
        )
        self.sprites: pygame.Surface = self._load("sprites.png")

        banner_w = self.PANEL_W - self.BANNER_INSET
        banner_h = max(
            48,
            self.highscores_banner_raw.get_height()
            * banner_w
            // self.highscores_banner_raw.get_width(),
        )
        self.hs_banner: pygame.Surface = scale_nearest(
            self.highscores_banner_raw, banner_w, banner_h
        )
        self.hs_banner_w: int = banner_w
        self.hs_banner_h: int = banner_h

        self.up_arrow: pygame.Surface = scale_nearest(
            self.crop_sprite(210, 663, 22, 16), self.ARROW_W, self.ARROW_H
        )
        self.down_arrow: pygame.Surface = scale_nearest(
            self.crop_sprite(210, 756, 22, 16), self.ARROW_W, self.ARROW_H
        )

        self.font_hint: pygame.font.Font = pygame.font.Font(None, 50)
        self.font: pygame.font.Font = pygame.font.Font(None, 40)
        self.font_small: pygame.font.Font = pygame.font.Font(None, 30)
        self.font_large: pygame.font.Font = pygame.font.Font(None, 48)

        self.hint: pygame.Surface = self.font_hint.render(
            "ENTER / CLICK PLAY", True, (200, 200, 210)
        )
        self.hint_w: int = self.hint.get_width()
        self.hint_h: int = self.hint.get_height()

        self.no_score: pygame.Surface = self.font.render(
            "no-score", True, (180, 180, 190)
        )

    def _load(self, name: str) -> pygame.Surface:
        return pygame.image.load(str(self.root / name)).convert_alpha()

    def crop_sprite(self, x: int, y: int, w: int, h: int) -> pygame.Surface:
        return crop(self.sprites, x, y, w, h)

    def menu_layout(self, screen_w: int, screen_h: int) -> MenuLayout:
        title_x = screen_w // 2 - self.TITLE_W // 2
        title_y = screen_h // 6 - self.TITLE_H // 2
        play_x = screen_w // 2 - self.PLAY_W
        play_y = (screen_h // 2) + 100

        hint_x = screen_w // 2 - self.hint_w - 24
        hint_y = screen_h // 3 + 180

        panel_w = self.PANEL_W
        panel_h = (
            36 + self.hs_banner_h + 24 + self.VISIBLE_ROWS * self.ROW_H + 64
        )
        panel_x = screen_w - panel_w - 24
        panel_y = play_y + self.PLAY_H // 2 - panel_h // 2

        pair_w = self.ARROW_W * 2 + self.ARROW_GAP
        ay = panel_y + panel_h - self.ARROW_BOTTOM
        ax = panel_x + (panel_w - pair_w) // 2
        up_arrow = pygame.Rect(ax, ay, self.ARROW_W, self.ARROW_H)
        down_arrow = pygame.Rect(
            ax + self.ARROW_W + self.ARROW_GAP, ay, self.ARROW_W, self.ARROW_H
        )

        return MenuLayout(
            title_x=title_x,
            title_y=title_y,
            play_x=play_x,
            play_y=play_y,
            hint_x=hint_x,
            hint_y=hint_y,
            panel_x=panel_x,
            panel_y=panel_y,
            panel_w=panel_w,
            panel_h=panel_h,
            up_arrow=up_arrow,
            down_arrow=down_arrow,
        )
