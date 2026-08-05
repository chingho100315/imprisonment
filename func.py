import pygame
import sys
import logging
import traceback
import inspect
from itertools import cycle
from datetime import datetime
from pickle import load, dump
from os.path import isfile
import game
from mainloop.vague.vague import vague

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

a = game.screen.get_width()
b = game.screen.get_height()
getsx= lambda: a
getsy = lambda: b

MouseX, MouseY = (None, None)

def mouse(a, b):
    global MouseX, MouseY
    MouseX, MouseY = a, b

def ScreenPercentage(x=1, y=1):
    return (getsx() / x, getsy() / y)

def ScreenReversal(x=0, y=0):
    return (getsx() - x, getsy() - y)

def mid(rect, scr = False, sur = game.screen):
    if scr == False:
        if type(rect) == pygame.rect.Rect:
            return (
                (sur.get_width() - rect.w) / 2, 
                (sur.get_height() - rect.h) / 2
            )
        elif len(rect) == 2:
            return (
                (sur.get_width() - rect[0]) / 2, 
                (sur.get_height() - rect[1]) / 2
            )

    else:
        if type(rect) == pygame.rect.Rect:
            return (
                (rect.w + getsx()) / 2, 
                (rect.h + getsy()) / 2
            )

    logging.debug("error is in mid")
    raise Exception("error is in func mid() !!!")

def errors(w, h):
    a = pygame.Surface((w / 2, h / 2))
    b = pygame.Surface((w / 2, h / 2))
    a.fill((255, 0, 0))
    b.fill((0, 0, 0))
    c = pygame.Surface((w, h))

    c.blit(a, (0, 0))
    c.blit(b, (w / 2, 0))
    c.blit(b, (0, h / 2))
    c.blit(a, (w / 2, h / 2))

    return c

def Buffers(x, c, w, h, s=False):
    a = pygame.Surface((w, h))

    if s:
        a.fill((0, 255, 0))
        a.blit(x, (0, 0))
        a = a.convert()
        a.set_colorkey((0, 255, 0))
    else:
        a.fill(c)
        a.blit(x, (0, 0))
        a = a.convert()
        a.set_colorkey(c)

    return a

def ui():
    return not (stop.rect.collidepoint(MouseX, MouseY) or shot.rect.collidepoint(MouseX, MouseY) or exits.rect.collidepoint(MouseX, MouseY))

def menu(x, y):
    for a in range(len(x)):
        said.choice_show(a)

    a = said.choice_rect
    b = []
    for c in y:
        b.append(fontos.SurUse(c))

    for c in b:
        game.screen.blit(
            c, 
            (a.x + (a.w - c.get_width()) / 2, a.y + (a.h - c.get_height()) / 2 - said.choice_number * b.index(c))
        )

    if "button" in said.clicks:
        if (not stop.stop):
            for c in b:
                if a.collidepoint(MouseX, MouseY):
                    said.event.add(x[b.index(c)])
                a.y -= said.choice_number

            for _ in b:
                a.y += said.choice_number

def speak(one="", name="", speak="", black=False, menu=True):
    if black:
        game.screen.blit(
            said.screen, 
            (0, 0)
        )

    if once.once(one):
        fontos.clear()

    said.show()

    game.screen.blit(
        fontos.SurUse(name), 
        said.namexy
    )

    fontos.useplus(speak, said.xy)

    if menu:
        said.clicks.add("speak")

    said.speak = speak

    if said.cursor_show <= 20:
        if fontos.IsMax(speak):
            game.screen.blit(
                said.cursor, 
                said.cursor_rect
            )

def all_speak(proce=[], name=[], say=[], add=0):
    if not (len(proce) == len(name) == len(say)):
        a = f"all_speak 函數的3個列表不一樣！在第 {inspect.currentframe().f_back.f_lineno} 行"
        logging.error(a)
        raise Exception(a)

    for a, b, c in zip(proce, name, say):
        if said.proce == proce.index(a) + add:
            if len(c) - 1 > fontos.num:
                said.now = c[round(fontos.num)]

            speak(
                one=a, 
                name=b, 
                speak=c
            )

def LoadPhoto(name=None, width=None, height=None, rotate=0, reversalx=False, reversaly=False):
    if None in [name, width, height]:
        # 調試
        raise Exception("name, width, height 是必填的")
    try:
        n = f"image/{name}"
        a = pygame.image.load(n)
        b = pygame.transform.scale(a, (width, height))
        c = pygame.transform.rotate(b, rotate)
        d = pygame.transform.flip(c, reversalx, reversaly)
        return d
    except FileNotFoundError:
        # 調試
        logging.error(f"你並沒有文件 : \"{n}\"")
        raise Exception(f"你並沒有文件 : \"{n}\"")

class Once:
    def __init__(self):
        self.record = {}
        self.manys = {}

    def once(self, x):
        if self.record.get(x) == None:
            self.record[x] = True
        if self.record[x]:
            a = self.record[x]
            self.record[x] = False
            return a

    def many(self, x, y):
        if self.manys.get(x) == None:
            self.manys[x] = 0
        if not self.manys[x] >= y:
            a = self.manys[x]
            self.manys[x] += 1
            return a

    def ClearOnce(self, x):
        if self.record.get(x) != None:
            self.record[x] = True

    def ClearMany(self, x):
        if self.manys.get(x) != None:
            self.manys[x] = 0

class Sounds:
    def __init__(self):
        self.sound = {
            "走路" : pygame.mixer.Sound("music/走路.mp3")
        }

    def play(self, x, n):
        if once.once(n):
            self.sound[x].play()

class Back(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.backs = {}
        self.surfaces = {}
    def load(self, n, pn):
        a = ScreenPercentage()
        self.backs[n] = LoadPhoto(name=pn, width=a[0], height=a[1])
        self.surfaces[n] = pygame.Surface((getsx(), getsy()))
        self.surfaces[n].blit(self.backs[n], (0, 0))
    def GetBacks(self, x):
        return self.surfaces[x]

class FpsTick:
    def __init__(self):
        self.fps = 0
        self.all = []
    def add(self):
        self.all.append(game.clock.get_fps())
    def get(self):
        return sum(self.all) / len(self.all)
    def now(self):
        return game.clock.get_fps()
    def ms(self):
        if self.now() != 0:
            return 1 / self.now()
        else:
            return "Infinity"

class Shadow(pygame.sprite.Sprite):
    def __init__(self):
        self.image = LoadPhoto(name="黃昏.png", width=getsx(), height=getsy()).convert()
        self.red = LoadPhoto(name="紅昏.png", width=getsx(), height=getsy()).convert()
        self.red.set_alpha(180)
        self.surface = pygame.Surface((getsx(), getsy()))
        self.surface.blit(self.image, (0, 0))
        self.surface.set_alpha(180)

        self.trans = pygame.Surface((getsx(), getsy()))
        self.trans_num = 255
        self.trans.set_alpha(255)

        self.fear = pygame.Surface((getsx(), getsy()))
        self.fear.fill((255, 0, 0))
        self.fear.set_alpha(45)

    def draw(self):
        game.screen.blit(
            self.surface, 
            (0, 0)
        )

    def reds(self):
        game.screen.blit(
            self.red, 
            (0, 0)
        )

    def tran(self):
        self.trans.set_alpha(self.trans_num)
        game.screen.blit(
            self.trans, 
            (0, 0)
        )

    def clear(self, x):
        self.trans.fill(x)

class Floor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(
            0, 
            ScreenPercentage(y=5)[1], 
            getsx(), 
            ScreenPercentage(y=5)[1]
        )

class Bus(pygame.sprite.Sprite):
    def __init__(self):
        self.image = LoadPhoto(name="bus2.png", width=ScreenPercentage(x=1.8)[0], height=ScreenPercentage(y=1.3)[1])
        self.speed = 18
        self.rect = self.image.get_rect()
        self.rect.x = getsx() - self.speed
        self.rect.y = ScreenReversal(y=self.rect.height)[1]

        self.image = Buffers(self.image, (0, 0, 0), self.rect.w, self.rect.h)

class Timer:
    def __init__(self):
        self.IsStart = {}
        self.Start = {}
        self.Value = {}
        self.os = {}
        self.start = {}
        self.now = datetime.now().timestamp()
        self.new = datetime.now()
        self.screen = 0

    def Renew(self):
        self.now = datetime.now().timestamp()
        self.new = datetime.now()

    def Time(self, x):
        if self.IsStart[x]:
            self.Start[x] = self.now

    def GetTime(self, x):
        return self.now - self.Start[x]

    def GetTimes(self, x):
        return self.Value[x] + self.GetTime(x)

    def Timer(self, x):
        if stop.stop:
            self.Time(x)
            self.IsStart[x] = False
        else:
            if not self.IsStart[x]:
                self.Value[x] += self.GetTime(x)
            self.Start[x] = self.now
            self.IsStart[x] = True

    def init(self, x):
        if self.start.get(x) == None:
            self.start[x] = self.now
            self.os[x] = []
            self.IsStart[x] = True
            self.Value[x] = 0
            self.Start[x] = self.now
            self.screen = 0

        self.Timer(x)

    def Os(self, x, y):
        try:
            return timer.now - timer.start[x] <= self.os[x][y] + self.GetTimes(x) + self.screen
        except Exception as e:
            logging.debug(f"timer.Os 函數 x : {x}, y : {y}, type x : {type(x)}, type y : {type(y)}")
            raise Exception(e)

    def wait(self, x):
        return timer.now - timer.start[x] - (self.GetTimes(x) + self.screen)

    def clear(self, x):
        self.start[x] = None

class Achv(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        if isfile("save/save.pkl"):
            with open("save/save.pkl", "rb") as f:
                self.save = load(f)
        else:
            with open("save/save.pkl", "wb") as f:
                self.save = {
                    "first" : {
                        "have" : False
                    }, 
                    "apple key?" : {
                        "have" : False
                    }
                }
                dump(self.save, f)

        self.image = LoadPhoto(name="achv2.png", width=getsx() / 12, height=getsy() / 10.5)
        self.font = {
            "first" : game.font["金陵"].render("第一次", True, (0, 0, 0)), 
            "apple key?" : game.font["金陵"].render("蘋果碼？", True, (0, 0, 0))
        }
        self.rect = self.image.get_rect()
        self.rect.x = (getsx() - self.rect.w) / 2
        self.rect.y = 0
        self.show = {
            "first" : self.rect.h, 
            "apple key?" : self.rect.h
        }
        self.image = Buffers(self.image, (1, 0, 0), self.rect.w, self.rect.h)
        self.xy = {
            "first" : ((getsx() - self.font["first"].get_rect().w) / 2, (self.rect.h - self.font["first"].get_rect().h) / 2), 
            "key" : ((getsx() - self.font["apple key?"].get_rect().w) / 2, (self.rect.h - self.font["apple key?"].get_rect().h) / 2)
        }

    def saves(self):
        with open("save/save.pkl", "wb") as f:
            dump(self.save, f)

class Said(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        a = ScreenPercentage(y=3)[1]
        self.surface = pygame.Surface((getsx() - a * 0.4, a))
        self.surface.set_alpha(130)
        self.surface.fill((255, 100, 255))
        self.rect = self.surface.get_rect()
        self.rect.x = a * 0.2
        self.rect.y = ScreenReversal(y=a * 1.2)[1]

        self.now = ""
        self.cursor = Buffers(LoadPhoto(name="光標.png", width=50, height=50), (0, 0, 0), 50, 50)
        self.cursor_rect = self.cursor.get_rect()
        self.cursor_rect.x = self.rect.x + self.rect.w - self.cursor_rect.w * 2
        self.cursor_rect.y = self.rect.y + self.rect.h - self.cursor_rect.h * 2

        self.far = 15
        self.clicks = set()
        self.proce = 0
        self.big_proce = 0
        self.speak = ""
        self.cursor_show = 0

        self.choice = pygame.Surface((ScreenPercentage(x=10)[0], ScreenPercentage(y=12)[1]))
        self.choice.fill((137, 194, 255))
        self.choice_number = self.far + self.choice.get_height()
        self.choice.set_alpha(180)
        self.choice_rect = self.choice.get_rect()
        self.choice_rect.x = getsx() - self.choice.get_width() - (self.rect.x - self.far)
        self.choice_rect.y = self.rect.y - self.choice.get_height() - self.rect.x / 2

        self.name = pygame.Surface((self.rect.w / 12, self.rect.h / 5))
        self.namerect = self.name.get_rect()
        self.name.set_alpha(130)
        self.name.fill((81, 128, 150))

        self.screen = pygame.Surface((getsx(), getsy()))
        self.screen.set_alpha(180)
        self.screen.fill((10, 10, 0))
        self.xy = (self.rect.x + self.far * 3, self.rect.y + self.far * 2)

        self.namerect.x = self.rect.x + self.far * 3
        self.namerect.y = self.rect.y - self.far - self.namerect.h

        a = game.font["金陵"].render("执法", True, (0, 0, 0))
        b = a.get_rect()
        c = self.namerect
        self.namexy = (c.x + (c.w - b.w) / 2, c.y + (c.h - b.h * 1.1) / 2)

        self.event = set()

    def choice_show(self, n):
        game.screen.blit(
            self.choice, 
            (self.choice_rect.x, self.choice_rect.y - self.choice_number * n)
        )

    def show(self):

        self.surface.fill((145, 207, 213))

        game.screen.blit(
            self.surface, 
            (self.rect.x - self.far, self.rect.y + self.far)
        )

        self.surface.fill((17, 48, 86))

        game.screen.blit(
            self.surface, 
            (self.rect.x + self.far, self.rect.y - self.far)
        )

        game.screen.blit(
            self.name, 
            (self.rect.x + self.far * 3, self.rect.y - self.far - self.namerect.h)
        )

    def Del(self):
        if "speak" in said.clicks:
            said.clicks.remove("speak")
            said.proce = 0

    def get_event(self, x):
        if type(x) == list:
            b = []
            for a in x:
                b.append(a in said.event)
            return any(b)
        return x in said.event

    def del_event(self, x):
        said.event.remove(x)

    def finish(self, x):
        return said.proce >= x

class FontOS(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = {}
        self.type = "金陵"
        self.surface = {}
        self.num = 0
        self.check = 0
        self.speed = 1
        self.proce = 0
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.orange = (255, 128, 0)
        self.yellow = (255, 255, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.purple = (128, 0, 255)
        self.pink = (255, 128, 255)
    def use(self, x):
        return self.font[x]
    def load(self, x, color):
        self.font[x] = game.font[self.type].render(
            x, 
            False, 
            color
        )

    def loadplus(self, x, color):
        self.font[f"%{x}"] = {}

        for a in range(len(x) + 1):
            self.font[f"%{x}"][x[:a]] = game.font[self.type].render(
                x[:a], 
                False, 
                color
            )
            b = self.font[f"%{x}"][x[:a]].get_rect()
            c = pygame.Surface((b.w, b.h))
            c.blit(self.font[f"%{x}"][x[:a]], b)
            c.set_colorkey((0, 0, 0))
            self.font[f"%{x}"][x[:a]] = c

    def useplus(self, n, xy):
        game.screen.blit(
            self.font[f"%{n}"][n[:round(self.num)]], 
            xy
        )

    def Surload(self, n, alpha):
        a = game.font[self.type].render(n, False, (0, 0, 0))
        a = a.get_rect()
        self.surface[n] = pygame.Surface((a.w, a.h))
        self.surface[n].fill((255, 255, 0))
        self.surface[n].blit(self.use(n), (0, 0))
        self.surface[n].set_alpha(alpha)
        self.surface[n].set_colorkey((255, 255, 0))
    def SurUse(self, n):
        return self.surface[n]

    def NextWord(self):
        self.num += self.speed
    def IsMax(self, n):
        return self.num >= len(n)
    def Proce(self, n):
        return self.proce == n
    def Check(self):
        if self.check + self.speed * 3 <= self.num:
            self.check += 1
            return True
        return False
    def clear(self):
        self.num = 0

class Stop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = LoadPhoto(name="暫停像素.png", width=ScreenPercentage(x=12)[0], height=ScreenPercentage(x=12)[0])
        self.image2 = LoadPhoto(name="繼續像素.png", width=ScreenPercentage(x=12)[0], height=ScreenPercentage(x=12)[0])

        self.click = False

        self.rect = self.image.get_rect()
        self.rect.x = ScreenReversal(x=self.rect.width*3)[0]
        self.rect.y = 0

        self.surface = pygame.Surface(ScreenPercentage())
        self.surface.set_alpha(64)
        self.surface.fill((255, 164, 0))

        self.font = game.font["金陵"].render("暫停", False, (0, 0, 0))

        self.font = Buffers(self.font, (255, 0, 0), self.font.get_rect().w, self.font.get_rect().h, s=True)
        self.font_rect = self.font.get_rect()
        self.font_rect.x = (getsx() - self.font_rect.w) / 2
        self.font_rect.y = 0

        self.stop = False

    def draw(self):
        game.screen.blit(
            self.font, 
            self.font_rect
        )

class Shot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = LoadPhoto(name="截圖2.png", width=ScreenPercentage(x=12)[0], height=ScreenPercentage(x=12)[0])
        self.rect = self.image.get_rect()
        self.rect.x = stop.rect.x + stop.rect.w
        self.rect.y = stop.rect.y
        self.image = Buffers(self.image, (0, 0, 0), self.rect.w, self.rect.h, s=True)
        self.click = False

        self.image_false = LoadPhoto(name="截圖-2.png", width=getsy() * 0.8, height=getsy() * 0.8)

class Exits(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = LoadPhoto(name="Exit.png", width=ScreenPercentage(x=12)[0], height=ScreenPercentage(x=12)[0])
        self.rect = self.image.get_rect()
        self.rect.x = stop.rect.x + stop.rect.w * 2
        self.rect.y = stop.rect.y
        self.image = Buffers(self.image, (0, 0, 0), self.rect.w, self.rect.h)
        self.click = False

        self.image2 = Buffers(LoadPhoto(name="E.png", width=self.rect.w, height=self.rect.h), (0, 255, 0), self.rect.w, self.rect.h)

class Inter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = LoadPhoto(name="互動像素3.png", width=ScreenPercentage(x=10)[0], height=ScreenPercentage(y=10)[1])
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.w / 2
        self.rect.y = getsy() - self.rect.h - self.rect.w / 2

        self.event = ""
        self.click = False

        self.image = Buffers(self.image, (255, 255, 255), self.rect.w, self.rect.h)

        a = game.font["金陵"].render("兩字", True, (0, 0, 0))
        a = a.get_rect()
        self.xy = (self.rect.x + self.rect.w / 3 * 1.55, self.rect.y + (self.rect.h - a.h) / 2)

class Move(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.right_image = LoadPhoto(
            name="Move.png", 
            width=ScreenPercentage(x=10)[0], 
            height=ScreenPercentage(x=10)[0]
        )
        self.left_image = LoadPhoto(
            name="Move.png", 
            width=ScreenPercentage(x=10)[0], 
            height=ScreenPercentage(x=10)[0], 
            reversalx=True
        )
        self.can = False
        self.right_rect = self.right_image.get_rect()
        self.left_rect = self.left_image.get_rect()

        self.right_rect.y = ScreenReversal(y=self.right_rect.height)[1]
        self.left_rect.y = ScreenReversal(y=self.left_rect.height)[1]

        self.right_rect.x = ScreenReversal(x=self.right_rect.width)[0]
        self.left_rect.x = ScreenReversal(x=self.left_rect.width * 2)[0]

        self.right_image = Buffers(self.right_image, (0, 0, 0), self.right_rect.w, self.right_rect.h)

        self.left_image = Buffers(self.left_image, (0, 0, 0), self.left_rect.w, self.left_rect.h)

    def draw(self):
        game.screen.blit(
            self.right_image, 
            self.right_rect
        )
        game.screen.blit(
            self.left_image, 
            self.left_rect
        )

class Thing(pygame.sprite.Sprite):
    def __init__(self, name, image, width, height, x, y, color):
        super().__init__()
        self.thing = {}
        self.value = {}
        self.more = {}
        for a, b, c, d, e, f, g in zip(name, image, width, height, x, y, color):
            self.thing[a] = {}
            self.thing[a]["image"] = b
            self.thing[a]["image"] = Buffers(self.thing[a]["image"], g, c, d)
            self.thing[a]["rect"] = pygame.Rect(e, f, c, d)

    def add(self, dame, name, width, height, color=(0, 255, 0), x=0, y=0) -> None:
        class things:
            pass

        self.more[dame] = things()
        self.more[dame].image = LoadPhoto(name=name, width=width, height=height)
        self.more[dame].image = Buffers(self.more[dame].image, color, width, height)
        self.more[dame].rect = self.more[dame].image.get_rect()
        self.more[dame].rect.x, self.more[dame].rect.y = x, y

    def get(self, dame):
        return self.more[dame]

    def draw(self, dame, image="image", rect="rect"):
        exec(f"game.screen.blit(self.more[dame].{image}, self.more[dame].{rect})")

    def invent(self, dame, image="image", rect="rect"):
        return eval(
            "{" + 
            f"'name' : '{dame}', " + 
            f"'image' : self.more['{dame}'].{image}, 'rect' : self.more[{'dame'}].{rect}" + 
            "}"
         )

    def print(self, dame):
        logging.debug(f"{self.more[dame].rect.x}, {self.more[dame].rect.y}")

class Invent:
    def __init__(self):
        self.data = [None for _ in range(5)]
        self.now = 0
        self.show = True

        thing.add("invert", "invert3.png", 160, 160)
        rect = thing.more["invert"].rect
        thing.more["invert"].rect.x = mid(rect)[0] - rect.w * 2
        thing.more["invert"].rect.y = getsy() - rect.h

        thing.more["invert"].image2 = Buffers(LoadPhoto(name="invert2.png", width=160, height=160), (0, 255, 0), 160, 160)
        thing.more["invert"].rect2 = rect.copy()

        self.rects = []

        surface = pygame.Surface((rect.w * 5, rect.h))

        for a in range(0, rect.w * 6, rect.w):
            surface.blit(thing.more["invert"].image, (a, 0))
            self.rects.append(pygame.Rect((rect.x + a, rect.y, rect.w , rect.h)))

        thing.more["invert"].image = surface

    def clear(self, number):
        for a in self.data:
            if a is None:
                return False
            if a.get("name") == number:
                self.data[self.data.index(a)] = None
        return False

    def click(self, tx, ty):
        if self.show:
            for a in range(5):
                if invent.rects[a].collidepoint(tx, ty):
                    invent.now = a

    def add(self, things):
        if not things in self.data:
            number = len(self.data) - self.data.count(None)
            self.data[number] = things

    def change(self):
        thing.more["invert"].rect2.x = thing.more["invert"].rect.x + 160 * (self.now)

    def is_thing(self, things, now = True):
        if now:
            for a in self.data:
                if a is None:
                    return False
                if a.get("name") == things:
                    return self.now == self.data.index(a)
        else:
            for a in self.data:
                if type(a) == dict:
                    if a["name"] == things:
                        return True

        return False

    def draw(self):
        if self.show:
            if (not stop.stop):
                invent.change()
            thing.draw("invert")
            thing.draw("invert", image="image2", rect="rect2")

            add = (0, 0)
            for a, b in zip(invent.data, range(len(invent.data))):
                add = (0, 0)

                if a != None:
                    if a["name"] == "axe":
                        add = (15, 0)

                    game.screen.blit(
                        a["image"], 
                        ((thing.more["invert"].rect.x + b * 160) + add[0], thing.more["invert"].rect.y + add[1])
                    )

class Start:
    def __init__(self):
        self.image = LoadPhoto(name="start.png", width=getsx(), height=getsy())
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.image = Buffers(self.image, (255, 0, 0), self.rect.w, self.rect.h)
        fontos.load("點擊即可開始", fontos.white)
        self.font = fontos.use("點擊即可開始")
        self.font_rect = self.font.get_rect()
        self.font_rect.x = (getsx() - self.font_rect.w) / 2
        game.font["囚禁"] = pygame.font.Font("font/金陵.ttf", getsy())
        fontos.type = "囚禁"
        fontos.load("囚禁", (50, 0, 0))
        self.font2 = fontos.use("囚禁")
        self.font2 = pygame.transform.scale(self.font2, (getsx(), getsy()))
        self.font2 = Buffers(self.font2, (254, 0, 0), getsx(), getsy())
        self.font2.set_alpha(145)

        fontos.load("開始", (255, 0, 0))
        self.font3 = fontos.use("開始")
        self.font3 = pygame.transform.scale(self.font3, (getsx(), getsy()))
        self.font3 = Buffers(self.font3, (254, 0, 0), getsx(), getsy())
        self.font3.set_alpha(shadow.trans_num)

        fontos.type = "金陵"

        self.surface = pygame.Surface((getsx(), getsy()))
        self.surface.fill((81, 95, 162))
        self.surface.set_alpha(32)

class Window:
    def __init__(self):
        self.rect = pygame.Rect((0, 0), (getsx(), getsy()))
        self.group = {}

class Sheriff(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = {}

        for a, b in zip(["normal", "right", "happy"], ["执法me.png", "执走me.png", "执笑me.png"]):
            if a != "happy":
                self.image[a] = LoadPhoto(name=b, width=ScreenPercentage(x=8)[0], height=ScreenPercentage(x=8)[0])
                self.image[a] = Buffers(self.image[a], (0, 0, 0), self.image[a].get_rect().w, self.image[a].get_rect().h)
            else:
                self.image[a] = LoadPhoto(name=b, width=getsy(), height=getsy())

        self.image["said"] = self.image["happy"]
        self.image["said"] = Buffers(self.image["said"], (0, 0, 0), getsy(), getsy())

        self.rect = self.image["normal"].get_rect()
        self.z = 0
        self.rect.y = ScreenReversal(y=floor.rect.height - self.rect.height)[1]
        self.speed = 15

class Stealth(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = {}

        self.size = ScreenPercentage(x=8)[0]
        self.image["normal"] = LoadPhoto(name="潜行me.png", width=self.size, height=self.size)
        self.image["sick"] = LoadPhoto(name="潜病me.png", width=self.size, height=self.size)
        self.image["crazy"] = LoadPhoto(name="潜瘋.png", width=self.size, height=self.size)

        self.rect = self.image["normal"].get_rect()
        self.rect.x = getsx() / 2.0789
        self.rect.y = getsy() / 1.5857

        self.image["normal"] = Buffers(self.image["normal"], (1, 1, 0), self.rect.w, self.rect.h)
        self.image["sick"] = Buffers(self.image["sick"], (0, 1, 0), self.rect.w, self.rect.h)
        self.image["crazy"] = Buffers(self.image["crazy"], (0, 1, 0), self.rect.w, self.rect.h)

        self.image["big"] = pygame.transform.scale(
            self.image["sick"], 
            (ScreenPercentage(y=1.5)[1], ScreenPercentage(y=1.5)[1])
        )

        self.change = cycle(
            [
                pygame.transform.scale(
                    self.image["sick"], 
                    (getsy(), getsy())
                ), 
                pygame.transform.scale(
                    self.image["crazy"], 
                    (getsy(), getsy())
                )
            ]
        )

        self.now = next(self.change)
        self.tick = 0

        #
        #self.image["big"] = errors(ScreenPercentage(y=1.5)[1], ScreenPercentage(y=1.5)[1])
        #

class Truth(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = {}

        self.image["normal"] = LoadPhoto(name="真心me.png", width=ScreenPercentage(x=8)[0], height=ScreenPercentage(x=8)[0])

        self.image["sit"] = LoadPhoto(name="真心me.png", width=ScreenPercentage(x=8)[0], height=ScreenPercentage(x=8)[0], rotate=10)

        self.image["said"] = LoadPhoto(name="真心me.png", width=getsy(), height=getsy())

        self.rect = self.image["normal"].get_rect()
        self.rect.x = getsx() / 2.0113
        self.rect.y = getsy() / 1.5857

        self.image["normal"] = Buffers(self.image["normal"], (0, 0, 0), self.rect.w, self.rect.h)
        self.image["sit"] = Buffers(self.image["sit"], (0, 0, 0), self.image["sit"].get_rect().w, self.image["sit"].get_rect().h)
        self.image["said"] = Buffers(self.image["said"], (0, 0, 0), getsy(), getsy())

once = Once()
sounds = Sounds()
back = Back()
fpstick = FpsTick()
shadow = Shadow()
floor = Floor()
bus = Bus()
timer = Timer()
said = Said()
fontos = FontOS()
achv = Achv()
stop = Stop()
shot = Shot()
exits = Exits()
inter = Inter()
move = Move()
start = Start()
window = Window()
sheriff = Sheriff()
stealth = Stealth()
truth = Truth()

thing = Thing(
    ["table", "apple", "key", "love", "day", "old key", "fear", "time"], 
    [
       LoadPhoto(name="table.png", width=1000, height=800), 
       LoadPhoto(name="apple.png", width=100, height=100), 
       LoadPhoto(name="按2.png", width=200, height=200), 
       LoadPhoto(name="love.png", width=getsy(), height=getsy()), 
       LoadPhoto(name="日記.png", width=getsx(), height=getsy()), 
       LoadPhoto(name="key.png", width=100, height=100), 
       LoadPhoto(name="恐景2.png", width=getsx() * 1.1, height=getsy() * 1.1), 
       LoadPhoto(name="time.png", width=100, height=100)
    ], 
    [1000, 100, 200, getsy(), getsx(), 100, getsx() * 1.1, 100], 
    [800, 100, 200, getsy(), getsy(), 100, getsy() * 1.1, 100], 
    [0, 0, 0, (getsx() - getsy()) / 2, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [(0, 0, 0)] * 6 + [(254, 0, 0)] + [(0, 0, 0)] * 1
)
invent = Invent()
