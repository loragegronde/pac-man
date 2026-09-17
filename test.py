from unpacked_mazegenerator.mazegenerator import MazeGenerator
import pygame


class Player():
    def __init__(self) -> None:
        

def create_maze(maze: list[list[int]], img: pygame.Surface):
    for j in range(len(maze)):
        for i in range(len(maze[j])):
            draw_cell(maze[j][i], (i, j), img)


def draw_cell(wall: int, coordinates: tuple[int, int], img: pygame.Surface):
    x, y = coordinates
    if wall & 8:
        wall -= 8
        for i in range(50):
            img.set_at((x * 50, y * 50 + i), (0, 0, 255))
    if wall & 4:
        wall -= 4
        for i in range(50):
            img.set_at((x * 50 + i, y * 50 + 49), (0, 0, 255))
    if wall & 2:
        wall -= 2
        for i in range(50):
            img.set_at((x * 50 + 49, y * 50 + i), (0, 0, 255))
    if wall & 1:
        for i in range(50):
            img.set_at((x * 50 + i, y * 50), (0, 0, 255))


if __name__ == "__main__":
    maze = MazeGenerator()
    pygame.init()
    window = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Pac-man")
    running = True
    img = pygame.Surface((750, 750))
    create_maze(maze.maze, img)
    window.blit(img, (25, 25))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
        pygame.display.flip()
    pygame.display.quit()
    pygame.quit()
