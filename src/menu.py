import pygame

from src.assets import Assets, MenuLayout
from src.highscores import Highscores, ScoreEntry


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
    _ = pygame.draw.rect(
        screen,
        outer,
        pygame.Rect(x, y, w, h),
        width=thickness,
        border_radius=radius,
    )
    inset = gap + thickness
    _ = pygame.draw.rect(
        screen,
        inner,
        pygame.Rect(x + inset, y + inset, w - 2 * inset, h - 2 * inset),
        width=thickness,
        border_radius=max(4, radius - inset),
    )


class Menu:
    def __init__(
        self,
        screen: pygame.Surface,
        width: int,
        height: int,
        highscores: Highscores,
        assets: Assets,
    ):
        self.screen: pygame.Surface = screen
        self.highscores: Highscores = highscores
        self.assets: Assets = assets
        self.layout: MenuLayout = assets.menu_layout(width, height)

        self.scroll: int = 0
        self.last_score: ScoreEntry | None = None
        self.blink_time: float = 0.0
        self.show_hint: bool = True

    def set_last_score(self, name: str, score: int) -> None:
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
        return max(0, len(self.highscores.entries) - self.assets.VISIBLE_ROWS)

    def scroll_by(self, delta: int) -> None:
        self.scroll = max(0, min(self._max_scroll(), self.scroll + delta))

    def render(self, dt: float = 0.0) -> None:
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
        hovered = (
            lay.play_x <= mx < lay.play_x + a.PLAY_W
            and lay.play_y <= my < lay.play_y + a.PLAY_H
        )
        _ = self.screen.blit(
            a.play_hovered if hovered else a.play,
            (lay.play_x, lay.play_y),
        )
        self._draw_panel()

    def _draw_panel(self) -> None:
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
            ns = a.no_score
            _ = self.screen.blit(
                ns,
                (
                    x + (w - ns.get_width()) // 2,
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
                score_s = a.font.render(str(score), True, color)
                _ = self.screen.blit(rank_s, (rank_x, ry))
                _ = self.screen.blit(name_s, (name_x, ry))
                _ = self.screen.blit(
                    score_s, (score_right - score_s.get_width(), ry)
                )

        _ = self.screen.blit(a.up_arrow, lay.up_arrow.topleft)
        _ = self.screen.blit(a.down_arrow, lay.down_arrow.topleft)

        if self.last_score is not None:
            note = a.font_small.render(
                (
                    f"last: {str(self.last_score['name'])[:10]}  "
                    f"{int(self.last_score['score'])}"
                ),
                True,
                (255, 200, 80),
            )
            _ = self.screen.blit(note, (x + 36, y + h - 78))

    def click_at(self, mx: int, my: int) -> str | None:
        a = self.assets
        lay = self.layout
        if lay.up_arrow.collidepoint(mx, my):
            self.scroll_by(-1)
            return None
        if lay.down_arrow.collidepoint(mx, my):
            self.scroll_by(1)
            return None
        if (
            lay.play_x <= mx < lay.play_x + a.PLAY_W
            and lay.play_y <= my < lay.play_y + a.PLAY_H
        ):
            return "playing"
        return None
