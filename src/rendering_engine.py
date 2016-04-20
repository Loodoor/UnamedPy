# coding=utf-8

import pygame
import pygame.gfxdraw
import pygame.locals


METHOD = "pygame"
TYPES = [
    pygame.locals.QUIT,
    pygame.locals.ACTIVEEVENT,
    pygame.locals.KEYDOWN,
    pygame.locals.KEYUP,
    pygame.locals.MOUSEMOTION,
    pygame.locals.MOUSEBUTTONUP,
    pygame.locals.MOUSEBUTTONDOWN,
    pygame.locals.JOYAXISMOTION,
    pygame.locals.JOYBALLMOTION,
    pygame.locals.JOYHATMOTION,
    pygame.locals.JOYBUTTONUP,
    pygame.locals.JOYBUTTONDOWN,
    pygame.locals.VIDEORESIZE,
    pygame.locals.VIDEOEXPOSE
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


class Event:
    def __init__(self, pg_event: pygame.event):
        self._ev = pg_event

    def __getattr__(self, item) -> object:
        if hasattr(self._ev, item):
            return self._ev.__getattribute__(item)
        raise AttributeError(str(item) + " not found in " + str(self._ev))

    def __cmp__(self, other) -> bool:
        if not isinstance(other, tuple):
            if other in TYPES:
                return self._ev.type == other
        else:
            if other[0] in TYPES:
                tmp = None
                for attr in ATTRIBS:
                    if hasattr(self._ev, attr):
                        tmp = self._ev.__getattr__(attr)
                        break
                if tmp:
                    return self._ev.type == other[0] and tmp == other[1]
        return False


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
    if METHOD == "pygame":
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