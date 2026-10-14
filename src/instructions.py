"""In-game instructions panel (controls and rules)."""

from __future__ import annotations

import pygame

from src.assets import Assets
from src.menu import draw_double_round_rect, point_in


class Instructions:
    """Show controls and rules, then return to the menu."""

    BOX_W: int = 720
    BOX_H: int = 550
    TITLE_W: int = 438
    BACK_W: int = 100
    BACK_H: int = 48
    FOOTER_H: int = 80
    LINE_H: int = 34
    SECTION_GAP: int = 14

    COLOR_TITLE: tuple[int, int, int] = (255, 220, 80)
    COLOR_SECTION: tuple[int, int, int] = (255, 200, 60)
    COLOR_BODY: tuple[int, int, int] = (220, 220, 230)
    COLOR_BACK: tuple[int, int, int] = (220, 220, 230)
    COLOR_BACK_SEL: tuple[int, int, int] = (255, 255, 120)

    SECTIONS: tuple[tuple[str, tuple[str, ...]], ...] = (
        (
            "CONTROLS",
            (
                "Arrow keys     Move Pac-Man",
                "ESC            Pause / Back",
                "ENTER / SPACE  Confirm",
            ),
        ),
        (
            "RULES",
            (
                "Eat all pac-gums to clear a level",
                "Super pac-gums scare the ghosts",
                "Eat scared ghosts for bonus points",
                "Avoid ghosts or lose a life",
                "Clear all 10 levels to win",
                "Timer ends or 0 lives = game over",
            ),
        ),
    )

    def __init__(
        self,
        screen: pygame.Surface,
        assets: Assets,
        screen_w: int,
        screen_h: int,
    ) -> None:
        """Center the instructions panel on screen.

        Args:
            screen: Display surface.
            assets: Fonts and border colors.
            screen_w: Window width.
            screen_h: Window height.
        """
        self.screen: pygame.Surface = screen
        self.assets: Assets = assets
        self.x: int = (screen_w - self.BOX_W) // 2
        self.y: int = (screen_h - self.BOX_H) // 2 - 10
        self.back_x: int = self.x + (self.BOX_W - self.BACK_W) // 2
        self.back_y: int = self.y + self.BOX_H - self.FOOTER_H + 16
        self.back_hovered: bool = False

    def handle_keydown(self, event: pygame.event.Event) -> str | None:
        """Close the panel on Esc, Enter, or Space.

        Args:
            event: A KEYDOWN event.

        Returns:
            ``"back"`` when the panel should close.
        """
        if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
            return "back"
        return None

    def _back_hit(self) -> tuple[int, int, int, int]:
        """Hitbox for the BACK label."""
        return (
            self.back_x - 20,
            self.back_y - 8,
            self.BACK_W + 40,
            self.BACK_H,
        )

    def click_at(self, mx: int, my: int) -> str | None:
        """Handle a click on BACK.

        Args:
            mx: Mouse x.
            my: Mouse y.

        Returns:
            ``"back"`` if BACK was clicked.
        """
        if point_in(mx, my, *self._back_hit()):
            return "back"
        return None

    def render(self, dt: float = 0.0) -> None:
        """Draw the panel content and BACK button.

        Args:
            dt: Unused frame delta (kept for a uniform API).
        """
        _ = dt
        a = self.assets
        mx, my = pygame.mouse.get_pos()
        self.back_hovered = point_in(mx, my, *self._back_hit())

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

        title = a.font_large.render("INSTRUCTIONS", True, self.COLOR_TITLE)
        _ = self.screen.blit(
            title,
            (self.x + (self.BOX_W - self.TITLE_W) // 2, self.y + 28),
        )

        content_bottom = self.y + self.BOX_H - self.FOOTER_H
        oy = self.y + 100
        for section, lines in self.SECTIONS:
            if oy + self.LINE_H > content_bottom:
                break
            header = a.font_medium.render(section, True, self.COLOR_SECTION)
            _ = self.screen.blit(header, (self.x + 56, oy))
            oy += self.LINE_H + 4
            for line in lines:
                if oy + self.LINE_H > content_bottom:
                    break
                body = a.font.render(line, True, self.COLOR_BODY)
                _ = self.screen.blit(body, (self.x + 72, oy))
                oy += self.LINE_H
            oy += self.SECTION_GAP

        back_color = (
            self.COLOR_BACK_SEL if self.back_hovered else self.COLOR_BACK
        )
        back = a.font_medium.render("BACK", True, back_color)
        _ = self.screen.blit(back, (self.back_x, self.back_y))
