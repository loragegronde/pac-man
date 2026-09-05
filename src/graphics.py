import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import time


class Graphics:
    def __init__(self, width: int, height: int):
        _ = pygame.init()
        pygame.display.set_caption("pac-man")
        self.screen: pygame.Surface = pygame.display.set_mode((width, height))
        self.running: bool = False

    def run(self) -> None:
        last = time.monotonic()
        img = pygame.image.load("assets/sprites.png").convert_alpha()

        def crop(
            sheet: pygame.Surface, x: int, y: int, w: int, h: int
        ) -> pygame.Surface:
            img = pygame.Surface((w, h), pygame.SRCALPHA)
            _ = img.blit(sheet, (0, 0), (x, y, w, h))
            return img

        blinky_r1: pygame.Surface = crop(img, 651, 4, 35, 35)
        blinky_r2: pygame.Surface = crop(img, 651, 54, 35, 35)
        blinky_d1: pygame.Surface = crop(img, 651, 104, 35, 35)
        blinky_d2: pygame.Surface = crop(img, 651, 154, 35, 35)
        blinky_l1: pygame.Surface = crop(img, 651, 204, 35, 35)
        blinky_l2: pygame.Surface = crop(img, 651, 254, 35, 35)
        blinky_u1: pygame.Surface = crop(img, 651, 304, 35, 35)
        blinky_u2: pygame.Surface = crop(img, 651, 354, 35, 35)

        blinky = {
            "right": [blinky_r1, blinky_r2],
            "down": [blinky_d1, blinky_d2],
            "left": [blinky_l1, blinky_l2],
            "up": [blinky_u1, blinky_u2],
        }

        pinky_r1: pygame.Surface = crop(img, 701, 4, 35, 35)
        pinky_r2: pygame.Surface = crop(img, 701, 54, 35, 35)
        pinky_d1: pygame.Surface = crop(img, 701, 104, 35, 35)
        pinky_d2: pygame.Surface = crop(img, 701, 154, 35, 35)
        pinky_l1: pygame.Surface = crop(img, 701, 204, 35, 35)
        pinky_l2: pygame.Surface = crop(img, 701, 254, 35, 35)
        pinky_u1: pygame.Surface = crop(img, 701, 304, 35, 35)
        pinky_u2: pygame.Surface = crop(img, 701, 354, 35, 35)

        pinky = {
            "right": [pinky_r1, pinky_r2],
            "down": [pinky_d1, pinky_d2],
            "left": [pinky_l1, pinky_l2],
            "up": [pinky_u1, pinky_u2],
        }

        inky_r1: pygame.Surface = crop(img, 751, 4, 35, 35)
        inky_r2: pygame.Surface = crop(img, 751, 54, 35, 35)
        inky_d1: pygame.Surface = crop(img, 751, 104, 35, 35)
        inky_d2: pygame.Surface = crop(img, 751, 154, 35, 35)
        inky_l1: pygame.Surface = crop(img, 751, 204, 35, 35)
        inky_l2: pygame.Surface = crop(img, 751, 254, 35, 35)
        inky_u1: pygame.Surface = crop(img, 751, 304, 35, 35)
        inky_u2: pygame.Surface = crop(img, 751, 354, 35, 35)

        inky = {
            "right": [inky_r1, inky_r2],
            "down": [inky_d1, inky_d2],
            "left": [inky_l1, inky_l2],
            "up": [inky_u1, inky_u2],
        }

        clyde_r1: pygame.Surface = crop(img, 801, 4, 35, 35)
        clyde_r2: pygame.Surface = crop(img, 801, 54, 35, 35)
        clyde_d1: pygame.Surface = crop(img, 801, 104, 35, 35)
        clyde_d2: pygame.Surface = crop(img, 801, 154, 35, 35)
        clyde_l1: pygame.Surface = crop(img, 801, 204, 35, 35)
        clyde_l2: pygame.Surface = crop(img, 801, 254, 35, 35)
        clyde_u1: pygame.Surface = crop(img, 801, 304, 35, 35)
        clyde_u2: pygame.Surface = crop(img, 801, 354, 35, 35)

        clyde = {
            "right": [clyde_r1, clyde_r2],
            "down": [clyde_d1, clyde_d2],
            "left": [clyde_l1, clyde_l2],
            "up": [clyde_u1, clyde_u2],
        }

        pac_man_r1: pygame.Surface = crop(img, 851, 4, 35, 35)
        pac_man_r2: pygame.Surface = crop(img, 851, 54, 35, 35)
        pac_man_r3: pygame.Surface = crop(img, 851, 104, 35, 35)
        pac_man_d1: pygame.Surface = crop(img, 851, 154, 35, 35)
        pac_man_d2: pygame.Surface = crop(img, 851, 204, 35, 35)
        pac_man_d3: pygame.Surface = crop(img, 851, 254, 35, 35)
        pac_man_l1: pygame.Surface = crop(img, 851, 304, 35, 35)
        pac_man_l2: pygame.Surface = crop(img, 851, 354, 35, 35)
        pac_man_l3: pygame.Surface = crop(img, 851, 404, 35, 35)
        pac_man_u1: pygame.Surface = crop(img, 851, 454, 35, 35)
        pac_man_u2: pygame.Surface = crop(img, 851, 504, 35, 35)
        pac_man_u3: pygame.Surface = crop(img, 851, 554, 35, 35)

        pac = {
            "right": [pac_man_r1, pac_man_r2, pac_man_r3],
            "down": [pac_man_d1, pac_man_d2, pac_man_d3],
            "left": [pac_man_l1, pac_man_l2, pac_man_l3],
            "up": [pac_man_u1, pac_man_u2, pac_man_u3],
        }

        direction = "right"
        FRAME_DURATION = 0.15
        anim_time = 0.0
        frame_index = 0

        self.running = True
        while self.running:
            now = time.monotonic()
            dt = now - last
            last = now

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        direction = "right"
                        frame_index = 0
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        direction = "left"
                        frame_index = 0
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        direction = "down"
                        frame_index = 0
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        direction = "up"
                        frame_index = 0

            anim_time += dt
            if anim_time >= FRAME_DURATION:
                anim_time -= FRAME_DURATION
                frame_index += 1

            _ = self.screen.fill((0, 0, 0))

            blinky_frames = blinky[direction]
            pinky_frames = pinky[direction]
            inky_frames = inky[direction]
            clyde_frames = clyde[direction]
            pac_frames = pac[direction]

            _ = self.screen.blit(
                blinky_frames[frame_index % len(blinky_frames)], (1, 1)
            )
            _ = self.screen.blit(
                pinky_frames[frame_index % len(pinky_frames)], (50, 1)
            )
            _ = self.screen.blit(
                inky_frames[frame_index % len(inky_frames)], (100, 1)
            )
            _ = self.screen.blit(
                clyde_frames[frame_index % len(clyde_frames)], (150, 1)
            )
            _ = self.screen.blit(
                pac_frames[frame_index % len(pac_frames)], (200, 1)
            )

            pygame.display.flip()
        pygame.quit()
