from __future__ import annotations

import pygame

from src.assets import Assets
from src.menu import draw_double_round_rect


class NameBox:
    MAX_LEN: int = 10
    BOX_W: int = 550
    BOX_H: int = 90

    def __init__(
        self,
        screen: pygame.Surface,
        assets: Assets,
        screen_w: int,
        screen_h: int,
    ) -> None:
        self.screen: pygame.Surface = screen
        self.assets: Assets = assets
        self.text: str = ""
        self.blink_time: float = 0.0
        self.show_cursor: bool = True
        self.typing_idle: float = 0.0
        self.x: int = (screen_w - self.BOX_W) // 2
        self.y: int = screen_h // 2 + 40

    def reset(self) -> None:
        self.text = ""
        self.blink_time = 0.0
        self.show_cursor = True
        self.typing_idle = 0.0
        pygame.key.set_repeat(400, 40)

    def _on_type(self) -> None:
        self.show_cursor = True
        self.blink_time = 0.0
        self.typing_idle = 0.0

    def handle_keydown(self, event: pygame.event.Event) -> str | None:
        if event.key == pygame.K_RETURN:
            name = self.text.strip()
            if name:
                return "submit"
            return None
        if event.key == pygame.K_BACKSPACE:
            if self.text:
                self.text = self.text[:-1]
                self._on_type()
            return None
        ch = event.unicode
        if not ch:
            return None
        if ch.isalnum() or ch == " ":
            if len(self.text) < self.MAX_LEN:
                self.text += ch
                self._on_type()
        return None

    def render(self, dt: float = 0.0) -> None:
        a = self.assets
        self.typing_idle += dt
        if self.typing_idle < 0.5:
            self.show_cursor = True
            self.blink_time = 0.0
        else:
            self.blink_time += dt
            if self.blink_time >= 0.5:
                self.blink_time -= 0.5
                self.show_cursor = not self.show_cursor

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

        label_text = "ENTER NAME"
        label = a.font_medium.render(label_text, True, (200, 200, 210))
        label_w, _ = a.font_medium.size(label_text)
        _ = self.screen.blit(
            label,
            (self.x + (self.BOX_W - label_w) // 2, self.y - 50),
        )

        display = self.text
        if self.show_cursor and len(self.text) < self.MAX_LEN:
            display = self.text + "|"
        name_surf = a.font_large.render(display, True, (230, 230, 190))
        name_w, _ = a.font_large.size(display)
        _ = self.screen.blit(
            name_surf,
            (self.x + (self.BOX_W - name_w) // 2, self.y + 20),
        )
