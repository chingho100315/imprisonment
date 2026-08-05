import pygame
import sys
import logging
import traceback
import game
from func import *

pygame.init()
pygame.font.init()
pygame.mixer.init()

logging.basicConfig(level=logging.DEBUG,
    format="%(asctime)s\n%(levelname)s\n%(message)s\n", 
    handlers=[
        logging.FileHandler("debug/logging.log")
    ]
)

sys.excepthook = lambda *e: [
    logging.error("\n" + "".join(traceback.format_exception(*e)))
]

class Fps:
    def __init__(self):
        self.image = []
        for a in range(200):
            self.image.append(
                game.font["金陵"].render(
                    f"fps : {a}", 
                    True, 
                    (0, 0, 0)
                )
            )

            surface = pygame.Surface((
                self.image[a].get_width(), 
                self.image[a].get_height()
            ))

            surface.fill(
                (0, 1, 0)
            )

            surface.blit(
                self.image[a], 
                (0, 0)
            )

            surface.set_colorkey(
                (0, 1, 0)
            )

            self.image[a] = surface
            self.rect = self.image[a].get_rect()

    def draw(self):
        surface.image.blit(
            self.image[round(fpstick.now())], 
            self.rect
        )

class Key:
    def __init__(self):
        fontos.load("key : 3784280", fontos.black)
        self.image = fontos.use("key : 3784280")
        self.rect = self.image.get_rect()
        self.rect.y = fps.rect.h

    def draw(self):
        surface.image.blit(
            self.image, 
            self.rect
        )

class Surface:
    def __init__(self):
        self.image = pygame.Surface((key.rect.w, fps.rect.h + fps.rect.h))
        self.image.fill((1, 0, 0))
        self.image.set_colorkey((1, 0, 0))
        self.tick = 0
    def draw(self):
        self.tick += 1

        if self.tick == 20:
            self.tick = 0

            self.image.fill((1, 0, 0))

            fps.draw()
            key.draw()

        game.screen.blit(
            self.image, 
            (0, 0)
        )

fps = Fps()
key = Key()
surface = Surface()

fps.draw()
key.draw()

yes = False