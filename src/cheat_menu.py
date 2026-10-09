from __future__ import annotations

import pygame

from src.assets import Assets
from src.cheats import Cheats
from src.menu import draw_double_round_rect, point_in
from src.visual.level_handler import LevelHandler


class CheatMenu:
    OPTIONS: tuple[tuple[str, str, str], ...] = (
        ("INVINCIBILITY", "check", "invincibility"),
        ("ONE PACGUM", "check", "one_pacgum"),
        ("ALWAYS CHASE", "check", "always_chase"),
        ("GHOST FREEZE", "check", "ghost_freeze"),
        ("LEVEL", "level", ""),
        ("LIVES", "lives", ""),
        ("SPEED", "speed", "speed_mult"),
        ("BACK", "back", ""),
    )

    BOX_W: int = 760
    BOX_H: int = 580
    ROW_H: int = 52
    TITLE_W: int = 227
    BACK_W: int = 100
    CHECK_SIZE: int = 28
    SPEED_MIN: float = 0.5
    SPEED_MAX: float = 3.0
    LEVEL_MIN: int = 1
    LEVEL_MAX: int = 10
    INT_LABEL_W: int = 208
    ARROW_W: int = 40
    CHAR_W: int = 26

    COLOR_LABEL: tuple[int, int, int] = (220, 220, 230)
    COLOR_SEL: tuple[int, int, int] = (255, 255, 120)
    COLOR_GREY: tuple[int, int, int] = (90, 90, 100)
    COLOR_BOX: tuple[int, int, int] = (255, 220, 80)
    COLOR_FILL: tuple[int, int, int] = (120, 255, 140)
    COLOR_TRACK: tuple[int, int, int] = (60, 60, 70)
    COLOR_KNOB: tuple[int, int, int] = (255, 220, 80)

    def __init__(
        self,
        screen: pygame.Surface,
        assets: Assets,
        screen_w: int,
        screen_h: int,
        cheats: Cheats,
        game: LevelHandler,
    ) -> None:
        self.screen: pygame.Surface = screen
        self.assets: Assets = assets
        self.cheats: Cheats = cheats
        self.game: LevelHandler = game
        self.selected: int = 0
        self.x: int = (screen_w - self.BOX_W) // 2
        self.y: int = (screen_h - self.BOX_H) // 2 - 20
        self._dragging_speed: bool = False
        self._row_hits: list[tuple[int, int, int, int]] = []
        self._slider_hit: tuple[int, int, int, int] = (0, 0, 0, 0)
        self._arrow_hits: dict[
            str, tuple[tuple[int, int, int, int], tuple[int, int, int, int]]
        ] = {}
        self._speed_i: int = self._index_of("speed")
        self._mouse_nav: bool = True
        self._last_mouse: tuple[int, int] = (-1, -1)

    def reset(self) -> None:
        self.selected = 0
        self._dragging_speed = False
        self._mouse_nav = True
        self._last_mouse = (-1, -1)

    def handle_keydown(self, event: pygame.event.Event) -> str | None:
        if event.key == pygame.K_UP:
            self._mouse_nav = False
            self.selected = (self.selected - 1) % len(self.OPTIONS)
        elif event.key == pygame.K_DOWN:
            self._mouse_nav = False
            self.selected = (self.selected + 1) % len(self.OPTIONS)
        elif event.key == pygame.K_LEFT:
            self._mouse_nav = False
            self._nudge(-1)
        elif event.key == pygame.K_RIGHT:
            self._mouse_nav = False
            self._nudge(1)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            return self._activate()
        elif event.key == pygame.K_ESCAPE:
            return "back"
        return None

    def click_at(self, mx: int, my: int) -> str | None:
        self._mouse_nav = True
        self._last_mouse = (mx, my)
        for kind, (left, right) in self._arrow_hits.items():
            if point_in(mx, my, *left):
                self.selected = self._index_of(kind)
                self._change_int(kind, -1)
                return None
            if point_in(mx, my, *right):
                self.selected = self._index_of(kind)
                self._change_int(kind, 1)
                return None
        if point_in(mx, my, *self._slider_hit):
            self.selected = self._speed_i
            self._dragging_speed = True
            self._set_speed_from_x(mx)
            return None
        for i, hit in enumerate(self._row_hits):
            if point_in(mx, my, *hit):
                self.selected = i
                kind = self.OPTIONS[i][1]
                if kind in ("lives", "level", "speed"):
                    return None
                return self._activate()
        return None

    def mouse_up(self) -> None:
        self._dragging_speed = False

    def mouse_move(self, mx: int, my: int) -> None:
        if (mx, my) != self._last_mouse:
            self._last_mouse = (mx, my)
            self._mouse_nav = True
        if self._dragging_speed:
            self._set_speed_from_x(mx)

    def _nudge(self, direction: int) -> None:
        kind = self.OPTIONS[self.selected][1]
        if kind in ("lives", "level"):
            self._change_int(kind, direction)
        elif kind == "speed":
            self._change_speed(0.1 * direction)

    def _activate(self) -> str | None:
        _label, kind, field = self.OPTIONS[self.selected]
        if kind == "back":
            return "back"
        if kind in ("lives", "level", "speed"):
            return None
        if field and self.cheats.is_blocked(field):
            return None
        if kind == "check":
            setattr(self.cheats, field, not bool(getattr(self.cheats, field)))
        return None

    def _change_int(self, kind: str, delta: int) -> None:
        if kind == "lives":
            self.game.lives = max(0, self.game.lives + delta)
        elif kind == "level":
            self.game.level = min(
                self.LEVEL_MAX,
                max(self.LEVEL_MIN, self.game.level + delta),
            )

    def _change_speed(self, delta: float) -> None:
        value = self.cheats.speed_mult + delta
        value = min(self.SPEED_MAX, max(self.SPEED_MIN, value))
        self.cheats.speed_mult = round(value, 1)

    def _set_speed_from_x(self, mx: int) -> None:
        track_x, _y, track_w, _h = self._slider_hit
        if track_w <= 0:
            return
        t = max(0.0, min(1.0, (mx - track_x) / track_w))
        value = self.SPEED_MIN + t * (self.SPEED_MAX - self.SPEED_MIN)
        self.cheats.speed_mult = round(value, 1)

    def _index_of(self, kind: str) -> int:
        for i, (_label, k, _field) in enumerate(self.OPTIONS):
            if k == kind:
                return i
        return 0

    def _row_y(self, index: int) -> int:
        return self.y + 100 + index * self.ROW_H

    def _row_color(self, index: int, field: str) -> tuple[int, int, int]:
        if field and self.cheats.is_blocked(field):
            return self.COLOR_GREY
        if index == self.selected:
            return self.COLOR_SEL
        return self.COLOR_LABEL

    def _update_hover(self) -> None:
        mx, my = pygame.mouse.get_pos()
        moved = (mx, my) != self._last_mouse
        self._last_mouse = (mx, my)
        if moved:
            self._mouse_nav = True
        if not self._mouse_nav:
            return
        for i, hit in enumerate(self._row_hits):
            if point_in(mx, my, *hit):
                self.selected = i
                return

    def render(self, dt: float = 0.0) -> None:
        _ = dt
        self._row_hits = []
        self._arrow_hits = {}
        for i in range(len(self.OPTIONS)):
            self._row_hits.append(
                (
                    self.x + 36,
                    self._row_y(i) - 4,
                    self.BOX_W - 72,
                    self.ROW_H - 4,
                )
            )
        self._update_hover()

        draw_double_round_rect(
            self.screen,
            self.x,
            self.y,
            self.BOX_W,
            self.BOX_H,
            outer=self.assets.BORDER_OUTER,
            inner=self.assets.BORDER_INNER,
            radius=self.assets.BORDER_RADIUS,
        )
        title = self.assets.font_large.render("CHEATS", True, (255, 220, 80))
        _ = self.screen.blit(
            title,
            (self.x + (self.BOX_W - self.TITLE_W) // 2, self.y + 24),
        )

        for i, (label, kind, field) in enumerate(self.OPTIONS):
            y = self._row_y(i)
            color = self._row_color(i, field)
            blocked = bool(field) and self.cheats.is_blocked(field)
            if kind == "check":
                self._draw_check(label, field, y, color, blocked)
            elif kind == "lives":
                self._draw_int_row(kind, label, self.game.lives, y, color)
            elif kind == "level":
                self._draw_int_row(kind, label, self.game.level, y, color)
            elif kind == "speed":
                self._draw_speed(y, i == self.selected)
            else:
                self._draw_back(label, y, color)

    def _blit(
        self, text: str, x: int, y: int, color: tuple[int, int, int]
    ) -> None:
        surf = self.assets.font_medium.render(text, True, color)
        _ = self.screen.blit(surf, (x, y))

    def _draw_check(
        self,
        label: str,
        field: str,
        y: int,
        color: tuple[int, int, int],
        blocked: bool,
    ) -> None:
        box_color = self.COLOR_GREY if blocked else self.COLOR_BOX
        _ = pygame.draw.rect(
            self.screen,
            box_color,
            (self.x + 48, y + 6, self.CHECK_SIZE, self.CHECK_SIZE),
            width=2,
        )
        if bool(getattr(self.cheats, field)):
            fill = self.COLOR_GREY if blocked else self.COLOR_FILL
            _ = pygame.draw.rect(
                self.screen,
                fill,
                (
                    self.x + 54,
                    y + 12,
                    self.CHECK_SIZE - 12,
                    self.CHECK_SIZE - 12,
                ),
            )
        self._blit(label, self.x + 90, y + 4, color)

    def _draw_int_row(
        self,
        kind: str,
        label: str,
        value: int,
        y: int,
        color: tuple[int, int, int],
    ) -> None:
        text_y = y + 4
        hit_y = y - 4
        hit_h = self.ROW_H - 4
        base_x = self.x + 48

        self._blit(f"{label}   ", base_x, text_y, color)

        left_x = base_x + self.INT_LABEL_W
        self._blit("<", left_x, text_y, color)
        left_hit = (left_x, hit_y, self.ARROW_W, hit_h)

        val = f" {value} "
        val_w = len(val) * self.CHAR_W
        self._blit(val, left_x + self.ARROW_W, text_y, color)

        right_x = left_x + self.ARROW_W + val_w
        self._blit(">", right_x, text_y, color)
        right_hit = (right_x, hit_y, self.ARROW_W, hit_h)

        self._arrow_hits[kind] = (left_hit, right_hit)

    def _draw_speed(self, y: int, selected: bool) -> None:
        color = self.COLOR_SEL if selected else self.COLOR_LABEL
        self._blit(
            f"SPEED  x{self.cheats.speed_mult:.1f}", self.x + 48, y, color
        )

        track_x = self.x + 280
        track_w = 360
        track_y = y + 12
        self._slider_hit = (track_x, track_y - 8, track_w, 26)
        _ = pygame.draw.rect(
            self.screen, self.COLOR_TRACK, (track_x, track_y, track_w, 10)
        )
        t = (self.cheats.speed_mult - self.SPEED_MIN) / (
            self.SPEED_MAX - self.SPEED_MIN
        )
        knob_x = track_x + int(t * track_w)
        _ = pygame.draw.rect(
            self.screen, self.COLOR_KNOB, (knob_x - 6, track_y - 5, 12, 20)
        )

    def _draw_back(
        self, label: str, y: int, color: tuple[int, int, int]
    ) -> None:
        self._blit(
            label,
            self.x + (self.BOX_W - self.BACK_W) // 2,
            y + 4,
            color,
        )
