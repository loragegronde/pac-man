from src.assets import Assets
from src.visual.maze import Maze
from src.visual.player import Player
import pygame


class GameMode:
    def __init__(self, window: pygame.Surface, assets: Assets) -> None:
        self.maze_pos = (300, 25)
        self.window = window
        self.assets = assets
        self.maze = Maze()
        self.maze.create_maze(pygame.Surface((750, 750)))
        self.player = Player(
            self.maze, self.assets.get_mobs(), window, self.maze_pos
        )

    def refresh_frame(self, dt: float) -> None:
        _ = self.window.blit(self.maze.img, self.maze_pos)
        self.player.update_pos(dt)

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
