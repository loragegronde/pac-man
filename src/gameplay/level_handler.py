from src.utils.assets import Assets
from src.parsing.parsing import Config
from src.gameplay.hud import Hud
from src.gameplay.game import GameMode
from src.scenes.cheats import Cheats
from dataclasses import dataclass
from typing import Any, ClassVar
import pygame


@dataclass
class GameData:
    """Data that are needed for game's creation"""

    assets: Assets
    nb_pacgums: int
    cheats: Cheats
    size: ClassVar[tuple[int, int]] = (15, 15)
    ghost_speed: ClassVar[list[float]] = [
        speed / 100 for speed in range(75, 125, 5)
    ]

    def get_data(self, i: int) -> list[Any]:
        """Return game's data depending of level difficulty"""
        return [
            self.assets,
            self.size,
            self.nb_pacgums,
            self.cheats,
            self.ghost_speed[i],
            1 if not i else None,
        ]


class LevelHandler:
    """Pipeline of all games and handle visualisation of game"""

    def __init__(
        self,
        window: pygame.Surface,
        assets: Assets,
        config: Config,
        cheats: Cheats,
    ) -> None:
        """Initialize 10 levels pipeline and default frames configuration.

        Args:
            window: current window to put on assets
            assets: visual representation of player and ghosts
            config: game's default state and configuration
            cheats: instance which tells if cheats are actives
        """
        self.window: pygame.Surface = window
        self.assets: Assets = assets
        self.config: Config = config
        self.cheats: Cheats = cheats
        self.level: int = 0
        self.nb_pacgum: int = config.pacgum
        self.lives: int = config.lives
        self.time_left: float = float(config.level_max_time)
        self.data = GameData(
            assets=assets, nb_pacgums=self.nb_pacgum, cheats=cheats
        )
        self.mazes: list[GameMode] = [
            GameMode(*self.data.get_data(i)) for i in range(10)
        ]
        self.hud: Hud = Hud(window, assets)
        self.dead: bool = False
        self.dt: float = 0.0
        self.dead_frame: int = -1
        self.frame: int = 0
        self.score: int = 0
        self.speed: float = 60 / self.config.fps

    def reset(self) -> None:
        """Reset to default configuration"""
        self.level = 0
        self.nb_pacgum = self.config.pacgum
        self.lives = self.config.lives
        self.time_left = float(self.config.level_max_time)
        self.dead = False
        self.dt = 0.0
        self.dead_frame = -1
        self.frame = 0
        self.score = 0
        self.mazes = [
            GameMode(*self.data.get_data(i)) for i in range(10)
        ]

    def refresh_frame(self, dt: float) -> None:
        """Update all positions of assets in the game.
        Then draw visual depending on game and assets state.

        Args:
            dt: time between current frame and last frame
        """
        self.dt += dt
        self.score = sum(m.score for m in self.mazes)
        if self.cheats.always_chase:
            for ghost in self.mazes[self.level].ghosts.ghosts:
                ghost.state = 5
        if self.mazes[self.level].pacgums_missing == 0:
            self.level += 1
            self.time_left = float(self.config.level_max_time)
            if self.level > 9:
                return
        game = self.mazes[self.level]
        if self.cheats.one_pacgum and len(game.pacgums) > 1:
            game.pacgums = {game.pacgums.pop()}
            game.super_pacgum = set()
            game.pacgums_missing = len(game.pacgums)
        maze_x, maze_y = game.maze_pos
        maze_x -= game.maze.ANGLE_SIZE
        maze_y -= game.maze.ANGLE_SIZE
        _ = self.window.blit(game.maze.img, (maze_x, maze_y))
        self.place_pacgum(game)
        if game.dead:
            self.death_animation()
            self.hud.render(
                self.score, self.lives, self.level, self.time_left, dt
            )
            return
        game.update_frame(self.config, dt, self.speed)
        self.time_left = self.time_left - dt
        self.draw_ghosts(dt)
        self.draw_player()
        self.hud.render(self.score, self.lives, self.level, self.time_left, dt)
        if self.dt > 0.14:
            self.frame += 1
            self.dt -= 0.14

    def death_animation(self) -> None:
        """Draw death animation of the player"""
        dead_anim = self.assets.get_mobs().pac_man_spawn
        if self.dead_frame == -1:
            time = 1.0
        else:
            time = 0.1
        if self.dt > time:
            self.dead_frame += 1
            self.dt = 0
        if self.dead_frame == len(dead_anim):
            self.mazes[self.level].dead = False
            self.dead_frame = -1
            self.lives = max(0, self.lives - 1)
            self.mazes[self.level].player.define_start_pos()
            for ghost in self.mazes[self.level].ghosts.ghosts:
                ghost.define_pos()
                ghost.speed = max(0.5, ghost.speed - 0.05)
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

    def place_pacgum(self, game: GameMode) -> None:
        """Draw all pacgums remaining on the maze"""
        maze_x, maze_y = game.maze_pos
        for pacgum in game.pacgums:
            x, y = pacgum
            _ = self.window.blit(
                self.assets.pac_gum,
                (
                    x * self.mazes[0].maze.WALL_SIZE + 22 + maze_x,
                    y * self.mazes[0].maze.WALL_SIZE + 22 + maze_y,
                ),
            )
        for super_pacgum in game.super_pacgum:
            x, y = super_pacgum
            _ = self.window.blit(
                self.assets.super_pacgum,
                (
                    x * self.mazes[0].maze.WALL_SIZE + 16 + maze_x,
                    y * self.mazes[0].maze.WALL_SIZE + 16 + maze_y,
                ),
            )

    def draw_player(self) -> None:
        """Draw player on his window position"""
        game = (
            self.mazes[self.level]
            if self.level != 10
            else self.mazes[self.level - 1]
        )
        img_x, img_y = game.maze_pos

        p_x, p_y = game.player.pos
        _ = self.window.blit(
            game.player.movement[game.player.direction][self.frame % 3],
            (p_x + img_x, p_y + img_y),
        )

    def draw_ghosts(self, dt: float = 0.0) -> None:
        """Draw all ghosts on position with ghost state"""
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
                asset = ghost.afraid[state][self.frame % 2]
                ghost.state = max(0.0, ghost.state - dt)
            else:
                asset = ghost.assets[ghost.direction][self.frame % 2]
            x, y = ghost.pos
            _ = self.window.blit(asset, (x + img_x, y + img_y))
