from __future__ import annotations

import pygame

from src.assets import Assets
from src.menu import draw_double_round_rect


class PauseMenu:
    OPTIONS: tuple[str, ...] = ("RESUME", "MAIN MENU")
    BOX_W: int = 520
    BOX_H: int = 280
    DIM_COLOR: tuple[int, int, int] = (0, 0, 0)

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
        self._option_rects: list[pygame.Rect] = []

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
        for i, rect in enumerate(self._option_rects):
            if rect.collidepoint(mx, my):
                self.selected = i
                return self._action()
        return None

    def _action(self) -> str:
        if self.OPTIONS[self.selected] == "RESUME":
            return "resume"
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
        title_w, _ = a.font_large.size("PAUSE")
        _ = self.screen.blit(
            title,
            (self.x + (self.BOX_W - title_w) // 2, self.y + 36),
        )

        # Build hitboxes first, then hover updates selection
        self._option_rects = []
        oy = self.y + 120
        layout: list[tuple[str, int, int, int]] = []
        for label in self.OPTIONS:
            text_w, _ = a.font_medium.size(label)
            rx = self.x + (self.BOX_W - text_w) // 2
            self._option_rects.append(
                pygame.Rect(rx - 20, oy - 8, text_w + 40, 48)
            )
            layout.append((label, rx, oy, text_w))
            oy += 60

        for i, rect in enumerate(self._option_rects):
            if rect.collidepoint(mx, my):
                self.selected = i
                break

        for i, (label, rx, oy, _text_w) in enumerate(layout):
            color = (255, 255, 120) if i == self.selected else (220, 220, 230)
            surf = a.font_medium.render(label, True, color)
            _ = self.screen.blit(surf, (rx, oy))
