import pygame
from datetime import datetime

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((800,600), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME)

pygame.transform.scale(
    pygame.Surface(
        (800, 600)
    ), 
    screen.get_size(), 
    screen
)

font = {
    "普通" : pygame.font.Font("font/普通.ttc", 50), 
    "金陵" : pygame.font.Font("font/金陵.ttf", 50)
}

__version__ = "0.5.4"

dt : float = 0
renew : bool = False
proce : str = "start"
touches : set = {}
press : set = set()
clock = pygame.time.Clock()
running : bool = True
shot : bool = False
shot2 : int = 0
start : float = datetime.now().timestamp()
end = None

def sw():
    return screen.get_width()

def sh():
    return screen.get_height()
