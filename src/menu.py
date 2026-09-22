import pygame


class Menu:
    def __init__(self, screen: pygame.Surface, width: int, height: int):
        self.screen: pygame.Surface = screen
        self.width: int = width
        self.height: int = height

        self.title: pygame.Surface = pygame.image.load(
            "assets/title.png"
        ).convert_alpha()

        self.title_w: int = 1500
        self.title_h: int = 340

        self.play: pygame.Surface = pygame.image.load(
            "assets/play.png"
        ).convert_alpha()
        self.play_hovered: pygame.Surface = pygame.image.load(
            "assets/play_hovered.png"
        ).convert_alpha()
        self.play_w: int = 440
        self.play_h: int = 123

        self.hint: pygame.Surface = pygame.font.Font(None, 50).render(
            "ENTER / CLICK PLAY", True, (200, 200, 210)
        )
        self.hint_w: int = self.hint.get_size()[0]
        self.hint_h: int = self.hint.get_size()[1]

        self.highscore: pygame.Surface = pygame.font.Font(None, 50).render(
            "HIGHSCORES", True, (200, 200, 210)
        )
        self.highscore_hovered: pygame.Surface = pygame.font.Font(
            None, 50
        ).render("HIGHSCORES", True, (255, 255, 0))

        self.highscore_w: int = self.highscore.get_size()[0]
        self.highscore_h: int = self.highscore.get_size()[1]

        self.title_x: int = self.width // 2 - self.title_w // 2
        self.title_y: int = self.height // 4 - self.title_h // 2
        self.play_x: int = self.width // 2 - self.play_w // 2
        self.play_y: int = (self.height // 2) + 100
        self.hint_x: int = self.width // 2 - self.hint_w // 2
        self.hint_y: int = self.height // 3 + 180
        self.highscore_x: int = self.width // 2 - self.highscore_w // 2
        self.highscore_y: int = (self.height // 2) + 350
        self.blink_time: float = 0.0
        self.show_hint: bool = True

    def render(self, dt: float = 0.0) -> None:
        _ = self.screen.blit(self.title, (self.title_x, self.title_y))

        self.blink_time += dt
        if self.blink_time >= 0.5:
            self.blink_time -= 0.5
            self.show_hint = not self.show_hint

        if self.show_hint:
            _ = self.screen.blit(self.hint, (self.hint_x, self.hint_y))

        mx, my = pygame.mouse.get_pos()
        hovered_p = (
            self.play_x <= mx < self.play_x + self.play_w
            and self.play_y <= my < self.play_y + self.play_h
        )
        _ = self.screen.blit(
            self.play_hovered if hovered_p else self.play,
            (self.play_x, self.play_y),
        )

        hovered_h = (
            self.highscore_x <= mx < self.highscore_x + self.highscore_w
            and self.highscore_y <= my < self.highscore_y + self.highscore_h
        )
        _ = self.screen.blit(
            self.highscore_hovered if hovered_h else self.highscore,
            (self.highscore_x, self.highscore_y),
        )

    def click_at(self, mx: int, my: int) -> str | None:
        if (
            self.play_x <= mx < self.play_x + self.play_w
            and self.play_y <= my < self.play_y + self.play_h
        ):
            return "playing"
        if (
            self.highscore_x <= mx < self.highscore_x + self.highscore_w
            and self.highscore_y <= my < self.highscore_y + self.highscore_h
        ):
            return "highscore"
        return None
