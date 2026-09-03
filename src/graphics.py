import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import time



class Graphics:
    def __init__(self, width: int, height: int):
        _ = pygame.init()
        pygame.display.set_caption("pac-man")
        self.screen: pygame.Surface = pygame.display.set_mode((width, height))
        self.running: bool = False

    def run(self) -> None:
        last = time.monotonic()

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
            _ = self.screen.fill((0, 0, 0))
            img = pygame.image.load("assets/pacman.png").convert_alpha()
            _ = self.screen.blit(img, (1, 1))
            pygame.display.flip()
        pygame.quit()
