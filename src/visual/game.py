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
        self.assets: Assets = assets
        self.cheats: Cheats = cheats
        self.maze: Maze = Maze(size)
        self.maze.create_maze(pygame.Surface((size[0] * 50, size[1] * 50)))
        self.player: Player = Player(self.maze, self.assets.get_mobs())
        self.ghosts: EnemyHandler = EnemyHandler(
            self.assets.get_mobs(), self.maze
        )
        self.score: int = 0
        self.dt: float = 0.0
        self.ghost_combo: int = 0
        self.eat_freeze: float = 0.0
        self.define_pacgum_pos(nb_pacgum)
        self.dead: bool = False

    def define_maze_pos(self, size: tuple[int, int]):
        x, y = size
        self.maze_pos: tuple[int, int] = (
            950 - ((x // 2) * 50),
            600 - ((y // 2) * 50),
        )

    def update_frame(self, config: Config, dt: float = 0.0):
        if self.eat_freeze > 0:
            self.eat_freeze = max(0.0, self.eat_freeze - dt)
            return
        self.is_player_dead(config)
        self.dt += dt
        if self.dt < 1 / 60:
            return
        for _ in range(4):
            x, y = self.player.pos
            self.check_interaction(config, (math.ceil(x), math.ceil(y)))
            self.check_interaction(config, (math.floor(x), math.floor(y)))
            self.player.update_pos(self.cheats.speed_mult)
        if not self.cheats.ghost_freeze:
            self.ghosts.refresh_frame(
                self.player.maze_pos, self.player.direction
            )

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
        self.super_pacgum: set[tuple[int, int]] = {
            (0, 0),
            (max_x - 1, 0),
            (max_x - 1, max_y - 1),
            (0, max_y - 1),
        }
        available = available.difference(
            self.super_pacgum, {(max_x // 2, max_y // 2)}
        )
        self.pacgums: set[tuple[int, int]] = set()
        i = 0
        while i < nb_pacgum and available:
            self.pacgums.add(available.pop())
            i += 1
        self.pacgums_missing: int = i + 4

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
                self.ghost_combo = 0
                for ghost in self.ghosts.ghosts:
                    if not ghost.dead:
                        ghost.state = 5

    def is_player_dead(self, config: Config) -> None:
        min_x, min_y = self.player.pos
        max_x, max_y = min_x + 35, min_y + 35
        for ghost in self.ghosts.ghosts:
            if ghost.dead:
                continue
            ghost_min_x, ghost_min_y = ghost.pos
            ghost_max_x, ghost_max_y = ghost_min_x + 35, ghost_min_y + 35
            if (
                min_x <= ghost_min_x <= max_x and min_y <= ghost_min_y <= max_y
            ) or (
                min_x <= ghost_max_x <= max_x and min_y <= ghost_max_y <= max_y
            ):
                if ghost.state > 0:
                    self.score += config.points_per_ghost << self.ghost_combo
                    self.ghost_combo += 1
                    ghost.dead = True
                    ghost.state = 0.0
                    ghost.dead_wait = 0
                    mx, my = ghost.maze_pos
                    ghost.pos = (mx * 50 + 7, my * 50 + 7)
                    self.eat_freeze = 1.0
                    return
                if not self.cheats.invincibility:
                    self.dead = True
