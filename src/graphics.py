import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import time
import random


def crop(
    sheet: pygame.Surface, x: int, y: int, w: int, h: int
) -> pygame.Surface:
    image = pygame.Surface((w, h), pygame.SRCALPHA)
    _ = image.blit(sheet, (0, 0), (x, y, w, h))
    return image


def get_star_list(width: int, height: int) -> list[tuple[int, int]]:

    stars: list[tuple[int, int]] = []
    spacing = 100
    row = width // spacing
    col = height // spacing

    for i in range(row):
        for j in range(col):
            x = (i * spacing) + random.randint(0, spacing - 1)
            y = (j * spacing) + random.randint(0, spacing - 1)
            stars.append((x, y))

    return stars


def make_background(width: int, height: int) -> pygame.Surface:
    bg = pygame.Surface((width, height))
    for y in range(height):
        t = y / max(height - 1, 1)
        r = int(4 + 10 * t)
        g = int(4 + 8 * t)
        b = int(18 + 28 * t)
        _ = bg.fill((r, g, b), pygame.Rect(0, y, width, 1))

    star = (220, 220, 255)
    dim = (80, 90, 140)
    stars = get_star_list(width, height)
    for i, (sx, sy) in enumerate(stars):
        if 0 <= sx < width and 0 <= sy < height:
            bg.set_at((sx, sy), star if i % 3 == 0 else dim)
            if i % 5 == 0 and sx + 1 < width:
                bg.set_at((sx + 1, sy), dim)
    return bg


class Graphics:
    def __init__(self, width: int, height: int):
        _ = pygame.init()
        pygame.display.set_caption("pac-man")
        self.width: int = width
        self.height: int = height
        self.screen: pygame.Surface = pygame.display.set_mode((width, height))
        self.running: bool = False
        self.state: str = "menu"

    def run(self) -> None:
        background = make_background(self.width, self.height)

        title_full = pygame.image.load("assets/title.png").convert_alpha()
        title = crop(title_full, 0, 0, 852, 195)
        title_w, title_h = 852, 190

        play = pygame.image.load("assets/play.png").convert_alpha()
        play_hovered = pygame.image.load(
            "assets/play_hovered.png"
        ).convert_alpha()
        play_w, play_h = 180, 63

        hint = pygame.font.Font(None, 28).render(
            "ENTER / CLICK PLAY", True, (200, 200, 210)
        )
        hint_w, hint_h = hint.get_size()

        gap = 28
        block_h = title_h + gap + play_h + gap + hint_h

        title_x = self.width // 2 - title_w // 2
        title_y = (self.height - block_h) // 2
        play_x = self.width // 2 - play_w // 2
        play_y = title_y + title_h + gap
        hint_x = self.width // 2 - hint_w // 2
        hint_y = play_y + play_h + gap

        playing_msg = pygame.font.Font(None, 48).render(
            "GAME START - ESC for menu", True, (255, 255, 0)
        )
        pm_w, pm_h = playing_msg.get_size()
        playing_msg_x = self.width // 2 - pm_w // 2
        playing_msg_y = self.height // 2 - pm_h // 2

        self.running = True
        while self.running:
            now = time.monotonic()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == "playing":
                            self.state = "menu"
                        else:
                            self.running = False
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if self.state == "menu":
                            self.state = "playing"
                elif (
                    event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                ):
                    if self.state == "menu":
                        mx, my = event.pos
                        if (
                            play_x <= mx < play_x + play_w
                            and play_y <= my < play_y + play_h
                        ):
                            self.state = "playing"

            _ = self.screen.blit(background, (0, 0))

            if self.state == "menu":
                _ = self.screen.blit(title, (title_x, title_y))

                mx, my = pygame.mouse.get_pos()
                hovered = (
                    play_x <= mx < play_x + play_w
                    and play_y <= my < play_y + play_h
                )
                _ = self.screen.blit(
                    play_hovered if hovered else play, (play_x, play_y)
                )

                if int(now * 2) % 2 == 0:
                    _ = self.screen.blit(hint, (hint_x, hint_y))
            else:
                _ = self.screen.blit(
                    playing_msg, (playing_msg_x, playing_msg_y)
                )

            pygame.display.flip()

        pygame.quit()
