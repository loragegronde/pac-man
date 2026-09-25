from unpacked_mazegenerator.mazegenerator import MazeGenerator
from src.visual.get_assets import AssetHandler
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
        (((1, 1), (2, 1), (3, 2)), ((1, -1), (2, -1), (3, -2))),
        (((-1, 1), (-2, 1), (-3, 2)), ((-1, -1), (-2, -1), (-3, -2)))
    )
}
MOVEMENT = {
    "W": (-1, 0),
    "S": (0, 1),
    "E": (1, 0),
    "N": (0, -1)
}
# format:
# left/ right angles
# interior/exterior


class Maze:
    def __init__(self) -> None:
        self.maze = MazeGenerator().maze
        self.define_angles()

    def define_angles(self) -> None:
        self.angles: dict[int, tuple] = {
            8: (1, 4, (0, -1), (0, 1), ANGLES["W"]),
            4: (8, 2, (-1, 0), (1, 0), ANGLES["S"]),
            2: (4, 1, (0, 1), (0, -1), ANGLES["E"]),
            1: (2, 8, (1, 0), (-1, 0), ANGLES["N"])
        }

    def create_maze(self, img: pygame.Surface):
        for j in range(len(self.maze)):
            for i in range(len(self.maze[j])):
                self.draw_cell(self.maze[j][i], (i, j), img)

    def draw_cell(self, wall: int, coordinates: tuple[int, int],
                  img: pygame.Surface):
        x, y = coordinates
        cell = wall
        if wall == 15:
            return
        if wall & 8:
            wall -= 8
            left, right, coord_l, coord_r, pixels = self.angles[8]
            first = self.draw_angles(8, left, coord_l, pixels[0],
                                     (x * 50 + 3, y * 50 + 3), (x, y), cell)
            second = self.draw_angles(8, right, coord_r, pixels[1],
                                      (x * 50 + 3, y * 50 + 47), (x, y), cell)
            for i in range(3 - first, 48 + second):
                img.set_at((x * 50 + 3, y * 50 + i), BLUE)
        if wall & 4:
            wall -= 4
            left, right, coord_l, coord_r, pixels = self.angles[4]
            first = self.draw_angles(4, left, coord_l, pixels[0],
                                     (x * 50 + 3, y * 50 + 47), (x, y), cell)
            second = self.draw_angles(4, right, coord_r, pixels[1],
                                      (x * 50 + 47, y * 50 + 47), (x, y), cell)
            for i in range(3 - first, 48 + second):
                img.set_at((x * 50 + i, y * 50 + 47), BLUE)
        if wall & 2:
            wall -= 2
            left, right, coord_l, coord_r, pixels = self.angles[2]
            first = self.draw_angles(2, left, coord_l, pixels[0],
                                     (x * 50 + 47, y * 50 + 47), (x, y), cell)
            second = self.draw_angles(2, right, coord_r, pixels[1],
                                      (x * 50 + 47, y * 50 + 3), (x, y), cell)
            for i in range(3 - second, 48 + first):
                img.set_at((x * 50 + 47, y * 50 + i), BLUE)
        if wall & 1:
            left, right, coord_l, coord_r, pixels = self.angles[1]
            first = self.draw_angles(1, left, coord_l, pixels[0],
                                     (x * 50 + 47, y * 50 + 3), (x, y), cell)
            second = self.draw_angles(1, right, coord_r, pixels[1],
                                      (x * 50 + 3, y * 50 + 3), (x, y), cell)
            for i in range(3 - second, 48 + first):
                img.set_at((x * 50 + i, y * 50 + 3), BLUE)

    def draw_angles(self, wall: int, side: int,
                    coord_side: tuple[int, int], pixels,
                    coordinates: tuple[int, int],
                    cell_coord: tuple[int, int], cell: int) -> int:
        x, y = coordinates
        v_x, v_y = coord_side
        side_x, side_y = cell_coord[0] + v_x, cell_coord[1] + v_y
        if cell & side:
            for corner_x, corner_y in pixels[0]:
                new_x, new_y = x + corner_x - v_x * 3, y + corner_y - v_y * 3
                img.set_at((new_x, new_y), BLUE)
            return -3
        elif not (0 <= side_y <= 15 and 0 <= side_x <= 15):
            return 3
        elif self.maze[side_y][side_x] & wall:
            return 3
        else:
            for corner_x, corner_y in pixels[1]:
                new_x, new_y = x + corner_x, y + corner_y
                img.set_at((new_x, new_y), BLUE)
        return 0


class Player():
    def __init__(self, maze: Maze, img) -> None:
        self.maze = maze
        self.define_start_pos()
        self.direction = "E"
        self.next_direction = "E"
        self.spawn = assets.pac_man_spawn
        self.movement = assets.pac
        self.frame = 0
        self.img = img
        self.update_pos()

    def define_start_pos(self):
        max_x = len(self.maze.maze[0])
        max_y = len(self.maze.maze)
        self.maze_pos = (max_x // 2, max_y // 2)
        self.pos = (self.maze_pos[0] * 50 + 7, self.maze_pos[1] * 50 + 7)

    def update_pos(self):
        x, y = self.pos
        next_x, next_y = MOVEMENT[self.direction]
        new_x, new_y = (x + next_x, y + next_y)
        _ = window.blit(
                self.movement[self.direction][self.frame % 3],
                (new_x + 25, new_y + 25)
            )
        # self.pos = (new_x, new_y)
        self.frame = self.frame + 1 % 3

    def define_collisions(self):
        pass


class GameMode():
    def __init__(self, maze: Maze, player: Player) -> None:
        self.maze = maze
        self.player = player

    def refresh_frame(self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.player.direction = "W"
            if event.key == pygame.K_DOWN:
                self.player.direction = "S"
            if event.key == pygame.K_RIGHT:
                self.player.direction = "E"
            if event.key == pygame.K_UP:
                self.player.direction = "N"


if __name__ == "__main__":
    maze = Maze()
    pygame.init()
    window = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Pac-man")
    assets = AssetHandler()
    assets.get_mobs("assets/sprites.png")
    running = True
    img = pygame.Surface((750, 750))
    player = Player(maze, img)
    maze.create_maze(img)
    window.blit(img, (25, 25))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_LEFT:
                    player.direction = "W"
                if event.key == pygame.K_DOWN:
                    player.direction = "S"
                if event.key == pygame.K_RIGHT:
                    player.direction = "E"
                if event.key == pygame.K_UP:
                    player.direction = "N"
        _ = window.fill((0, 0, 0))
        window.blit(img, (25, 25))
        player.update_pos()
        pygame.display.flip()
    pygame.display.quit()
    pygame.quit()
