from src.assets import Assets
from src.parsing import Config
from src.visual.hud import Hud
import pygame
from enum import Enum
from src.visual.game import GameMode
from src.cheats import Cheats

data = [(15, 15) for _ in range(10)]
data = data[::-1]


class VisualState(Enum):
    START = "start"
    MAZE = "maze"
    VICTORY = "victory"
    DEFEAT = "defeat"


class LevelHandler:
    def __init__(
        self,
        window: pygame.Surface,
        assets: Assets,
        config: Config,
        cheats: Cheats,
    ) -> None:
        self.window: pygame.Surface = window
        self.assets: Assets = assets
        self.config: Config = config
        self.cheats: Cheats = cheats
        self.level: int = 0
        self.nb_pacgum: int = config.pacgum
        self.lives: int = config.lives
        self.time_left: float = float(config.level_max_time)
        self.mazes: list[GameMode] = [
            GameMode(assets, size, config.pacgum, self.cheats) for size in data
        ]
        self.hud: Hud = Hud(window, assets)
        self.dead: bool = False
        self.dt: float = 0.0
        self.dead_frame: int = -1
        self.frame: int = 0
        self.state: VisualState = VisualState.START
        self.score: int = 0

    def reset(self) -> None:
        self.level = 0
        self.nb_pacgum = self.config.pacgum
        self.lives = self.config.lives
        self.time_left = float(self.config.level_max_time)
        self.mazes = [
            GameMode(self.assets, size, self.config.pacgum, self.cheats)
            for size in data
        ]
        self.dead = False
        self.dt = 0.0
        self.dead_frame = -1
        self.frame = 0
        self.state = VisualState.START
        self.score = 0
        self.hud.reset()

    def refresh_frame(self, dt: float) -> None:
        if self.mazes[self.level].pacgums_missing == 0:
            self.level += 1
            self.time_left = float(self.config.level_max_time)
            if self.level > 9:
                return
        game = self.mazes[self.level]
        if self.cheats.one_pacgum and len(game.pacgums) > 1:
            game.pacgums = {game.pacgums.pop()}
            game.pacgums_missing = len(game.pacgums) + len(game.super_pacgum)
        _ = self.window.blit(game.maze.img, game.maze_pos)
        self.place_pacgum(game)
        if game.dead:
            self.death_animation(dt)
            self.score = sum(m.score for m in self.mazes)
            self.hud.render(
                self.score, self.lives, self.level, self.time_left, dt
            )
            return
        game.update_frame(self.config, dt)
        self.score = sum(m.score for m in self.mazes)
        self.time_left = self.time_left - dt
        self.draw_ghosts(dt)
        self.draw_player()
        self.hud.render(self.score, self.lives, self.level, self.time_left, dt)
        self.frame = self.frame + 1 % self.config.fps

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
        game = (
            self.mazes[self.level]
            if self.level != 10
            else self.mazes[self.level - 1]
        )
        img_x, img_y = game.maze_pos

        p_x, p_y = game.player.pos
        _ = self.window.blit(
            game.player.movement[game.player.direction][self.frame // 5 % 3],
            (p_x + img_x, p_y + img_y),
        )

    def draw_ghosts(self, dt: float = 0.0):
        game = self.mazes[self.level]
        img_x, img_y = game.maze_pos

        for ghost in game.ghosts.ghosts:
            if ghost.dead:
                asset = ghost.dead_assets[ghost.direction]
            elif ghost.state > 0:
                state = (
                    "flash"
                    if ghost.state < 2 and 0 <= ghost.state % 0.4 < 0.2
                    else "normal"
                )
                asset = ghost.afraid[state][self.frame // 5 % 2]
                ghost.state = max(0.0, ghost.state - dt)
            else:
                asset = ghost.assets[ghost.direction][self.frame // 5 % 2]
            x, y = ghost.pos
            _ = self.window.blit(asset, (x + img_x, y + img_y))
