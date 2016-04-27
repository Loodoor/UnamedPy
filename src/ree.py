# coding=utf-8

import pygame
import pygame.gfxdraw
from pygame.locals import *


METHOD = "pygame"
TYPES = [
    QUIT,
    ACTIVEEVENT,
    KEYDOWN,
    KEYUP,
    MOUSEMOTION,
    MOUSEBUTTONUP,
    MOUSEBUTTONDOWN,
    JOYAXISMOTION,
    JOYBALLMOTION,
    JOYHATMOTION,
    JOYBUTTONUP,
    JOYBUTTONDOWN,
    VIDEORESIZE,
    VIDEOEXPOSE
]
ATTRIBS = [
    "gain",
    "state",
    "unicode",
    "key",
    "mod",
    "pos",
    "rel",
    "buttons",
    "button",
    "joy",
    "axis",
    "value",
    "ball",
    "rel",
    "hat",
    "value",
    "size",
    "w",
    "h",
    "code"
]

# consts
surf = pygame.Surface
rect = pygame.Rect
font = pygame.font.Font


class Event:
    def __init__(self, pg_event: pygame.event):
        self._ev = pg_event

    def __getattr__(self, item) -> object:
        if hasattr(self._ev, item):
            return self._ev.__getattribute__(item)
        raise AttributeError(str(item) + " not found in " + str(self._ev))

    def __eq__(self, other) -> bool:
        if not isinstance(other, tuple):
            if other in TYPES:
                return self._ev.type == other
        else:
            if other[0] in TYPES:
                for attr in ATTRIBS:
                    if hasattr(self._ev, attr):
                        tmp = self._ev.__getattribute__(attr)
                        if self._ev.type == other[0] and tmp == other[1]:
                            return True
        return False

    def __ne__(self, other) -> bool:
        return not self == other


def get_method() -> str:
    return METHOD


def init():
    return pygame.init()


def init_font():
    return pygame.font.init()


def init_mixer():
    return pygame.mixer.init()


def init_joystick():
    return pygame.joystick.init()


def count_joysticks() -> int:
    return pygame.joystick.get_count()


def create_joystick() -> pygame.joystick.Joystick:
    return pygame.joystick.Joystick(0)


def set_key_repeat(after: int, each: int):
    pygame.key.set_repeat(after, each)


def quit_():
    return pygame.quit()


def create_window(size: tuple, *flags) -> pygame.Surface:
    return pygame.display.set_mode(size, *flags)


def draw_rect(screen, rect: tuple, fgcolor: tuple, bgcolor: tuple=(0, 0, 0), width: int=0):
    pygame.draw.rect(screen, fgcolor, rect, width)


def load_image(path: str) -> pygame.Surface:
    return pygame.image.load(path).convert_alpha()


def load_sys_font(name: str, size: int) -> pygame.font.SysFont:
    return pygame.font.SysFont(name, size)


def load_font(path: str, size: int) -> pygame.font.Font:
    return pygame.font.Font(path, size)


def create_surface(*args) -> pygame.Surface:
    return pygame.Surface(*args)


def create_clock() -> pygame.time.Clock:
    return pygame.time.Clock()


def get_surface_class() -> pygame.Surface:
    return pygame.Surface


def flip():
    pygame.display.flip()


def rescale(image: object, size: tuple) -> pygame.Surface:
    return pygame.transform.scale(image, size)


def poll_event() -> Event:
    return Event(pygame.event.poll())


def get_event() -> list:
    return [Event(ev) for ev in pygame.event.get()]


def set_caption(caption: str=""):
    pygame.display.set_caption(caption)


def save_image(image: object, path: str):
    pygame.image.save(image, path)


def get_mouse_pos() -> tuple:
    return pygame.mouse.get_pos()


def get_rel_mouse_move() -> tuple:
    return pygame.mouse.get_rel()


def set_mouse_visible(visible: bool=True):
    pygame.mouse.set_visible(visible)


def set_mouse_pos(new_x: int, new_y: int):
    pygame.mouse.set_pos(new_x, new_y)


def get_key_name(key: int) -> str:
    return pygame.key.name(key)


def load_music_object(path: str) -> pygame.mixer.Sound:
    return pygame.mixer.Sound(path)


def load_music(path: str):
    pygame.mixer.music.load(path)


def play_music(loops: int=-1):
    pygame.mixer.music.play(loops=loops)


def stop_music():
    pygame.mixer.music.stop()


def fadeout_music(value: float):
    pygame.mixer.music.fadeout(value)


def is_mixer_busy() -> bool:
    return pygame.mixer.get_busy()


def create_rect(x: int, y: int, w: int, h: int) -> pygame.Rect:
    return pygame.Rect(x, y, w, h)


def get_alpha_channel() -> int or float:
    return pygame.SRCALPHA


def gfxdraw_filled_circle(image, x, y, r, color):
    pygame.gfxdraw.filled_circle(image, x, y, r, color)