from src.assets import Assets
from src.visual.maze import Maze
from src.visual.player import Player
from src.visual.enemy_handler import EnemyHandler
import pygame


class GameMode:
    def __init__(self, window: pygame.Surface, assets: Assets,
                 nb_pacgum: int = 500) -> None:
        self.maze_pos = (300, 25)
        self.window = window
        self.assets = assets
        self.maze = Maze()
        self.maze.create_maze(pygame.Surface((750, 750)))
        self.player = Player(
            self.maze, self.assets.get_mobs(), window, self.maze_pos
        )
        self.ghosts = EnemyHandler(
            self.maze_pos, self.window, self.assets.get_mobs(), self.maze
        )
        self.nb_pacgum = nb_pacgum
        self.define_pacgum_pos()

    def refresh_frame(self, dt: float) -> None:
        _ = self.window.blit(self.maze.img, self.maze_pos)
        if self.is_player_dead():
            self.player.define_start_pos()
            for i in range(len(self.ghosts.ghosts)):
                self.ghosts.ghosts[i].define_pos()
        self.place_pacgum()
        for i in range(4):
            self.check_interaction()
            self.player.update_pos(dt)
        self.ghosts.refresh_frame(dt)

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

    def draw_border(self):
        img_x, img_y = self.maze_pos
        for x in range(756):
            self.window.set_at((x + img_x - 3, 0 + img_y - 3),
                               self.maze.BLUE)
            self.window.set_at((x + img_x - 3, 755 + img_y - 3),
                               self.maze.BLUE)
        for y in range(756):
            self.window.set_at((0 + img_x - 3, y + img_y - 3),
                               self.maze.BLUE)
            self.window.set_at((755 + img_x - 3, y + img_y - 3),
                               self.maze.BLUE)

    def define_pacgum_pos(self):
        max_x = len(self.maze.maze[0])
        max_y = len(self.maze.maze)
        available = {(x, y) for y in range(max_y)
                     for x in range(max_x)
                     if self.maze.maze[y][x] != 15}
        self.super_pacgum = {
            (0, 0), (max_x - 1, 0),
            (max_x - 1, max_y - 1),
            (0, max_y - 1)
        }
        available = available.difference(
            self.super_pacgum, {(max_x // 2, max_y // 2)}
        )
        self.pacgums = set()
        i = 0
        while i < self.nb_pacgum and available:
            self.pacgums.add(available.pop())
            i += 1
        self.pacgums_missing = i

    def place_pacgum(self):
        maze_x, maze_y = self.maze_pos
        for pacgum in self.pacgums:
            x, y = pacgum
            _ = self.window.blit(self.assets.pac_gum, (x * 50 + 22 + maze_x,
                                                       y * 50 + 22 + maze_y))
        for super_pacgum in self.super_pacgum:
            x, y = super_pacgum
            _ = self.window.blit(
                self.assets.super_pacgum, (x * 50 + 16 + maze_x,
                                           y * 50 + 16 + maze_y)
            )

    def check_interaction(self):
        x, y = self.player.pos
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
            if maze_pos in self.super_pacgum:
                self.super_pacgum.remove(maze_pos)

    def is_player_dead(self):
        min_x, min_y = self.player.pos
        max_x, max_y = min_x + 35, min_y + 35
        for ghost in self.ghosts.ghosts:
            x, y = ghost.pos
            if min_x <= x <= max_x and min_y <= y <= max_y:
                return True
        return False
