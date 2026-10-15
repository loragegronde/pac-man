from typing import TypeAlias

from mazegenerator import MazeGenerator
import pygame

Point: TypeAlias = tuple[int, int]
Color: TypeAlias = tuple[int, int, int]
CornerTriple: TypeAlias = tuple[Point, Point, Point]
SideCorners: TypeAlias = tuple[CornerTriple, CornerTriple]
WallAngles: TypeAlias = tuple[SideCorners, SideCorners]
AngleEntry: TypeAlias = tuple[int, int, Point, Point, WallAngles]


class Maze:
    """Handle visual representation of the maze"""

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
    WALL_SIZE: int = 50
    ANGLE_SIZE: int = 3

    def __init__(self, size: Point, seed: int | None) -> None:
        """Initialize maze and maze's image"""
        self.size: Point = size
        self.maze: list[list[int]] = (
            MazeGenerator(size, seed=seed).maze
            if seed
            else MazeGenerator(size).maze
        )
        self.forty_two: set[Point] = {
            (i, j)
            for i in range(len(self.maze[0]))
            for j in range(len(self.maze))
            if self.maze[j][i] == 15
        }
        self.maze_img: pygame.Surface = pygame.Surface((1, 1))
        self.img: pygame.Surface = pygame.Surface((1, 1))
        self.define_angles()

    def define_angles(self) -> None:
        """Needed information to draw each angles rounded"""
        self.angles: dict[int, AngleEntry] = {
            8: (1, 4, (0, -1), (0, 1), self.ANGLES[8]),
            4: (8, 2, (-1, 0), (1, 0), self.ANGLES[4]),
            2: (4, 1, (0, 1), (0, -1), self.ANGLES[2]),
            1: (2, 8, (1, 0), (-1, 0), self.ANGLES[1]),
        }

    def modify_42(self, i: int, j: int) -> None:
        """Temporarily modify 42 for visual representation"""
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
        """Draw all cells of the maze and maze's border

        Args:
            img: image to draw the maze on
        """
        self.maze_img = img
        for cell in self.forty_two:
            self.modify_42(*cell)
        for j in range(len(self.maze)):
            for i in range(len(self.maze[j])):
                self.draw_cell(self.maze[j][i], (i, j))
        for cell in self.forty_two:
            i, j = cell
            self.maze[j][i] = 15
        self.draw_border()

    def draw_cell(self, wall: int, coordinates: Point) -> None:
        """Draw each walls of a cell if there is a wall

        Args:
            wall: hexa value of the cell which determine walls
            coordinates: coordinates of the current cell
        """
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
                (
                    x * self.WALL_SIZE + self.ANGLE_SIZE,
                    y * self.WALL_SIZE + self.ANGLE_SIZE,
                ),
                (x, y),
                cell,
            )
            second = self.draw_angles(
                8,
                right,
                coord_r,
                pixels[1],
                (
                    x * self.WALL_SIZE + self.ANGLE_SIZE,
                    y * self.WALL_SIZE + self.WALL_SIZE - self.ANGLE_SIZE,
                ),
                (x, y),
                cell,
            )
            for i in range(3 - first, 48 + second):
                self.maze_img.set_at(
                    (
                        x * self.WALL_SIZE + self.ANGLE_SIZE,
                        y * self.WALL_SIZE + i,
                    ),
                    self.BLUE,
                )
        if wall & 4:
            wall -= 4
            left, right, coord_l, coord_r, pixels = self.angles[4]
            first = self.draw_angles(
                4,
                left,
                coord_l,
                pixels[0],
                (
                    x * self.WALL_SIZE + self.ANGLE_SIZE,
                    y * self.WALL_SIZE + self.WALL_SIZE - self.ANGLE_SIZE,
                ),
                (x, y),
                cell,
            )
            second = self.draw_angles(
                4,
                right,
                coord_r,
                pixels[1],
                (
                    x * self.WALL_SIZE + self.WALL_SIZE - self.ANGLE_SIZE,
                    y * self.WALL_SIZE + self.WALL_SIZE - self.ANGLE_SIZE,
                ),
                (x, y),
                cell,
            )
            for i in range(3 - first, 48 + second):
                self.maze_img.set_at(
                    (
                        x * self.WALL_SIZE + i,
                        y * self.WALL_SIZE + self.WALL_SIZE - self.ANGLE_SIZE,
                    ),
                    self.BLUE,
                )
        if wall & 2:
            wall -= 2
            left, right, coord_l, coord_r, pixels = self.angles[2]
            first = self.draw_angles(
                2,
                left,
                coord_l,
                pixels[0],
                (
                    x * self.WALL_SIZE + self.WALL_SIZE - self.ANGLE_SIZE,
                    y * self.WALL_SIZE + self.WALL_SIZE - self.ANGLE_SIZE,
                ),
                (x, y),
                cell,
            )
            second = self.draw_angles(
                2,
                right,
                coord_r,
                pixels[1],
                (
                    x * self.WALL_SIZE + self.WALL_SIZE - self.ANGLE_SIZE,
                    y * self.WALL_SIZE + self.ANGLE_SIZE,
                ),
                (x, y),
                cell,
            )
            for i in range(3 - second, 48 + first):
                self.maze_img.set_at(
                    (
                        x * self.WALL_SIZE + self.WALL_SIZE - self.ANGLE_SIZE,
                        y * self.WALL_SIZE + i,
                    ),
                    self.BLUE,
                )
        if wall & 1:
            left, right, coord_l, coord_r, pixels = self.angles[1]
            first = self.draw_angles(
                1,
                left,
                coord_l,
                pixels[0],
                (
                    x * self.WALL_SIZE + self.WALL_SIZE - self.ANGLE_SIZE,
                    y * self.WALL_SIZE + self.ANGLE_SIZE,
                ),
                (x, y),
                cell,
            )
            second = self.draw_angles(
                1,
                right,
                coord_r,
                pixels[1],
                (
                    x * self.WALL_SIZE + self.ANGLE_SIZE,
                    y * self.WALL_SIZE + self.ANGLE_SIZE,
                ),
                (x, y),
                cell,
            )
            for i in range(3 - second, 48 + first):
                self.maze_img.set_at(
                    (
                        x * self.WALL_SIZE + i,
                        y * self.WALL_SIZE + self.ANGLE_SIZE,
                    ),
                    self.BLUE,
                )

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
        """Draw either inside angle, outside angle or full wall
        depending of cell state and neighbor cells

        Args:
            wall: current wall's angles we are drawing
            side: value of the side wall
            coord_side: vector of the neighbor cell
            pixels: pixels possible of the angles to draw
            coordinates: visual coordinate of the cell
            cell_coord: maze coordinates of the current cell
            cell: values of all walls in the cells

        Returns:
            Value of the pixels that are needed to draw if a full wall is draw
        """
        x, y = coordinates
        v_x, v_y = coord_side
        side_x, side_y = cell_coord[0] + v_x, cell_coord[1] + v_y
        if cell & side:
            for corner_x, corner_y in pixels[0]:
                new_x, new_y = x + corner_x - v_x * 3, y + corner_y - v_y * 3
                self.maze_img.set_at((new_x, new_y), self.BLUE)
            return -self.ANGLE_SIZE
        elif not (0 <= side_y <= 15 and 0 <= side_x <= 15):
            return self.ANGLE_SIZE
        elif self.maze[side_y][side_x] & wall:
            return self.ANGLE_SIZE
        else:
            for corner_x, corner_y in pixels[1]:
                new_x, new_y = x + corner_x, y + corner_y
                self.maze_img.set_at((new_x, new_y), self.BLUE)
        return 0

    def draw_border(self) -> None:
        """Draw maze's limits"""
        x, y = self.size
        x_img = x * self.WALL_SIZE + self.ANGLE_SIZE * 2 + 1
        y_img = y * self.WALL_SIZE + self.ANGLE_SIZE * 2 + 1
        self.img = pygame.Surface((x_img, y_img))
        for i in range(x_img):
            self.img.set_at((i, 0), self.BLUE)
            self.img.set_at((i, y_img - 1), self.BLUE)
        for i in range(y_img):
            self.img.set_at((0, i), self.BLUE)
            self.img.set_at((x_img - 1, i), self.BLUE)
        _ = self.img.blit(self.maze_img, (self.ANGLE_SIZE, self.ANGLE_SIZE))
