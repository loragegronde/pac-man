import os
import pygame
import time
from src.visual.level_handler import LevelHandler
from pathlib import Path
from random import randint

from src.menu import Menu
from src.highscores import Highscores
from src.parsing import Config
from src.assets import Assets
from src.victory import Victory
from src.game_over import GameOver
from src.name_box import NameBox
from src.pause import PauseMenu
from src.cheats import Cheats
from src.cheat_menu import CheatMenu

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"


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
    def __init__(self, width: int, height: int, config: Config):
        _ = pygame.init()
        pygame.display.set_caption("pac-man")
        self.screen: pygame.Surface = pygame.display.set_mode((width, height))

        self.width: int = width
        self.height: int = height
        self.config: Config = config
        self.running: bool = False
        self.state: str = "menu"

        self.highscores: Highscores = Highscores(
            Path(config.highscore_filename)
        )
        self.assets: Assets = Assets()
        self.menu: Menu = Menu(
            self.screen, width, height, self.highscores, self.assets
        )
        self.cheats: Cheats = Cheats()
        self.game: LevelHandler = LevelHandler(
            self.screen, self.assets, config
        )
        self.name_box: NameBox = NameBox(
            self.screen, self.assets, width, height
        )
        self.victory: Victory = Victory(
            self.assets, self.screen, self.name_box, width, height
        )
        self.game_over: GameOver = GameOver(
            self.assets, self.screen, self.name_box, width, height
        )
        self.pause: PauseMenu = PauseMenu(
            self.screen, self.assets, width, height
        )
        self.cheat_menu: CheatMenu = CheatMenu(
            self.screen,
            self.assets,
            width,
            height,
            self.cheats,
            self.game,
        )
        self.pause_bg: pygame.Surface | None = None
        self.last_score: int = 0

    def run(self) -> None:
        background = make_background(self.width, self.height)

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
                    if self.state == "menu":
                        if event.key == pygame.K_UP:
                            self.menu.scroll_by(-1)
                        elif event.key == pygame.K_DOWN:
                            self.menu.scroll_by(1)
                        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                            # self.game.reset()
                            self.state = "playing"
                        elif event.key == pygame.K_ESCAPE:
                            self.running = False
                    elif self.state == "playing":
                        self.game.mazes[self.game.level].get_direction(event)
                        if event.key == pygame.K_ESCAPE:
                            self.pause.reset()
                            self.pause_bg = None
                            self.state = "pause"
                        elif event.key == pygame.K_v:
                            self.name_box.reset()
                            self.state = "victory"
                        elif event.key == pygame.K_o:
                            self.name_box.reset()
                            self.state = "game_over"
                    elif self.state == "pause":
                        action = self.pause.handle_keydown(event)
                        if action == "resume":
                            self.pause_bg = None
                            self.state = "playing"
                        elif action == "cheats":
                            self.cheat_menu.reset()
                            self.state = "cheats"
                        elif action == "menu":
                            self.pause_bg = None
                            self.state = "menu"
                    elif self.state == "cheats":
                        action = self.cheat_menu.handle_keydown(event)
                        if action == "back":
                            self.pause.reset()
                            self.state = "pause"
                    elif self.state in ("victory", "game_over"):
                        if event.key == pygame.K_ESCAPE:
                            self.state = "menu"
                        else:
                            action = self.name_box.handle_keydown(event)
                            if action == "submit":
                                name = self.name_box.text.strip()
                                self.highscores.add(name, self.last_score)
                                self.menu.set_last_score(name, self.last_score)
                                self.state = "menu"
                elif (
                    event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                ):
                    if self.state == "menu":
                        clicked = self.menu.click_at(*event.pos)
                        if clicked == "playing":
                            # self.game.reset()
                            self.state = "playing"
                    elif self.state == "pause":
                        action = self.pause.click_at(*event.pos)
                        if action == "resume":
                            self.pause_bg = None
                            self.state = "playing"
                        elif action == "cheats":
                            self.cheat_menu.reset()
                            self.state = "cheats"
                        elif action == "menu":
                            self.pause_bg = None
                            self.state = "menu"
                    elif self.state == "cheats":
                        action = self.cheat_menu.click_at(*event.pos)
                        if action == "back":
                            self.pause.reset()
                            self.state = "pause"
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.state == "cheats":
                        self.cheat_menu.mouse_up()
                elif event.type == pygame.MOUSEMOTION:
                    if self.state == "cheats":
                        self.cheat_menu.mouse_move(*event.pos)
                elif event.type == pygame.MOUSEWHEEL and self.state == "menu":
                    self.menu.scroll_by(-event.y)

            _ = self.screen.blit(background, (0, 0))
            if self.state == "menu":
                self.menu.render(dt)
            elif self.state == "playing":
                self.game.refresh_frame(dt)
                self.last_score = self.game.score
            elif self.state == "pause":
                if self.pause_bg is None:
                    self.game.refresh_frame(0.0)
                    self.pause.dim_screen()
                    self.pause_bg = self.screen.copy()
                _ = self.screen.blit(self.pause_bg, (0, 0))
                self.pause.render(dt)
            elif self.state == "cheats":
                if self.pause_bg is None:
                    self.game.refresh_frame(0.0)
                    self.pause.dim_screen()
                    self.pause_bg = self.screen.copy()
                _ = self.screen.blit(self.pause_bg, (0, 0))
                self.cheat_menu.render(dt)
            elif self.state == "victory":
                self.victory.render(dt)
            elif self.state == "game_over":
                self.game_over.render(dt)

            pygame.display.flip()

            elapsed = time.monotonic() - frame_start
            sleep_for = frame_time - elapsed
            if sleep_for > 0:
                time.sleep(sleep_for)

        pygame.quit()
