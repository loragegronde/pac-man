import pygame


class AssetHandler:
    def crop(
        self, sheet: pygame.Surface, x: int, y: int, w: int, h: int
    ) -> pygame.Surface:
        img = pygame.Surface((w, h), pygame.SRCALPHA)
        _ = img.blit(sheet, (0, 0), (x, y, w, h))
        return img

    def get_mobs(self, filename: str):
        img = pygame.image.load(filename).convert_alpha()

        blinky_r1: pygame.Surface = self.crop(img, 651, 4, 35, 35)
        blinky_r2: pygame.Surface = self.crop(img, 651, 54, 35, 35)
        blinky_d1: pygame.Surface = self.crop(img, 651, 104, 35, 35)
        blinky_d2: pygame.Surface = self.crop(img, 651, 154, 35, 35)
        blinky_l1: pygame.Surface = self.crop(img, 651, 204, 35, 35)
        blinky_l2: pygame.Surface = self.crop(img, 651, 254, 35, 35)
        blinky_u1: pygame.Surface = self.crop(img, 651, 304, 35, 35)
        blinky_u2: pygame.Surface = self.crop(img, 651, 354, 35, 35)

        self.blinky = {
            "E": [blinky_r1, blinky_r2],
            "S": [blinky_d1, blinky_d2],
            "W": [blinky_l1, blinky_l2],
            "N": [blinky_u1, blinky_u2],
        }

        pinky_r1: pygame.Surface = self.crop(img, 701, 4, 35, 35)
        pinky_r2: pygame.Surface = self.crop(img, 701, 54, 35, 35)
        pinky_d1: pygame.Surface = self.crop(img, 701, 104, 35, 35)
        pinky_d2: pygame.Surface = self.crop(img, 701, 154, 35, 35)
        pinky_l1: pygame.Surface = self.crop(img, 701, 204, 35, 35)
        pinky_l2: pygame.Surface = self.crop(img, 701, 254, 35, 35)
        pinky_u1: pygame.Surface = self.crop(img, 701, 304, 35, 35)
        pinky_u2: pygame.Surface = self.crop(img, 701, 354, 35, 35)

        self.pinky = {
            "E": [pinky_r1, pinky_r2],
            "S": [pinky_d1, pinky_d2],
            "W": [pinky_l1, pinky_l2],
            "N": [pinky_u1, pinky_u2],
        }

        inky_r1: pygame.Surface = self.crop(img, 751, 4, 35, 35)
        inky_r2: pygame.Surface = self.crop(img, 751, 54, 35, 35)
        inky_d1: pygame.Surface = self.crop(img, 751, 104, 35, 35)
        inky_d2: pygame.Surface = self.crop(img, 751, 154, 35, 35)
        inky_l1: pygame.Surface = self.crop(img, 751, 204, 35, 35)
        inky_l2: pygame.Surface = self.crop(img, 751, 254, 35, 35)
        inky_u1: pygame.Surface = self.crop(img, 751, 304, 35, 35)
        inky_u2: pygame.Surface = self.crop(img, 751, 354, 35, 35)

        self.inky = {
            "E": [inky_r1, inky_r2],
            "S": [inky_d1, inky_d2],
            "W": [inky_l1, inky_l2],
            "N": [inky_u1, inky_u2],
        }

        clyde_r1: pygame.Surface = self.crop(img, 801, 4, 35, 35)
        clyde_r2: pygame.Surface = self.crop(img, 801, 54, 35, 35)
        clyde_d1: pygame.Surface = self.crop(img, 801, 104, 35, 35)
        clyde_d2: pygame.Surface = self.crop(img, 801, 154, 35, 35)
        clyde_l1: pygame.Surface = self.crop(img, 801, 204, 35, 35)
        clyde_l2: pygame.Surface = self.crop(img, 801, 254, 35, 35)
        clyde_u1: pygame.Surface = self.crop(img, 801, 304, 35, 35)
        clyde_u2: pygame.Surface = self.crop(img, 801, 354, 35, 35)

        self.clyde = {
            "E": [clyde_r1, clyde_r2],
            "S": [clyde_d1, clyde_d2],
            "W": [clyde_l1, clyde_l2],
            "N": [clyde_u1, clyde_u2],
        }

        pac_man_r1: pygame.Surface = self.crop(img, 851, 4, 35, 35)
        pac_man_r2: pygame.Surface = self.crop(img, 851, 54, 35, 35)
        pac_man_r3: pygame.Surface = self.crop(img, 851, 104, 35, 35)
        pac_man_d1: pygame.Surface = self.crop(img, 851, 154, 35, 35)
        pac_man_d2: pygame.Surface = self.crop(img, 851, 204, 35, 35)
        pac_man_d3: pygame.Surface = self.crop(img, 851, 254, 35, 35)
        pac_man_l1: pygame.Surface = self.crop(img, 851, 304, 35, 35)
        pac_man_l2: pygame.Surface = self.crop(img, 851, 354, 35, 35)
        pac_man_l3: pygame.Surface = self.crop(img, 851, 404, 35, 35)
        pac_man_u1: pygame.Surface = self.crop(img, 851, 454, 35, 35)
        pac_man_u2: pygame.Surface = self.crop(img, 851, 504, 35, 35)
        pac_man_u3: pygame.Surface = self.crop(img, 851, 554, 35, 35)

        self.pac = {
            "E": [pac_man_r1, pac_man_r2, pac_man_r3],
            "S": [pac_man_d1, pac_man_d2, pac_man_d3],
            "W": [pac_man_l1, pac_man_l2, pac_man_l3],
            "N": [pac_man_u1, pac_man_u2, pac_man_u3],
        }

        self.pac_man_spawn: list[pygame.Surface] = [
            self.crop(img, 351, 4 + (i * 50), 35, 35) for i in range(11)
        ]
