from src.assets import Assets
from src.parsing import Config
from src.visual.maze import Maze
from src.visual.player import Player
from src.visual.enemy_handler import EnemyHandler
from src.cheats import Cheats
import pygame
import math


class GameMode:
    def __init__(
        self,
        assets: Assets,
        size: tuple[int, int],
        nb_pacgum: int,
        cheats: Cheats,
    ) -> None:
        self.define_maze_pos(size)
        self.assets = assets
        self.cheats = cheats
        self.maze = Maze(size)
        self.maze.create_maze(pygame.Surface((size[0] * 50, size[1] * 50)))
        self.player = Player(self.maze, self.assets.get_mobs())
        self.ghosts = EnemyHandler(self.assets.get_mobs(), self.maze)
        self.score = 0
        self.define_pacgum_pos(nb_pacgum)
        self.dead = False

    def define_maze_pos(self, size: tuple[int, int]):
        x, y = size
        self.maze_pos = (950 - ((x // 2) * 50), 600 - ((y // 2) * 50))

    def update_frame(self, config: Config):
        self.is_player_dead()
        for _ in range(4):
            x, y = self.player.pos
            self.check_interaction(config, (math.ceil(x), math.ceil(y)))
            self.check_interaction(config, (math.floor(x), math.floor(y)))
            self.player.update_pos(self.cheats.speed_mult)
        if not self.cheats.ghost_freeze:
            self.ghosts.refresh_frame()

    def get_direction(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_LEFT:
            self.player.next_direction = 8
        elif event.key == pygame.K_DOWN:
            self.player.next_direction = 4
        elif event.key == pygame.K_RIGHT:
            self.player.next_direction = 2
        elif event.key == pygame.K_UP:
            self.player.next_direction = 1

    def define_pacgum_pos(self, nb_pacgum: int):
        max_x = len(self.maze.maze[0])
        max_y = len(self.maze.maze)
        available = {
            (x, y)
            for y in range(max_y)
            for x in range(max_x)
            if self.maze.maze[y][x] != 15
        }
        self.super_pacgum = {
            (0, 0),
            (max_x - 1, 0),
            (max_x - 1, max_y - 1),
            (0, max_y - 1),
        }
        available = available.difference(
            self.super_pacgum, {(max_x // 2, max_y // 2)}
        )
        self.pacgums = set()
        i = 0
        while i < nb_pacgum and available:
            self.pacgums.add(available.pop())
            i += 1
        self.pacgums_missing = i + 4

    def check_interaction(self, config: Config, coordinates: tuple[int, int]):
        x, y = coordinates
        direction = self.player.direction
        check = False
        if direction == 1 and y % 50 == 25:
            check = True
        if direction == 2 and (x + 35) % 50 == 25:
            check = True
            x += 35
        if direction == 4 and (y + 35) % 50 == 25:
            check = True
            y += 35
        if direction == 8 and x % 50 == 25:
            check = True
        if check:
            maze_pos = (x // 50, y // 50)
            if maze_pos in self.pacgums:
                self.pacgums.remove(maze_pos)
                self.pacgums_missing -= 1
                self.score += config.points_per_pacgum
            if maze_pos in self.super_pacgum:
                self.super_pacgum.remove(maze_pos)
                self.pacgums_missing -= 1
                self.score += config.points_per_super_pacgum
                for i in range(len(self.ghosts.ghosts)):
                    self.ghosts.ghosts[i].state = 5

    def is_player_dead(self):
        min_x, min_y = self.player.pos
        max_x, max_y = min_x + 35, min_y + 35
        for ghost in self.ghosts.ghosts:
            ghost_min_x, ghost_min_y = ghost.pos
            ghost_max_x, ghost_max_y = ghost_min_x + 35, ghost_min_y + 35
            if (
                min_x <= ghost_min_x <= max_x and min_y <= ghost_min_y <= max_y
            ) or (
                min_x <= ghost_max_x <= max_x and min_y <= ghost_max_y <= max_y
            ):
                if ghost.state > 0:
                    ghost.state = 0
                elif not self.cheats.invincibility:
                    self.dead = True

    # def reset(self) -> None:
    #     self.score = 0
    #     self.lives = self.config.lives
    #     self.level = 1
    #     self.time_left = float(self.config.level_max_time)
    #     self.nb_pacgum = self.config.pacgum
    #     self.define_pacgum_pos()
    #     self.dead = False
    #     self.dt = 0.0
    #     self.frame = -1
    #     self.hud.reset()
    #     self.player.define_start_pos()
    #     for ghost in self.ghosts.ghosts:
    #         ghost.define_pos()

    # def draw_border(self):
    #     img_x, img_y = self.maze_pos
    #     for x in range(756):
    #         self.window.set_at((x + img_x - 3, 0 + img_y - 3),
    #         self.maze.BLUE)
    #         self.window.set_at(
    #             (x + img_x - 3, 755 + img_y - 3), self.maze.BLUE
    #         )
    #     for y in range(756):
    #         self.window.set_at((0 + img_x - 3, y + img_y - 3),
    #         self.maze.BLUE)
    #         self.window.set_at(
    #             (755 + img_x - 3, y + img_y - 3), self.maze.BLUE
    #         )
