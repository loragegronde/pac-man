from unpacked_mazegenerator.mazegenerator import MazeGenerator
import pygame


BLUE = (66, 147, 245)
ANGLES = {
    "W": (
        (((1, -1), (1, -2), (2, -3)), ((-1, -1), (-1, -2), (-2, -3))),
        (((1, 1), (1, 2), (2, 3)), ((-1, 1), (-1, 2), (-2, 3)))
    ),
    "S": (
        (((-1, -1), (-2, -1), (-3, -2)), ((-1, 1), (-2, 1), (-3, 2))),
        (((1, -1), (2, -1), (3, -2)), ((1, 1), (2, 1), (3, 2)))
    ),
    "E": (
        (((-1, 1), (-1, 2), (-2, 3)), ((1, 1), (1, 2), (2, 3))),
        (((-1, -1), (-1, -2), (-2, -3)), ((1, -1), (1, -2), (2, -3)))
    ),
    "N": (
        (((1, -1), (2, -1), (3, -2)), ((1, 1), (2, 1), (3, 2))),
        (((-1, -1), (-2, -1), (-3, -2)), ((-1, 1), (-2, 1), (-3, 2)))
    )
}
# format:
# left/ right angles
# interior/exterior


class Player:
    def __init__(self) -> None:
        pass


class Maze:
    def __init__(self) -> None:
        self.maze = MazeGenerator().maze
        self.define_angles()

    def define_angles(self) -> None:
        self.angles: dict[int, tuple] = {
            8: (1, 4, (0, -1), (0, 1), ANGLES["W"]),
            4: (8, 2, (0, -1), (0, 1), ANGLES["S"]),
            2: (4, 1, (0, -1), (0, 1), ANGLES["E"]),
            1: (2, 8, (0, -1), (0, 1), ANGLES["N"])
        }

    def create_maze(self, img: pygame.Surface):
        for j in range(len(self.maze)):
            for i in range(len(self.maze[j])):
                self.draw_cell(self.maze[j][i], (i, j), img)

    def draw_cell(self, wall: int, coordinates: tuple[int, int],
                  img: pygame.Surface):
        x, y = coordinates
        if wall & 8:
            wall -= 8
            left, right, coord_l, coord_r, pixels = self.angles[8]
            first = self.draw_angles(8, left, coord_l, pixels[0],
                                     (x * 50 + 3, y * 50 + 3))
            second = self.draw_angles(8, right, coord_r, pixels[1],
                                      (x * 50 + 3, y * 50 + 47))
            for i in range(3 - first, 48 + second):
                img.set_at((x * 50 + 3, y * 50 + i), BLUE)
        if wall & 4:
            wall -= 4
            left, right, coord_l, coord_r, pixels = self.angles[4]
            first = self.draw_angles(4, left, coord_l, pixels[0],
                                     (x * 50 + 3, y * 50 + 47))
            second = self.draw_angles(4, right, coord_r, pixels[1],
                                      (x * 50 + 47, y * 50 + 47))
            for i in range(3 - first, 48 + second):
                img.set_at((x * 50 + i, y * 50 + 47), BLUE)
        if wall & 2:
            wall -= 2
            left, right, coord_l, coord_r, pixels = self.angles[2]
            first = self.draw_angles(2, left, coord_l, pixels[0],
                                     (x * 50 + 47, y * 50 + 47))
            second = self.draw_angles(2, right, coord_r, pixels[1],
                                      (x * 50 + 47, y * 50 + 3))
            for i in range(3 - first, 48 + second):
                img.set_at((x * 50 + 47, y * 50 + i), BLUE)
        if wall & 1:
            left, right, coord_l, coord_r, pixels = self.angles[1]
            first = self.draw_angles(1, left, coord_l, pixels[0],
                                     (x * 50 + 47, y * 50 + 3))
            second = self.draw_angles(1, right, coord_r, pixels[1],
                                      (x * 50 + 3, y * 50 + 3))
            for i in range(3 - first, 48 + second):
                img.set_at((x * 50 + i, y * 50 + 3), BLUE)

    def draw_angles(self, wall: int, side: int,
                    coord_side: tuple[int, int], pixels,
                    coordinates: tuple[int, int]) -> int:
        x, y = coordinates
        side_x, side_y = x + coord_side[0], y + coord_side[1]
        if side:
            for corner_x, corner_y in pixels[0]:
                new_x, new_y = x + corner_x, y + corner_y
                img.set_at((new_x, new_y), BLUE)
        elif self.maze[side_y][side_x] & wall:
            return 3
        else:
            for corner_x, corner_y in pixels[1]:
                new_x, new_y = x + corner_x, y + corner_y
                img.set_at((new_x, new_y), BLUE)
        return 0


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
