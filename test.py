from unpacked_mazegenerator.mazegenerator import MazeGenerator
import pygame


BLUE = (66, 147, 245)


class Player:
    def __init__(self) -> None:
        pass


class Maze:
    def __init__(self) -> None:
        self.maze = MazeGenerator().maze
        self.define_angles()

    def define_angles(self) -> None:
        self.angles: dict[str, list[tuple[int, int]]] = {
            "top_right": [(1, 1), (2, 1), (3, 2)],
            "top_left": [(-1, 1), (-2, 1), (-3, 2)],
            "botom_right": [(1, -1), (2, -1), (3, -2)],
            "botom_left": [(-1, -1), (-2, -1), (-3, -2)]
        }

    def create_maze(self, img: pygame.Surface):
        for j in range(len(self.maze)):
            for i in range(len(self.maze[j])):
                self.draw_cell(self.maze[j][i], (i, j), img)

    def draw_cell(self, wall: int, coordinates: tuple[int, int],
                  img: pygame.Surface):
        x, y = coordinates
        self.put_angles(wall, x, y, img)
        if wall & 8:
            wall -= 8
            for i in range(45):
                img.set_at((x * 50 + 5, y * 50 + i), BLUE)
        if wall & 4:
            wall -= 4
            for i in range(45):
                img.set_at((x * 50 + i, y * 50 + 44), BLUE)
        if wall & 2:
            wall -= 2
            for i in range(45):
                img.set_at((x * 50 + 44, y * 50 + i), BLUE)
        if wall & 1:
            for i in range(45):
                img.set_at((x * 50 + i, y * 50 + 5), BLUE)

    def draw_angles(self, wall: int, x: int, y: int,
                   img: pygame.Surface) -> None:
        # Botom left angle
        if ((wall & 8 and wall & 4) or not self.maze[y][x - 1] & 4):
            for corner_x, corner_y in self.angles["botom_left"]:
                new_x, new_y = x * 50 + corner_x, y * 50 + 44 + corner_y
                img.set_at((new_x, new_y), BLUE)
        else:
            for corner_x, corner_y in self.angles["top_right"]:
                new_x, new_y = x * 50 + corner_x, y * 50 + 44 + corner_y
                img.set_at((new_x, new_y), BLUE)


if __name__ == "__main__":
    maze = Maze()
    pygame.init()
    window = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Pac-man")
    running = True
    img = pygame.Surface((750, 750))
    maze.create_maze(img)
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
