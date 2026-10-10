from unpacked_mazegenerator.mazegenerator import MazeGenerator
import pygame

type Point = tuple[int, int]
type Color = tuple[int, int, int]
type CornerTriple = tuple[Point, Point, Point]
type SideCorners = tuple[CornerTriple, CornerTriple]
type WallAngles = tuple[SideCorners, SideCorners]
type AngleEntry = tuple[int, int, Point, Point, WallAngles]


class Maze:
    BLUE: Color = (66, 147, 245)
    ANGLES: dict[int, WallAngles] = {
        8: (
            (((1, -1), (1, -2), (2, -3)), ((-1, -1), (-1, -2), (-2, -3))),
            (((1, 1), (1, 2), (2, 3)), ((-1, 1), (-1, 2), (-2, 3))),
        ),
        4: (
            (((-1, -1), (-2, -1), (-3, -2)), ((-1, 1), (-2, 1), (-3, 2))),
            (((1, -1), (2, -1), (3, -2)), ((1, 1), (2, 1), (3, 2))),
        ),
        2: (
            (((-1, 1), (-1, 2), (-2, 3)), ((1, 1), (1, 2), (2, 3))),
            (((-1, -1), (-1, -2), (-2, -3)), ((1, -1), (1, -2), (2, -3))),
        ),
        1: (
            (((1, 1), (2, 1), (3, 2)), ((1, -1), (2, -1), (3, -2))),
            (((-1, 1), (-2, 1), (-3, 2)), ((-1, -1), (-2, -1), (-3, -2))),
        ),
    }

    def __init__(self, size: Point) -> None:
        self.maze: list[list[int]] = MazeGenerator(size).maze
        self.forty_two: set[Point] = {
            (i, j)
            for i in range(len(self.maze[0]))
            for j in range(len(self.maze))
            if self.maze[j][i] == 15
        }
        self.img: pygame.Surface = pygame.Surface((1, 1))
        self.define_angles()

    def define_angles(self) -> None:
        self.angles: dict[int, AngleEntry] = {
            8: (1, 4, (0, -1), (0, 1), self.ANGLES[8]),
            4: (8, 2, (-1, 0), (1, 0), self.ANGLES[4]),
            2: (4, 1, (0, 1), (0, -1), self.ANGLES[2]),
            1: (2, 8, (1, 0), (-1, 0), self.ANGLES[1]),
        }

    def modify_42(self, i: int, j: int) -> None:
        wall = 15
        if (i - 1, j) in self.forty_two:
            wall -= 8
        if (i, j + 1) in self.forty_two:
            wall -= 4
        if (i + 1, j) in self.forty_two:
            wall -= 2
        if (i, j - 1) in self.forty_two:
            wall -= 1
        self.maze[j][i] = wall

    def create_maze(self, img: pygame.Surface) -> None:
        self.img = img
        for cell in self.forty_two:
            self.modify_42(*cell)
        for j in range(len(self.maze)):
            for i in range(len(self.maze[j])):
                self.draw_cell(self.maze[j][i], (i, j))
        for cell in self.forty_two:
            i, j = cell
            self.maze[j][i] = 15

    def draw_cell(self, wall: int, coordinates: Point) -> None:
        x, y = coordinates
        cell = wall
        if wall & 8:
            wall -= 8
            left, right, coord_l, coord_r, pixels = self.angles[8]
            first = self.draw_angles(
                8,
                left,
                coord_l,
                pixels[0],
                (x * 50 + 3, y * 50 + 3),
                (x, y),
                cell,
            )
            second = self.draw_angles(
                8,
                right,
                coord_r,
                pixels[1],
                (x * 50 + 3, y * 50 + 47),
                (x, y),
                cell,
            )
            for i in range(3 - first, 48 + second):
                self.img.set_at((x * 50 + 3, y * 50 + i), self.BLUE)
        if wall & 4:
            wall -= 4
            left, right, coord_l, coord_r, pixels = self.angles[4]
            first = self.draw_angles(
                4,
                left,
                coord_l,
                pixels[0],
                (x * 50 + 3, y * 50 + 47),
                (x, y),
                cell,
            )
            second = self.draw_angles(
                4,
                right,
                coord_r,
                pixels[1],
                (x * 50 + 47, y * 50 + 47),
                (x, y),
                cell,
            )
            for i in range(3 - first, 48 + second):
                self.img.set_at((x * 50 + i, y * 50 + 47), self.BLUE)
        if wall & 2:
            wall -= 2
            left, right, coord_l, coord_r, pixels = self.angles[2]
            first = self.draw_angles(
                2,
                left,
                coord_l,
                pixels[0],
                (x * 50 + 47, y * 50 + 47),
                (x, y),
                cell,
            )
            second = self.draw_angles(
                2,
                right,
                coord_r,
                pixels[1],
                (x * 50 + 47, y * 50 + 3),
                (x, y),
                cell,
            )
            for i in range(3 - second, 48 + first):
                self.img.set_at((x * 50 + 47, y * 50 + i), self.BLUE)
        if wall & 1:
            left, right, coord_l, coord_r, pixels = self.angles[1]
            first = self.draw_angles(
                1,
                left,
                coord_l,
                pixels[0],
                (x * 50 + 47, y * 50 + 3),
                (x, y),
                cell,
            )
            second = self.draw_angles(
                1,
                right,
                coord_r,
                pixels[1],
                (x * 50 + 3, y * 50 + 3),
                (x, y),
                cell,
            )
            for i in range(3 - second, 48 + first):
                self.img.set_at((x * 50 + i, y * 50 + 3), self.BLUE)

    def draw_angles(
        self,
        wall: int,
        side: int,
        coord_side: Point,
        pixels: SideCorners,
        coordinates: Point,
        cell_coord: Point,
        cell: int,
    ) -> int:
        x, y = coordinates
        v_x, v_y = coord_side
        side_x, side_y = cell_coord[0] + v_x, cell_coord[1] + v_y
        if cell & side:
            for corner_x, corner_y in pixels[0]:
                new_x, new_y = x + corner_x - v_x * 3, y + corner_y - v_y * 3
                self.img.set_at((new_x, new_y), self.BLUE)
            return -3
        elif not (0 <= side_y <= 15 and 0 <= side_x <= 15):
            return 3
        elif self.maze[side_y][side_x] & wall:
            return 3
        else:
            for corner_x, corner_y in pixels[1]:
                new_x, new_y = x + corner_x, y + corner_y
                self.img.set_at((new_x, new_y), self.BLUE)
        return 0
