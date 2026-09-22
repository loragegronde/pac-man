import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import time
from random import randint

from src.menu import Menu


def crop(
    sheet: pygame.Surface, x: int, y: int, w: int, h: int
) -> pygame.Surface:
    image = pygame.Surface((w, h), pygame.SRCALPHA)
    _ = image.blit(sheet, (0, 0), (x, y, w, h))
    return image


def get_star_list(width: int, height: int) -> list[tuple[int, int]]:

    stars: list[tuple[int, int]] = []
    spacing = 60
    row = width // spacing
    col = height // spacing

    for i in range(col):
        spacing += 7
        for j in range(row):
            x = (j * spacing) + randint(0, spacing - 1)
            y = (i * spacing) + randint(0, spacing - 1)
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
    stars = get_star_list(width, height)
    for sx, sy in stars:
        _ = pygame.draw.circle(
            bg,
            (randint(120, 220), randint(120, 220), randint(120, 220)),
            (sx, sy),
            randint(1, 4),
        )

    return bg


class Graphics:
    def __init__(self, width: int, height: int):
        _ = pygame.init()
        pygame.display.set_caption("pac-man")
        self.screen: pygame.Surface = pygame.display.set_mode((width, height))

        self.width: int = width
        self.height: int = height
        self.running: bool = False
        self.state: str = "menu"

    def run(self) -> None:
        background = make_background(self.width, self.height)
        menu = Menu(self.screen, self.width, self.height)

        fps = 60
        frame_time = 1.0 / fps
        last = time.monotonic()

        self.running = True
        while self.running:
            frame_start = time.monotonic()
            now = frame_start
            dt = now - last
            last = now

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if (
                            self.state == "playing"
                            or self.state == "highscore"
                        ):
                            self.state = "menu"
                        else:
                            self.running = False
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if self.state == "menu":
                            self.state = "playing"
                    elif event.key is pygame.K_TAB:
                        if self.state == "menu":
                            self.state = "highscore"
                elif (
                    event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                ):
                    if self.state == "menu":
                        clicked = menu.click_at(*event.pos)
                        if clicked is not None:
                            self.state = clicked

            _ = self.screen.blit(background, (0, 0))
            if self.state == "menu":
                menu.render(dt)
            elif self.state == "playing":
                pass
            elif self.state == "highscore":
                pass
            pygame.display.flip()

            elapsed = time.monotonic() - frame_start
            sleep_for = frame_time - elapsed
            if sleep_for > 0:
                time.sleep(sleep_for)

        pygame.quit()
