# from src.visual.game import GameMode
from src.assets import Assets
import pygame


class LevelHandler:
    def __init__(
        self, window: pygame.Surface, assets: Assets, nb_pacgum: int = 500
    ) -> None:
        self.maze_pos = (300, 25)
        self.window = window
        self.assets = assets
