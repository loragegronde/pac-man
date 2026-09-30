from src.visual.get_assets import AssetHandler
from src.visual.maze import Maze
from src.visual.player import Player
import pygame


class GameMode():
    def __init__(self, window) -> None:
        self.maze_pos = (300, 25)
        self.window = window
        self.assets = AssetHandler()
        self.assets.get_mobs("assets/sprites.png")
        self.maze = Maze()
        self.maze.create_maze(pygame.Surface((750, 750)))
        self.draw_border()
        self.player = Player(self.maze, self.assets, window, self.maze_pos)

    def refresh_frame(self):
        self.window.blit(self.maze.img, self.maze_pos)
        self.player.update_pos()

    def get_direction(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.player.next_direction = 8
            if event.key == pygame.K_DOWN:
                self.player.next_direction = 4
            if event.key == pygame.K_RIGHT:
                self.player.next_direction = 2
            if event.key == pygame.K_UP:
                self.player.next_direction = 1

    def draw_border(self):
        img_x, img_y = self.maze_pos
        for x in range(756):
            self.window.set_at((x + img_x - 3, 0 + img_y - 3), self.maze.BLUE)
            self.window.set_at((x + img_x - 3, 755 + img_y - 3), self.maze.BLUE)
        for y in range(756):
            self.window.set_at((0 + img_x - 3, y + img_y - 3), self.maze.BLUE)
            self.window.set_at((755 + img_x - 3, y + img_y - 3), self.maze.BLUE)
