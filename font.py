from pathlib import Path

import pygame

ASSETS = Path("assets")
FONT_PATH = Path("pacman_font.ttf")
LABEL_COLOR = (200, 200, 210)


def generate_hud_sprites() -> None:
    _ = pygame.init()
    _ = pygame.display.set_mode((1, 1))
    font = pygame.font.Font(str(FONT_PATH), 42)
    ASSETS.mkdir(exist_ok=True)

    for label in ("SCORE", "LIVES", "LEVEL", "TIME"):
        surf = font.render(label, True, LABEL_COLOR)
        _ = pygame.image.save(surf, str(ASSETS / f"hud_{label.lower()}.png"))

    pygame.quit()


if __name__ == "__main__":
    generate_hud_sprites()
