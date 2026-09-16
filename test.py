from unpacked_mazegenerator.mazegenerator import MazeGenerator
import pygame


if __name__ == "__main__":
    maze = MazeGenerator()
    pygame.init()
    pygame.display.set_mode((1200, 700))
    pygame.display.set_caption("Pac-man")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
    pygame.display.quit()
    pygame.quit()
