from __future__ import annotations

import pygame

from src.assets import Assets
from src.menu import draw_double_round_rect, point_in


class PauseMenu:
    OPTIONS: tuple[str, ...] = ("RESUME", "CHEATS", "MAIN MENU")
    LABEL_W: dict[str, int] = {
        "RESUME": 147,
        "CHEATS": 141,
        "MAIN MENU": 201,
    }
    TITLE_W: int = 187
    BOX_W: int = 520
    BOX_H: int = 340
    DIM_COLOR: tuple[int, int, int] = (0, 0, 0)
    ROW_H: int = 70
    HIT_H: int = 48
    HIT_PAD_X: int = 20

    def __init__(
        self,
        screen: pygame.Surface,
        assets: Assets,
        screen_w: int,
        screen_h: int,
    ) -> None:
        self.screen: pygame.Surface = screen
        self.assets: Assets = assets
        self.screen_w: int = screen_w
        self.screen_h: int = screen_h
        self.selected: int = 0
        self.x: int = (screen_w - self.BOX_W) // 2
        self.y: int = (screen_h - self.BOX_H) // 2 - 40
        self._option_hits: list[tuple[int, int, int, int]] = []

    def reset(self) -> None:
        self.selected = 0

    def handle_keydown(self, event: pygame.event.Event) -> str | None:
        if event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.OPTIONS)
        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.OPTIONS)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            return self._action()
        elif event.key == pygame.K_ESCAPE:
            return "resume"
        return None

    def click_at(self, mx: int, my: int) -> str | None:
        for i, (x, y, w, h) in enumerate(self._option_hits):
            if point_in(mx, my, x, y, w, h):
                self.selected = i
                return self._action()
        return None

    def _action(self) -> str:
        choice = self.OPTIONS[self.selected]
        if choice == "RESUME":
            return "resume"
        if choice == "CHEATS":
            return "cheats"
        return "menu"

    def dim_screen(self) -> None:
        cell = 2
        for y in range(0, self.screen_h, cell):
            for x in range(0, self.screen_w, cell * 2):
                ox = x + (cell if (y // cell) % 2 else 0)
                _ = pygame.draw.rect(
                    self.screen,
                    self.DIM_COLOR,
                    (ox, y, cell, cell),
                )

    def render(self, dt: float = 0.0) -> None:
        _ = dt
        a = self.assets
        mx, my = pygame.mouse.get_pos()

        draw_double_round_rect(
            self.screen,
            self.x,
            self.y,
            self.BOX_W,
            self.BOX_H,
            outer=a.BORDER_OUTER,
            inner=a.BORDER_INNER,
            radius=a.BORDER_RADIUS,
        )

        title = a.font_large.render("PAUSE", True, (255, 220, 80))
        _ = self.screen.blit(
            title,
            (self.x + (self.BOX_W - self.TITLE_W) // 2, self.y + 36),
        )

        self._option_hits = []
        oy = self.y + 120
        layout: list[tuple[str, int, int]] = []
        for label in self.OPTIONS:
            text_w = self.LABEL_W[label]
            rx = self.x + (self.BOX_W - text_w) // 2
            self._option_hits.append(
                (
                    rx - self.HIT_PAD_X,
                    oy - 8,
                    text_w + 2 * self.HIT_PAD_X,
                    self.HIT_H,
                )
            )
            layout.append((label, rx, oy))
            oy += self.ROW_H

        for i, (x, y, w, h) in enumerate(self._option_hits):
            if point_in(mx, my, x, y, w, h):
                self.selected = i
                break

        for i, (label, rx, oy) in enumerate(layout):
            color = (255, 255, 120) if i == self.selected else (220, 220, 230)
            surf = a.font_medium.render(label, True, color)
            _ = self.screen.blit(surf, (rx, oy))
