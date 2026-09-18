from unpacked_mazegenerator.mazegenerator import MazeGenerator
import pygame


class Player:
    def __init__(self) -> None:
        pass


class Maze:
    def __init__(self) -> None:
        pass

    def define_angles(self) -> None:
        self.angles: dict[str, list[tuple[int, int]]] = {
            "up_right": [(1, -1), (2, -1), (3, -2)],
            "up_left": [(-1, -1), (-2, -1), (-3, -2)],
            "botom_right": [],
            "botom_left": []
        }

    def create_maze(self, maze: list[list[int]], img: pygame.Surface):
        for j in range(len(maze)):
            for i in range(len(maze[j])):
                self.draw_cell(maze[j][i], (i, j), img)

    def draw_cell(self, wall: int, coordinates: tuple[int, int],
                  img: pygame.Surface):
        x, y = coordinates
        BLUE = (66, 147, 245)
        if wall & 8:
            wall -= 8
            for i in range(50):
                img.set_at((x * 50 + 5, y * 50 + i), BLUE)
        if wall & 4:
            wall -= 4
            for i in range(50):
                img.set_at((x * 50 + i, y * 50 + 44), BLUE)
        if wall & 2:
            wall -= 2
            for i in range(50):
                img.set_at((x * 50 + 44, y * 50 + i), BLUE)
        if wall & 1:
            for i in range(50):
                img.set_at((x * 50 + i, y * 50 + 5), BLUE)


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
