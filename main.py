import pygame
import sys
import traceback
import functools
import contextlib
import cProfile
import logging
import inspect
import game
from datetime import datetime
from random import uniform, choices
from pickle import load, dump
from os.path import isfile

pygame.init()
pygame.mixer.init()
pygame.font.init()

logging.basicConfig(level=logging.DEBUG,
    format="%(asctime)s\n%(levelname)s\n%(message)s\n", 
    handlers=[
        logging.FileHandler("debug/logging.log")
    ]
)

sys.excepthook = lambda *e: [
    logging.error("\n" + "".join(traceback.format_exception(*e)))
]

start = pygame.transform.scale(
    pygame.image.load("image/loading2.jpg"), 
    (game.screen.get_width(), game.screen.get_height())
)

game.screen.blit(
    start, 
    (0, 0)
)

start = pygame.transform.scale(
    pygame.image.load(f"image/version/{game.__version__}/image.png"), 
    (game.screen.get_width() * 0.3, game.screen.get_height() * 0.3)
)

start.set_alpha(164)

game.screen.blit(
    start, 
    (0, 0 + game.font["金陵"].render(f"version : {game.__version__}", True, (255, 255, 255)).get_height())
)

start = game.font["金陵"].render(
    f"version : {game.__version__}", 
    True, 
    (255, 255, 255)
)

game.screen.blit(
    start, 
    (0, 0)
)

pygame.display.update()

pygame.mixer.music.load("music/nop.mp3")
pygame.mixer.music.play(-1)

import debugs
from init import *
from func import *
from mainloop.loop.backing import backing
from mainloop.loop.music import music, first
from mainloop.loop.last import last
from mainloop.load import update
from mainloop.load.can import apk
from mainloop.change import change

# need cython
from mainloop.loop.catch import catch
from mainloop.blit import blit
from mainloop.stop import run

# 潜执の囚禁
width, height = 800, 600
pygame.display.set_caption("imprisonment")

with open("debug/logging.log", "w") as file:
    file.write("")

logging.debug(" -- 遊戲開始 -- ")
logging.debug(f"screen - width : {getsx()}, height : {getsy()}")
logging.debug(f"python : {sys.version}")
logging.debug(f"pygame : {pygame.__version__}")
logging.debug(f"file : {__file__}")
logging.debug(f"version : {game.__version__}")

with open("debug/renew.log") as file:
    logging.debug(f"{file.read()}")

init()
change.apk = apk
change.change()
debugs.yes = False
pygame.mixer.music.stop()

@functools.lru_cache(maxsize = None)
@contextlib.contextmanager
def running():
    game.dt = 0
    while game.running:
        mx, my = pygame.mouse.get_pos()
        mouse(mx, my)
        catch(mx, my)
        backing()
        blit.run()
        run.run()
        last()
        music()

        if debugs.yes:
            debugs.surface.draw()

        if update.yes:
            pygame.display.update(update.update())
        else:
            pygame.display.update(window.rect)

        if game.running == False:
            logging.debug(" -- 退出遊戲 -- ")

        if not game.shot:
            game.dt = game.clock.tick() / 60
        else:
            game.shot = False

# captivity

profiler = cProfile.Profile()
profiler.enable()
running()
profiler.disable()
profiler.dump_stats("debug/analyze.prof")

pygame.quit()
sys.exit()