from abc import ABC, abstractmethod
from src.visual.blinky import Blinky
from src.assets import Mob


class Enemy(ABC):
    maze_pos: tuple[int, int]
    pos: tuple[int, int]

    def __init__(self, assets, afraid, maze) -> None:
        self.direction: int = 0
        self.assets = assets
        self.afraid = afraid
        self.maze = maze
        self.update_direction()
        self.vector: dict[int, tuple[int, int]] = {
            8: (-1, 0),
            4: (0, 1),
            2: (1, 0),
            1: (0, -1),
        }

    @abstractmethod
    def update_direction(self):
        ...

    def update_pos(self):
        maze_x, maze_y = self.maze_pos
        x, y = self.pos
        if not self.maze.maze[maze_y][maze_x] & self.direction or (
            x % 50 != 7 or y % 50 != 7
        ):
            next_x, next_y = self.vector[self.direction]
        else:
            next_x, next_y = 0, 0
        new_x, new_y = (x + next_x, y + next_y)
        if new_x % 50 == 7 and new_y % 50 == 7:
            self.maze_pos = (new_x // 50, new_y // 50)
        self.pos = (new_x, new_y)


class EnemyHandler():
    def __init__(self, img_pos, window, assets: Mob, maze) -> None:
        self.img_pos = img_pos
        self.window = window
        self.create_ghosts(assets, maze)
        self.dt: float = 0

    def create_ghosts(self, assets: Mob, maze):
        self.ghosts: list[Enemy] = [
            Blinky(assets.blinky, None, maze)
        ]

    def draw_enemy(self) -> None:
        return
        img_x, img_y = self.img_pos
        # _ = self.window.blit(
        #     self.movement[self.direction][self.frame % 3],
        #     (new_x + img_x, new_y + img_y),
        # )
        # if self.dt > 0.2:
        #     if self.frame >= 2:
        #         self.mov = -1
        #     if self.frame <= 0:
        #         self.mov = 1
        #     self.frame = self.frame + self.mov % 3
        #     self.dt -= 0.2

    def draw_ghosts(self):
        ...

    def refresh_frame(self):
        if self.dt > 0.2:
            self.dt -= 0.2
