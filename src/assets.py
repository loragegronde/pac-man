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


@dataclass
class Mob:
    blinky: dict[int, list[pygame.Surface]]
    pinky: dict[int, list[pygame.Surface]]
    clyde: dict[int, list[pygame.Surface]]
    inky: dict[int, list[pygame.Surface]]
    pac: dict[int, list[pygame.Surface]]
    pac_man_spawn: list[pygame.Surface]
    afraid: dict[str, list[pygame.Surface]]
    dead: dict[int, pygame.Surface]


class Assets:

    TITLE_W: int = 1500
    TITLE_H: int = 340

    PLAY_W: int = 440
    PLAY_H: int = 123

    HS_BANNER_SRC_W: int = 614
    HS_BANNER_SRC_H: int = 75
    VICTORY_W: int = 1022
    VICTORY_H: int = 160
    GAME_OVER_W: int = 1136
    GAME_OVER_H: int = 175

    PANEL_W: int = 900
    VISIBLE_ROWS: int = 10

    ROW_H: int = 42

    BANNER_INSET: int = 64
    BORDER_RADIUS: int = 24
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

    DIGIT_W: int = 16
    CHAR_W_MEDIUM: int = 26
    CHAR_W_LARGE: int = 37
    HINT_W: int = 352
    HINT_H: int = 34
    NO_SCORE_W: int = 116
    NO_SCORE_H: int = 27

    def __init__(self, root: Path = ASSETS_DIR) -> None:
        self.root: Path = root

        self.title: pygame.Surface = self._load("title.png")
        self.play: pygame.Surface = self._load("play.png")
        self.play_hovered: pygame.Surface = self._load("play_hovered.png")
        self.hs_banner: pygame.Surface = self._load("highscores.png")
        self.sprites: pygame.Surface = self._load("sprites.png")
        self.victory: pygame.Surface = self._load("victory.png")
        self.game_over: pygame.Surface = self._load("game_over.png")

        self.victory_w: int = self.VICTORY_W
        self.victory_h: int = self.VICTORY_H
        self.game_over_w: int = self.GAME_OVER_W
        self.game_over_h: int = self.GAME_OVER_H

        banner_w = self.PANEL_W - self.BANNER_INSET
        banner_h = max(
            48,
            self.HS_BANNER_SRC_H * banner_w // self.HS_BANNER_SRC_W,
        )
        self.hs_banner_w: int = banner_w
        self.hs_banner_h: int = banner_h

        self.up_arrow: pygame.Surface = self.crop_sprite(210, 663, 22, 16)
        self.down_arrow: pygame.Surface = self.crop_sprite(210, 756, 22, 16)

        self.font_hint: pygame.font.Font = pygame.font.Font(None, 50)
        self.font: pygame.font.Font = pygame.font.Font(None, 40)
        self.font_medium: pygame.font.Font = pygame.font.Font(None, 50)
        self.font_large: pygame.font.Font = pygame.font.Font(None, 80)

        hint_text = "ENTER / CLICK PLAY"
        self.hint: pygame.Surface = self.font_hint.render(
            hint_text, True, (200, 200, 210)
        )
        self.hint_w: int = self.HINT_W
        self.hint_h: int = self.HINT_H

        no_score_text = "no-score"
        self.no_score: pygame.Surface = self.font.render(
            no_score_text, True, (180, 180, 190)
        )
        self.no_score_w: int = self.NO_SCORE_W
        self.no_score_h: int = self.NO_SCORE_H
        self.get_pacgum()
        self.hud_labels: dict[str, pygame.Surface] = {
            "SCORE": self._load("hud_score.png"),
            "LIVES": self._load("hud_lives.png"),
            "LEVEL": self._load("hud_level.png"),
            "TIME": self._load("hud_time.png"),
        }

    def _load(self, name: str) -> pygame.Surface:
        return pygame.image.load(str(self.root / name)).convert_alpha()

    def crop_sprite(self, x: int, y: int, w: int, h: int) -> pygame.Surface:
        return crop(self.sprites, x, y, w, h)

    def get_mobs(self) -> Mob:
        img = self.sprites

        blinky_r1: pygame.Surface = crop(img, 651, 4, 35, 35)
        blinky_r2: pygame.Surface = crop(img, 651, 54, 35, 35)
        blinky_d1: pygame.Surface = crop(img, 651, 104, 35, 35)
        blinky_d2: pygame.Surface = crop(img, 651, 154, 35, 35)
        blinky_l1: pygame.Surface = crop(img, 651, 204, 35, 35)
        blinky_l2: pygame.Surface = crop(img, 651, 254, 35, 35)
        blinky_u1: pygame.Surface = crop(img, 651, 304, 35, 35)
        blinky_u2: pygame.Surface = crop(img, 651, 354, 35, 35)

        blinky = {
            2: [blinky_r1, blinky_r2],
            4: [blinky_d1, blinky_d2],
            8: [blinky_l1, blinky_l2],
            1: [blinky_u1, blinky_u2],
        }

        pinky_r1: pygame.Surface = crop(img, 701, 4, 35, 35)
        pinky_r2: pygame.Surface = crop(img, 701, 54, 35, 35)
        pinky_d1: pygame.Surface = crop(img, 701, 104, 35, 35)
        pinky_d2: pygame.Surface = crop(img, 701, 154, 35, 35)
        pinky_l1: pygame.Surface = crop(img, 701, 204, 35, 35)
        pinky_l2: pygame.Surface = crop(img, 701, 254, 35, 35)
        pinky_u1: pygame.Surface = crop(img, 701, 304, 35, 35)
        pinky_u2: pygame.Surface = crop(img, 701, 354, 35, 35)

        pinky = {
            2: [pinky_r1, pinky_r2],
            4: [pinky_d1, pinky_d2],
            8: [pinky_l1, pinky_l2],
            1: [pinky_u1, pinky_u2],
        }

        inky_r1: pygame.Surface = crop(img, 751, 4, 35, 35)
        inky_r2: pygame.Surface = crop(img, 751, 54, 35, 35)
        inky_d1: pygame.Surface = crop(img, 751, 104, 35, 35)
        inky_d2: pygame.Surface = crop(img, 751, 154, 35, 35)
        inky_l1: pygame.Surface = crop(img, 751, 204, 35, 35)
        inky_l2: pygame.Surface = crop(img, 751, 254, 35, 35)
        inky_u1: pygame.Surface = crop(img, 751, 304, 35, 35)
        inky_u2: pygame.Surface = crop(img, 751, 354, 35, 35)

        inky = {
            2: [inky_r1, inky_r2],
            4: [inky_d1, inky_d2],
            8: [inky_l1, inky_l2],
            1: [inky_u1, inky_u2],
        }

        clyde_r1: pygame.Surface = crop(img, 801, 4, 35, 35)
        clyde_r2: pygame.Surface = crop(img, 801, 54, 35, 35)
        clyde_d1: pygame.Surface = crop(img, 801, 104, 35, 35)
        clyde_d2: pygame.Surface = crop(img, 801, 154, 35, 35)
        clyde_l1: pygame.Surface = crop(img, 801, 204, 35, 35)
        clyde_l2: pygame.Surface = crop(img, 801, 254, 35, 35)
        clyde_u1: pygame.Surface = crop(img, 801, 304, 35, 35)
        clyde_u2: pygame.Surface = crop(img, 801, 354, 35, 35)

        clyde = {
            2: [clyde_r1, clyde_r2],
            4: [clyde_d1, clyde_d2],
            8: [clyde_l1, clyde_l2],
            1: [clyde_u1, clyde_u2],
        }

        pac_man_r1: pygame.Surface = crop(img, 851, 4, 35, 35)
        pac_man_r2: pygame.Surface = crop(img, 851, 54, 35, 35)
        pac_man_r3: pygame.Surface = crop(img, 851, 104, 35, 35)
        pac_man_d1: pygame.Surface = crop(img, 851, 154, 35, 35)
        pac_man_d2: pygame.Surface = crop(img, 851, 204, 35, 35)
        pac_man_d3: pygame.Surface = crop(img, 851, 254, 35, 35)
        pac_man_l1: pygame.Surface = crop(img, 851, 304, 35, 35)
        pac_man_l2: pygame.Surface = crop(img, 851, 354, 35, 35)
        pac_man_l3: pygame.Surface = crop(img, 851, 404, 35, 35)
        pac_man_u1: pygame.Surface = crop(img, 851, 454, 35, 35)
        pac_man_u2: pygame.Surface = crop(img, 851, 504, 35, 35)
        pac_man_u3: pygame.Surface = crop(img, 851, 554, 35, 35)

        pac = {
            2: [pac_man_r1, pac_man_r2, pac_man_r3],
            4: [pac_man_d1, pac_man_d2, pac_man_d3],
            8: [pac_man_l1, pac_man_l2, pac_man_l3],
            1: [pac_man_u1, pac_man_u2, pac_man_u3],
        }

        afraid_1: pygame.Surface = crop(img, 1, 553, 35, 35)
        afraid_2: pygame.Surface = crop(img, 1, 603, 35, 35)
        flash_1: pygame.Surface = crop(img, 51, 553, 35, 35)
        flash_2: pygame.Surface = crop(img, 51, 603, 35, 35)

        afraid = {"normal": [afraid_1, afraid_2], "flash": [flash_1, flash_2]}

        pac_man_spawn: list[pygame.Surface] = [
            crop(img, 351, 4 + (i * 50), 35, 35) for i in range(11)
        ]

        dead_r = crop(img, 301, 254, 35, 35)
        dead_d = crop(img, 301, 304, 35, 35)
        dead_l = crop(img, 301, 354, 35, 35)
        dead_u = crop(img, 301, 404, 35, 35)
        for eye in (dead_r, dead_d, dead_l, dead_u):
            _ = eye.set_colorkey((0, 0, 0))
        dead: dict[int, pygame.Surface] = {
            2: dead_r,
            4: dead_d,
            8: dead_l,
            1: dead_u,
        }
        return Mob(
            blinky=blinky,
            pinky=pinky,
            clyde=clyde,
            inky=inky,
            pac=pac,
            pac_man_spawn=pac_man_spawn,
            afraid=afraid,
            dead=dead
        )

    def menu_layout(self, screen_w: int, screen_h: int) -> MenuLayout:
        title_x = screen_w // 2 - self.TITLE_W // 2
        title_y = screen_h // 6 - self.TITLE_H // 2
        play_x = screen_w // 2 - self.PLAY_W - 100
        play_y = (screen_h // 2) + 100

        hint_x = screen_w // 2 - self.hint_w - 150
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

    def get_pacgum(self):
        img = self.sprites

        self.pac_gum: pygame.Surface = crop(img, 409, 227, 7, 7)
        self.super_pacgum: pygame.Surface = crop(img, 409, 311, 19, 19)
