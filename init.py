import pygame
import sys
import logging
import traceback
import game
from datetime import datetime
from func import *
from mainloop.vague.vague import vague

logging.basicConfig(level=logging.DEBUG,
    format="%(asctime)s\n%(levelname)s\n%(message)s\n", 
    handlers=[
        logging.FileHandler("debug/logging.log")
    ]
)

sys.excepthook = lambda *e: [
    logging.error("\n" + "".join(traceback.format_exception(*e)))
]

def inits():
    a : pygame.rect = thing.thing["table"]["rect"]
    b : pygame.rect = thing.thing["apple"]["rect"]
    c : pygame.rect = thing.thing["key"]["rect"]

    thing.thing["table"]["rect"].x : float = (getsx() - a.w) / 2
    thing.thing["table"]["rect"].y : float = (getsy() - a.h) / 2 + b.h * 1.5

    thing.thing["apple"]["rect"].x : float = (getsx() - b.w) / 2
    thing.thing["apple"]["rect"].y : float = (getsy() - b.h) / 2
    thing.value["apple"] : bool = False

    thing.thing["old key"]["rect"].x : float = thing.thing["apple"]["rect"].x - thing.thing["apple"]["rect"].w * 1.2
    thing.thing["old key"]["rect"].y : float = thing.thing["apple"]["rect"].y - thing.thing["apple"]["rect"].h * 0.3
    thing.value["old key show"] : bool = True

    thing.thing["key"]["rect"].x : float = (getsx() - c.w) / 2
    thing.thing["key"]["rect"].y : float = (getsy() - c.h) / 2
    thing.value["key"] : dict = {}
    thing.value["word"] : dict = {}
    game.font["密碼"] : pygame.surface = pygame.font.Font("font/金陵.ttf", round(c.h / 2))

    thing.value["key surface"] : pygame.surface = pygame.Surface((c.w * 3, c.h * 4))
    thing.value["key surface"].set_alpha(200)

    thing.value["key board"] : pygame.surface = pygame.Surface((c.w * 3, c.h))
    thing.value["key board"].set_alpha(200)
    thing.value["key board"].fill((50, 50, 50))

    thing.value["key end"] : str = ""
    thing.value["key click"] : bool = False
    thing.value["key down"] : str = ""
    thing.value["key image"] : surface = Buffers(LoadPhoto(name="反按2.png", width=c.w, height=c.h), (0, 0, 0), c.w, c.h)
    thing.value["key said"] : bool = False
    thing.value["love"] : int = 0
    thing.value["read"] : int = 0
    thing.value["read said"] : float = False
    thing.value["notice"] : int = 6
    thing.value["Proce 6 said"] : bool = False

    a : list = [-c.w, 0, c.w, -c.w, 0, c.w, -c.w, 0, c.w]
    b : list = [-c.h, -c.h, -c.h, 0, 0, 0, c.h, c.h, c.h]
    for x, y, z in zip(a, b, range(1, 10)):
        thing.value["key"][str(z)] : tuple = (c.x + x, c.y + y)
        fontos.load(str(z), fontos.black)
        thing.value["word"][str(z)] : pygame.surface = fontos.use(str(z))
    thing.value["key"]["0"] : tuple = (c.x, c.y + c.h * 2)
    fontos.load("0", fontos.black)
    thing.value["word"]["0"] : pygame.surface = fontos.use("0")
    thing.value["key"]["d"] : tuple =  (c.x + c.w, c.y + c.h * 2)
    thing.value["word"]["d"] : pygame.surface = LoadPhoto(name="del.png", width=c.w, height=c.h)

    fontos.speed : int = 1

    with open("load/load/text.txt") as text:
        with open("load/load/color.txt") as color:
            for a, b in zip(text.read().split("\n"), color.read().split("\n")):
                fontos.load(a, eval(b))

    with open("load/Surload/text.txt") as text:
        with open("load/Surload/alpha.txt") as alpha:
            for a, b in zip(text.read().split("\n"), alpha.read().split("\n")):
                fontos.Surload(a, eval(b))

    fontos.type : str = "密碼"
    for a in range(0, 10):
        fontos.load(str(a), fontos.pink)
    fontos.type : str = "金陵"

    game.font["囚禁"] : pygame.font.Font = pygame.font.Font("font/金陵.ttf", getsy())
    fontos.type : str = "囚禁"
    fontos.load("3784280", (128, 0, 0))
    thing.value["key_press"] : pygame.surface = fontos.use("3784280")
    thing.value["key_press"] : pygame.surface = pygame.transform.scale(thing.value["key_press"], (400, 200))
    thing.value["key_press"] : pygame.surface = Buffers(thing.value["key_press"], (255, 0, 0), 400, 200)
    thing.value["key_press"].set_alpha(100)
    fontos.type : str = "金陵"

    thing.value["buttons"] : pygame.surface = pygame.Surface((c.w * 3, c.h * 4))
    thing.value["buttons"].set_colorkey((0, 0, 0))
    cs : pygame.rect = c
    cs.x, cs.y = cs.x - cs.w, cs.y - cs.h
    for a, b, c in zip(thing.value["key"].values(), thing.value["word"].values(), thing.value["key"].keys()):
        if thing.value["key down"] != c:
            thing.value["buttons"].blit(
                thing.thing["key"]["image"], 
                (a[0] - cs.x, a[1] - cs.y)
            )
        else:
            thing.value["buttons"].blit(
                thing.value["key image"], 
                (a[0] - cs.x, a[1] - cs.y)
            )

        if b != thing.value["word"]["d"]:
            thing.value["buttons"].blit(
                b, 
                ((a[0] - cs.x) + thing.thing["key"]["rect"].w / 2.4, (a[1] - cs.y) + thing.thing["key"]["rect"].h / 3)
            )
        else:
            thing.value["buttons"].blit(
                b, 
                (a[0] - cs.x, a[1] - cs.y)
            )

    for x in range(thing.value["notice"]):
        with open(f"journal/潜行日記{x+1}.txt") as file:
            thing.value["day"] = file.read()
            for a in thing.value["day"].split("\n"):
                if x in [0, 1, 2]:
                    fontos.load(a, fontos.black)
                if x == 3:
                    fontos.load(a, (128, 0, 0))
                if x == 4:
                    fontos.load(a, fontos.red)
                if x == 5:
                    fontos.load(a, (200, 0, 0))
            b : int = 0
            for a in thing.value["day"].split("\n"):
                b += fontos.use(a).get_height()
            thing.value[f"day surface {x}"] = pygame.Surface((getsx(), b))
            thing.value[f"day surface {x}"].fill((1, 1, 1))
            b : int = 0
            for a in thing.value["day"].split("\n"):
                thing.value[f"day surface {x}"].blit(
                    fontos.use(a), 
                    (0, b)
                )
                b += fontos.use(a).get_height()
            thing.value[f"day surface {x}"].set_colorkey((1, 1, 1))
            thing.value[f"day surface 0"].set_alpha(0)

    with open("load/loadplus/text.txt") as text:
        with open("load/loadplus/color.txt") as color:
            for a, b in zip(text.read().split("\n"), color.read().split("\n")):
                fontos.loadplus(a, eval(b))

    back.load("bus stop", "bus_stop.png")
    back.load("in bus", "巴士_內.jpg")
    back.load("the road", "road.jpg")
    back.load("in house", "back11.jpg")
    back.load("red", "房間.webp")
    back.load("bus out", "bus_out.jpg")
    back.load("exit", "出口(long).png")
    back.load("fear", "恐室.png")
    back.load("room", "room.png")
    back.load("bed", "血景.png")
    back.surfaces["bus out"] : pygame.surface = vague(back.backs["bus out"], 0.2, 15)

    rect : pygame.rect = back.surfaces["exit"].get_rect()
    back.surfaces["exit"] : pygame.surface = pygame.transform.scale(
        back.surfaces["exit"], 
        (rect.w * 1.1, rect.h * 1.1)
    )
    shadow.clear((248, 158, 95))

    window.group["proce -1"] : pygame.surface = pygame.Surface((getsx(), getsy()))

    window.group["proce -1"].blit(
        start.image, 
        start.rect
    )

    window.group["proce -1"].blit(
        start.surface, 
        (0, 0)
    )

    window.group["proce -1"].blit(
        start.font, 
        start.font_rect
    )

    window.group["proce -1"].blit(
        start.font2, 
        (0, 0)
    )

    thing.value["fear"] : tuple = (getsx() * 0.1, getsy() * 0.1)
    thing.thing["fear"]["add"] : list = [0, 0]
    thing.thing["fear"]["distance"] : float = 0 #max = 500
    thing.thing["fear"]["metres"] : float = 500
    thing.thing["fear"]["rect"].x : float = - (thing.value["fear"][0] / 2)
    thing.thing["fear"]["rect"].y : float = - (thing.value["fear"][1] / 2)
    thing.thing["fear"]["size"] : float = 0

    game.font["fear metres"] : pygame.font.Font = pygame.font.Font("font/金陵.ttf", round(getsy()))
    game.font["gold"] : pygame.font.Font = pygame.font.Font("font/金陵.ttf", 50)
    thing.thing["fear"]["font"] : dict = {}
    thing.thing["fear"]["door shock"] : float = 0
    thing.thing["fear"]["door font"] : dict = {}
    thing.thing["fear"]["door fonts"] : pygame.surface = pygame.Surface(
        (
            game.font["金陵"].render("0" * 4, False, (0, 0, 0)).get_width(), 
            game.font["金陵"].render("0" * 4, False, (0, 0, 0)).get_height()
        )
    )
    thing.thing["fear"]["door fonts"].set_colorkey((0, 0, 0))
    thing.thing["fear"]["fonts"] : pygame.surface = pygame.Surface((getsx(), getsy()))

    def getting(x, y, a):
        thing.thing["fear"][x][a] = game.font[y].render(
            str(a), 
            False, 
            fontos.red
        )

        image = thing.thing["fear"][x][a]
        rect = image.get_rect()
        thing.thing["fear"][x][a] = Buffers(
            image, 
            (0, 0, 0), 
            rect.w, 
            rect.h
        )

        thing.thing["fear"]["font"][a] = pygame.transform.scale(
            thing.thing["fear"]["font"][a], 
            (getsx() / 3, getsy())
        )

    for a in range(10):
        getting("font", "fear metres", a)

        thing.thing["fear"]["door font"][a] = game.font["gold"].render(
            str(a), 
            False, 
            fontos.red
        )

    thing.thing["fear"]["fonts"].set_alpha(50)
    thing.thing["fear"]["fonts"].set_colorkey((0, 0, 0))
    thing.thing["fear"]["door"] = 100
    thing.thing["fear"]["is speed"] = False
    thing.thing["fear"]["can speed"] = True
    thing.thing["fear"]["come"] = False
    thing.thing["fear"]["sound"] = []
    thing.thing["fear"]["sleep"] : int = 0

    def run(x):
        a = LoadPhoto(
            name=f"{x}.png", 
            width=stop.rect.w, 
            height=stop.rect.h
        )

        a = Buffers(
            a, 
            (0, 0, 0), 
            a.get_width(), 
            a.get_height()
        )

        a.set_colorkey((0, 0, 0))
        return a

    thing.thing["fear"]["run"] = {}
    thing.thing["fear"]["is run"] = False
    thing.thing["fear"]["run"]["run"] = run("rt")
    thing.thing["fear"]["run"]["nun"] = run("rf")
    thing.thing["fear"]["run"]["speed"] = run("st")
    thing.thing["fear"]["run"]["npeed"] = run("sf")

    thing.thing["fear"]["run"]["cd"] = 0
    thing.thing["fear"]["run"]["run rect"] = thing.thing["fear"]["run"]["run"].get_rect()
    thing.thing["fear"]["run"]["speed rect"] = thing.thing["fear"]["run"]["speed"].get_rect()
    thing.thing["fear"]["cd font"] = {}

    for a in range(11):
        thing.thing["fear"]["cd font"][a] = game.font["fear metres"].render(
            f"{a:02d}", 
            False, 
            (255, 255, 255)
        )

        rect = thing.thing["fear"]["run"]["run rect"]
        thing.thing["fear"]["cd font"][a] = pygame.transform.scale(
            thing.thing["fear"]["cd font"][a], 
            (rect.w, rect.h * 1.4)
        )

        thing.thing["fear"]["cd font"][a] = Buffers(
            thing.thing["fear"]["cd font"][a], 
            (0, 0, 0), 
            rect.w, 
            rect.h * 1.4
        )

        thing.thing["fear"]["cd font"][a].set_alpha(100)

    rr = thing.thing["fear"]["run"]["run rect"]
    sr = thing.thing["fear"]["run"]["speed rect"]
    rr.x = rr.w
    rr.y = getsy() - rr.h * 2
    sr.x = getsx() - sr.w * 2
    sr.y = getsy() - sr.h * 2 
    thing.thing["fear"]["run"]["run rect"] = rr
    thing.thing["fear"]["run"]["speed rect"] = sr

    fontos.type = "金陵"

    game.font["RUN"] = pygame.font.Font("font/金陵.ttf", round(getsy() / 3))
    fontos.type = "RUN"
    fontos.load("RUN!!!", fontos.red)

    a = fontos.use("RUN!!!").get_rect()

    thing.thing["fear"]["image"].blit(
        fontos.use("RUN!!!"), 
        ((getsx() - a.w) / 2 + thing.value["fear"][0] / 2, (getsy() - a.h) / 2 + thing.value["fear"][1] / 2)
    )

    fontos.type = "金陵"

    thing.thing["time"]["rect"].y = getsy() - thing.thing["fear"]["rect"].h / 8
    thing.thing["time"]["time"] = []
    thing.thing["time"]["x"] = []
    thing.thing["time"]["can"] = False
    thing.thing["time"]["add"] = 0
    thing.thing["time"]["cd"] = 12
    thing.thing["time"]["now"] = -1

    # 到這里是proce狀態機為8的初始化

    thing.value["sleep"] = 0

    # 桌子的初始化
    thing.add("table_2", "table2.png", getsx() / 2, getsy() / 2, color=(0, 0, 0))
    rect = thing.more["table_2"].rect
    thing.more["table_2"].rect.x, thing.more["table_2"].rect.y = mid(rect)[0], getsy() - getsy() / 128 * 15 - rect.h

    # 紙條的初始化
    thing.add("paper", "paper.png", 150, 150)
    rect = thing.more["paper"].image.get_rect()
    thing.more["paper"].rect.x, thing.more["paper"].rect.y = mid(rect)[0], thing.more["table_2"].rect.y + rect.h * 1.4
    thing.more["paper"].image2 = Buffers(LoadPhoto(name="便條2.png", width=getsy(), height=getsy()), (0, 255, 0), getsy(), getsy())
    thing.more["paper"].rect2 = thing.more["paper"].image2.get_rect()
    thing.more["paper"].rect2.x = (getsx() - getsy()) / 2
    thing.more["paper"].get = False
    thing.more["paper"].can = False

    # 斧頭的初始化
    rect = thing.more["paper"].rect
    thing.add("axe", "axe.png", 150, 150, x = rect.x + 150, y = rect.y - 15)
    thing.more["axe"].image2 = pygame.transform.rotate(thing.more["axe"].image, 15)
    thing.more["axe"].have = False

    # 櫃子的初始化
    rect = thing.more["table_2"].rect
    size = 200
    number = 0.64 * 2
    x, y = 0, 0
    thing.add("cabinet", "cabinet_colse_2.png", size * number, size, x = x, y = y)

    thing.more["cabinet"].image2 = Buffers(
        LoadPhoto("cabinet_open_2.png", size * number, size), 
        (0, 255, 0), 
        size * number, size
    )

    thing.more["cabinet"].open = False

    # key的初始化
    rect = thing.more["cabinet"].rect
    thing.add("key_2", "key_2.png", rect.w / 2, rect.h / 2, x = rect.w / 4)
    thing.more["key_2"].image2 = pygame.transform.scale(
        thing.more["key_2"].image, 
        (invent.rects[0].w, invent.rects[0].h)
    )
    thing.more["key_2"].show = True

    # 床的初始化
    w, h = getsx() / 2, getsy() / 1.5
    thing.add("bed", "bed2.png", w, h, x = mid([w, h])[0], y = getsy() - h)
    thing.value["sf"] = False

    # 櫃子2的初始化
    rect = thing.more["cabinet"].rect
    rect2 = thing.more["bed"].rect
    thing.add("cabinet_2", "cabinet_3.png", rect.w, rect.h, x = rect2.x - rect.w, y = getsy() - rect.h * 2)
    thing.more["cabinet_2"].next = False

def init():
    try:
        inits()
    except Exception as error:
        logging.debug(f"init error : {error}")
        raise Exception(error)
