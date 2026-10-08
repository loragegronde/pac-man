from src.assets import Assets
from src.parsing import Config
from src.visual.hud import Hud
import pygame
from enum import Enum
from src.visual.game import GameMode


data = [
    (15, 15) for _ in range(10)
]
data = data[::-1]


class VisualState(Enum):
    START = "start"
    MAZE = "maze"
    VICTORY = "victory"
    DEFEAT = "defeat"


class LevelHandler:
    def __init__(
        self, window: pygame.Surface, assets: Assets, config: Config
    ) -> None:
        self.window = window
        self.assets = assets
        self.config = config
        self.level = 0
        self.nb_pacgum = config.pacgum
        self.lives = config.lives
        self.time_left = float(config.level_max_time)
        self.mazes: list[GameMode] = [
            GameMode(assets, size, config.pacgum) for size in data
        ]
        self.hud = Hud(window, assets)
        self.dead = False
        self.dt: float = 0.0
        self.dead_frame: int = -1
        self.frame: int = 0
        self.state = VisualState.START
        self.score: int = 0

    def refresh_frame(self, dt: float) -> None:
        if self.mazes[self.level].pacgums_missing == 0:
            self.level += 1
        game = self.mazes[self.level]
        _ = self.window.blit(game.maze.img, game.maze_pos)
        self.place_pacgum(game)
        if game.dead:
            self.death_animation(dt)
            self.hud.render(
                self.score, self.lives, self.level, self.time_left, dt
            )
            return
        game.update_frame(self.config)
        self.time_left = self.time_left - dt
        self.draw_ghosts(dt)
        self.draw_player()
        self.hud.render(self.score, self.lives, self.level, self.time_left, dt)
        self.frame = self.frame + 1 % 60

    def death_animation(self, dt: float = 0.0):
        dead_anim = self.assets.get_mobs().pac_man_spawn
        self.dt += dt
        if self.dead_frame == -1:
            time = 1
        else:
            time = 0.1
        if self.dt > time:
            self.dead_frame += 1
            self.dt -= time
        if self.dead_frame == len(dead_anim):
            self.mazes[self.level].dead = False
            self.dead_frame = -1
            self.lives = max(0, self.lives - 1)
            self.mazes[self.level].player.define_start_pos()
            for i in range(len(self.mazes[self.level].ghosts.ghosts)):
                self.mazes[self.level].ghosts.ghosts[i].define_pos()
            return
        if self.dead_frame == -1:
            self.draw_player()
            self.draw_ghosts()
        else:
            x, y = self.mazes[self.level].player.pos
            img_x, img_y = self.mazes[self.level].maze_pos
            _ = self.window.blit(
                dead_anim[self.dead_frame],
                (x + img_x, y + img_y),
            )

    def place_pacgum(self, game: GameMode):
        maze_x, maze_y = game.maze_pos
        for pacgum in game.pacgums:
            x, y = pacgum
            _ = self.window.blit(
                self.assets.pac_gum,
                (x * 50 + 22 + maze_x, y * 50 + 22 + maze_y),
            )
        for super_pacgum in game.super_pacgum:
            x, y = super_pacgum
            _ = self.window.blit(
                self.assets.super_pacgum,
                (x * 50 + 16 + maze_x, y * 50 + 16 + maze_y),
            )

    def draw_player(self):
        game = self.mazes[self.level]
        img_x, img_y = game.maze_pos

        p_x, p_y = game.player.pos
        _ = self.window.blit(
            game.player.movement[game.player.direction][self.frame // 5 % 3],
            (p_x + img_x, p_y + img_y),
        )

    def draw_ghosts(self, dt: float = 0.0):
        game = self.mazes[self.level]
        img_x, img_y = game.maze_pos

        for i, ghost in enumerate(game.ghosts.ghosts):
            if ghost.state > 0:
                if ghost.state < 2 and 0 <= ghost.state % 0.4 < 0.2:
                    state = "flash"
                else:
                    state = "normal"
                asset = ghost.afraid[state][self.frame // 5 % 2]
                game.ghosts.ghosts[i].state -= dt
            else:
                asset = ghost.assets[ghost.direction][self.frame // 5 % 2]
            x, y = ghost.pos
            _ = self.window.blit(
                asset,
                (x + img_x, y + img_y),
            )
