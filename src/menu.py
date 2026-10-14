"""Main menu UI and shared rounded-rect drawing helpers."""

import pygame

from src.assets import Assets, MenuLayout
from src.highscores import Highscores, ScoreEntry


def point_in(mx: int, my: int, x: int, y: int, w: int, h: int) -> bool:
    """Return True if the point lies inside the rectangle.

    Args:
        mx: Point x.
        my: Point y.
        x: Rect left.
        y: Rect top.
        w: Rect width.
        h: Rect height.

    Returns:
        Whether ``(mx, my)`` is inside the rect.
    """
    return x <= mx < x + w and y <= my < y + h


def draw_quarter_circle_outline(
    screen: pygame.Surface,
    cx: int,
    cy: int,
    radius: int,
    thickness: int,
    color: tuple[int, int, int],
    dx_sign: int,
    dy_sign: int,
) -> None:
    """Draw one corner arc of a rounded rectangle outline.

    Args:
        screen: Target surface.
        cx: Arc center x.
        cy: Arc center y.
        radius: Outer radius.
        thickness: Stroke width in pixels.
        color: RGB color.
        dx_sign: Horizontal quadrant (+1 or -1).
        dy_sign: Vertical quadrant (+1 or -1).
    """
    r_outer = radius
    r_inner = max(0, radius - thickness)
    r_out_sq = r_outer * r_outer
    r_in_sq = r_inner * r_inner
    for i in range(radius + 1):
        for j in range(radius + 1):
            dist_sq = i * i + j * j
            if r_in_sq < dist_sq <= r_out_sq:
                screen.set_at((cx + dx_sign * i, cy + dy_sign * j), color)


def draw_round_rect_outline(
    screen: pygame.Surface,
    x: int,
    y: int,
    w: int,
    h: int,
    color: tuple[int, int, int],
    radius: int = 18,
    thickness: int = 3,
) -> None:
    """Draw a rounded rectangle outline with pixel corners.

    Args:
        screen: Target surface.
        x: Left.
        y: Top.
        w: Width.
        h: Height.
        color: RGB color.
        radius: Corner radius.
        thickness: Stroke width.
    """
    if w <= 0 or h <= 0 or thickness <= 0:
        return
    r = max(1, min(radius, w // 2, h // 2))
    t = min(thickness, r)

    draw_quarter_circle_outline(screen, x + r, y + r, r, t, color, -1, -1)
    draw_quarter_circle_outline(
        screen, x + w - 1 - r, y + r, r, t, color, 1, -1
    )
    draw_quarter_circle_outline(
        screen, x + r, y + h - 1 - r, r, t, color, -1, 1
    )
    draw_quarter_circle_outline(
        screen, x + w - 1 - r, y + h - 1 - r, r, t, color, 1, 1
    )

    span_w = w - 2 * r
    span_h = h - 2 * r
    if span_w > 0:
        _ = pygame.draw.rect(screen, color, (x + r, y, span_w, t))
        _ = pygame.draw.rect(screen, color, (x + r, y + h - t, span_w, t))
    if span_h > 0:
        _ = pygame.draw.rect(screen, color, (x, y + r, t, span_h))
        _ = pygame.draw.rect(screen, color, (x + w - t, y + r, t, span_h))


def draw_double_round_rect(
    screen: pygame.Surface,
    x: int,
    y: int,
    w: int,
    h: int,
    outer: tuple[int, int, int],
    inner: tuple[int, int, int],
    radius: int = 18,
    gap: int = 5,
    thickness: int = 3,
) -> None:
    """Draw outer and inner rounded borders for UI panels.

    Args:
        screen: Target surface.
        x: Left.
        y: Top.
        w: Width.
        h: Height.
        outer: Outer border color.
        inner: Inner border color.
        radius: Outer corner radius.
        gap: Space between the two borders.
        thickness: Stroke width.
    """
    draw_round_rect_outline(screen, x, y, w, h, outer, radius, thickness)
    inset = gap + thickness
    draw_round_rect_outline(
        screen,
        x + inset,
        y + inset,
        w - 2 * inset,
        h - 2 * inset,
        inner,
        max(1, radius - inset),
        thickness,
    )


class Menu:
    """Title screen with play, exit, instructions, and highscores."""

    def __init__(
        self,
        screen: pygame.Surface,
        width: int,
        height: int,
        highscores: Highscores,
        assets: Assets,
    ):
        """Build the menu layout from screen size and assets.

        Args:
            screen: Display surface.
            width: Window width.
            height: Window height.
            highscores: Shared highscore table.
            assets: Images, fonts, and layout constants.
        """
        self.screen: pygame.Surface = screen
        self.highscores: Highscores = highscores
        self.assets: Assets = assets
        self.layout: MenuLayout = assets.menu_layout(width, height)

        self.scroll: int = 0
        self.last_score: ScoreEntry | None = None
        self.blink_time: float = 0.0
        self.show_hint: bool = True

    def set_last_score(self, name: str, score: int) -> None:
        """Highlight a freshly submitted score in the list.

        Args:
            name: Player name.
            score: Player score.
        """
        self.last_score = {"name": name, "score": score}
        self.highscores.reload()
        rows = self.assets.VISIBLE_ROWS
        for i, e in enumerate(self.highscores.entries):
            if e["name"] == name and e["score"] == score:
                if i < self.scroll:
                    self.scroll = i
                elif i >= self.scroll + rows:
                    self.scroll = max(0, i - rows + 1)
                break

    def _max_scroll(self) -> int:
        """Largest valid scroll offset for the highscore list."""
        return max(0, len(self.highscores.entries) - self.assets.VISIBLE_ROWS)

    def scroll_by(self, delta: int) -> None:
        """Move the highscore list up or down.

        Args:
            delta: Rows to scroll (negative = up).
        """
        self.scroll = max(0, min(self._max_scroll(), self.scroll + delta))

    def render(self, dt: float = 0.0) -> None:
        """Draw the title screen.

        Args:
            dt: Frame delta used for the blinking hint.
        """
        a = self.assets
        lay = self.layout

        _ = self.screen.blit(a.title, (lay.title_x, lay.title_y))

        self.blink_time += dt
        if self.blink_time >= 0.5:
            self.blink_time -= 0.5
            self.show_hint = not self.show_hint
        if self.show_hint:
            _ = self.screen.blit(a.hint, (lay.hint_x, lay.hint_y))

        mx, my = pygame.mouse.get_pos()
        play_hovered = point_in(
            mx, my, lay.play_x, lay.play_y, a.PLAY_W, a.PLAY_H
        )
        _ = self.screen.blit(
            a.play_hovered if play_hovered else a.play,
            (lay.play_x, lay.play_y),
        )

        exit_hovered = point_in(
            mx, my, lay.exit_x, lay.exit_y, lay.exit_w, lay.exit_h
        )
        draw_double_round_rect(
            self.screen,
            lay.exit_x,
            lay.exit_y,
            lay.exit_w,
            lay.exit_h,
            outer=a.BORDER_OUTER,
            inner=a.BORDER_INNER,
            radius=a.BORDER_RADIUS,
        )
        exit_color = (255, 255, 120) if exit_hovered else (220, 220, 230)
        exit_label = a.font_medium.render("EXIT", True, exit_color)
        _ = self.screen.blit(
            exit_label,
            (
                lay.exit_x
                + (lay.exit_w - a.EXIT_LABEL_W) // 2
                + a.EXIT_LABEL_OX,
                lay.exit_y + (lay.exit_h - a.FONT_MEDIUM_H) // 2,
            ),
        )

        instr_hovered = point_in(
            mx,
            my,
            lay.instructions_x,
            lay.instructions_y,
            lay.instructions_w,
            lay.instructions_h,
        )
        instr_color = (220, 220, 120) if instr_hovered else (140, 140, 155)
        instr_label = a.font.render("INSTRUCTIONS", True, instr_color)
        _ = self.screen.blit(
            instr_label,
            (
                lay.instructions_x
                + (lay.instructions_w - a.INSTR_LABEL_W) // 2,
                lay.instructions_y,
            ),
        )

        self._draw_panel()

    def _draw_panel(self) -> None:
        """Draw the highscore panel and scroll arrows."""
        a = self.assets
        lay = self.layout
        x, y, w, h = lay.panel_x, lay.panel_y, lay.panel_w, lay.panel_h

        draw_double_round_rect(
            self.screen,
            x,
            y,
            w,
            h,
            outer=a.BORDER_OUTER,
            inner=a.BORDER_INNER,
            radius=a.BORDER_RADIUS,
        )

        bx = x + (w - a.hs_banner_w) // 2
        by = y + a.BANNER_TOP
        _ = self.screen.blit(a.hs_banner, (bx, by))

        list_top = by + a.hs_banner_h + a.LIST_TOP_GAP
        rank_x = x + a.RANK_OX
        name_x = x + a.NAME_OX
        score_right = x + w - a.SCORE_RIGHT_PAD

        if self.highscores.empty:
            _ = self.screen.blit(
                a.no_score,
                (
                    x + (w - a.no_score_w) // 2,
                    list_top + (a.VISIBLE_ROWS * a.ROW_H) // 2,
                ),
            )
        else:
            entries = self.highscores.entries
            end = min(len(entries), self.scroll + a.VISIBLE_ROWS)
            for row, idx in enumerate(range(self.scroll, end)):
                entry = entries[idx]
                name = str(entry["name"])[:10]
                score = int(entry["score"])
                highlight = (
                    self.last_score is not None
                    and name == self.last_score["name"]
                    and score == self.last_score["score"]
                )
                color = (255, 255, 100) if highlight else (230, 230, 240)
                ry = list_top + row * a.ROW_H
                rank_s = a.font.render(f"{idx + 1:2d}.", True, color)
                name_s = a.font.render(name, True, color)
                score_str = str(score)
                score_s = a.font.render(score_str, True, color)
                score_w = len(score_str) * a.DIGIT_W
                _ = self.screen.blit(rank_s, (rank_x, ry))
                _ = self.screen.blit(name_s, (name_x, ry))
                _ = self.screen.blit(score_s, (score_right - score_w, ry))

        _ = self.screen.blit(a.up_arrow, lay.up_arrow.topleft)
        _ = self.screen.blit(a.down_arrow, lay.down_arrow.topleft)

    def click_at(self, mx: int, my: int) -> str | None:
        """Handle a click on menu controls.

        Args:
            mx: Mouse x.
            my: Mouse y.

        Returns:
            Next state name (``playing``, ``instructions``, ``exit``),
            or None for scroll-only clicks.
        """
        a = self.assets
        lay = self.layout
        up = lay.up_arrow
        down = lay.down_arrow
        if point_in(mx, my, up.x, up.y, up.w, up.h):
            self.scroll_by(-1)
            return None
        if point_in(mx, my, down.x, down.y, down.w, down.h):
            self.scroll_by(1)
            return None
        if point_in(mx, my, lay.play_x, lay.play_y, a.PLAY_W, a.PLAY_H):
            return "playing"
        if point_in(
            mx,
            my,
            lay.instructions_x,
            lay.instructions_y,
            lay.instructions_w,
            lay.instructions_h,
        ):
            return "instructions"
        if point_in(mx, my, lay.exit_x, lay.exit_y, lay.exit_w, lay.exit_h):
            return "exit"
        return None
