import pygame

from src.utils.assets import Assets


class Hud:
    """Display curren't game state"""

    VALUE_COLOR: tuple[int, int, int] = (255, 220, 80)

    def __init__(self, screen: pygame.Surface, assets: Assets) -> None:
        """Define hub's place on window"""
        self.screen: pygame.Surface = screen
        self.assets: Assets = assets
        self.x: int = 40
        self.y: int = 80

    def render(
        self,
        score: int,
        lives: int,
        level: int,
        time_left: float,
        dt: float = 0.0,
    ) -> None:
        """Display all game's informations on top right window

        Args:
            score: sum of all game's score
            lives: remaining lives of the player
            level: current level the player is at
            time_left: time_remaining before end of the level
        """
        _ = dt
        a = self.assets
        rows = (
            ("SCORE", str(score)),
            ("LIVES", str(lives)),
            ("LEVEL", str(level + 1)),
            ("TIME", self._format_time(time_left)),
        )
        y = self.y
        for label, value in rows:
            _ = self.screen.blit(a.hud_labels[label], (self.x, y))
            value_s = a.font_medium.render(value, True, self.VALUE_COLOR)
            _ = self.screen.blit(value_s, (self.x, y + 48))
            y += 110

    def _format_time(self, time_left: float) -> str:
        """Format time left into printable string"""
        t = max(0, int(time_left + 0.999))
        return f"{t // 60:02d}:{t % 60:02d}"
