import os
from src.visual.game import GameMode
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import time


class Graphics:
    def __init__(self, width: int, height: int):
        _ = pygame.init()
        pygame.display.set_caption("pac-man")
        self.screen: pygame.Surface = pygame.display.set_mode((width, height))
        self.running: bool = False
        self.game = GameMode(self.screen)

    def run(self) -> None:
        last = time.monotonic()
        FRAME_DURATION = 0.15
        anim_time = 0.0
        frame_index = 0

        self.running = True
        while self.running:
            now = time.monotonic()
            dt = now - last
            last = now

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                self.game.get_direction(event)

            anim_time += dt
            if anim_time >= FRAME_DURATION:
                anim_time -= FRAME_DURATION
                frame_index += 1

            _ = self.screen.fill((0, 0, 0))
            self.game.refresh_frame()
            pygame.display.flip()
        pygame.quit()
