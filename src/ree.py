# coding=utf-8

import _pickle
import pygame
import pygame.gfxdraw
from pygame.locals import *
import pyfmodex as fmod
import os
import pickle


def warning(fonction):
    warning.already_affiche = []

    def wrapper(*args, **kwargs):
        if fonction.__name__ not in warning.already_affiche:
            print("[REE]", fonction.__name__, "est dangereux à utiliser")
        warning.already_affiche.append(fonction.__name__)
        return fonction(*args, **kwargs)
    return wrapper


def _diacritic(chain: str) -> str:
    return ''.join(c for c in chain if c not in [':', '/', ',', '?', '!', '.', ';', '*', '-', '+', ' '])


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
mask = pygame.mask.Mask
sound = fmod.sound.Sound

ssound = None


class _TmpBuffer:
    def __init__(self):
        self.items = {}

    def __call__(self, *args, **kwargs):
        self.items.update(*args, **kwargs)

    def __getitem__(self, item):
        return self.items[item]

    def __contains__(self, item):
        return item in self.__dict__


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


_buffer = _TmpBuffer()


def get_method() -> str:
    return METHOD


def init():
    global ssound
    pygame.mixer.pre_init(44100, -16, 2)
    try:
        ssound = fmod.System()
        ssound.init()
    except ValueError as e:
        print("[REE] Impossible de charger FMODEX\n[REE] - Err: %s" % e)
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


def load_image(path: str, normal_convert: bool=False) -> pygame.Surface:
    if not normal_convert:
        return pygame.image.load(path).convert_alpha()
    return pygame.image.load(path).convert()


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


def load_music_object(path: str="") -> sound:
    global ssound
    global _buffer

    try:
        if ssound:
            return ssound.create_sound(path)
        if os.path.exists(path) and path not in _buffer:
            try:
                print("(load_music_object) Attente ... Chargement de données lourdes sur %s" % path)
                _buffer(**{_diacritic(path): pygame.mixer.Sound(buffer=pickle.Unpickler(open(path, 'rb')).load())})
                return _buffer[_diacritic(path)]
            except (pygame.error, _pickle.UnpicklingError) as e:
                print("(load_music_object) Impossible de charger la musique à l'adresse : {}".format(path))
                print("(load_music_object) Fichier existant : {}".format(os.path.exists(path)))
                print("[REE] Err: %s" % e)
                return pygame.mixer.Sound(buffer=b"")
    except fmod.utils.FmodError as e:
        print("(load_music_object) Impossible de charger la musique à l'adresse : {}".format(path))
        print("(load_music_object) Fichier existant : {}".format(os.path.exists(path)))
        print("[REE] Err: %s" % e)
        if os.path.exists(path) and path not in _buffer:
            print("(load_music_object) Attente ... Chargement de données lourdes sur %s" % path)
            _buffer(**{_diacritic(path): pygame.mixer.Sound(buffer=pickle.Unpickler(open(path, 'rb')).load())})
        return _buffer[_diacritic(path)]


@warning
def load_music(path: str):
    try:
        pygame.mixer.music.load(path)
    except pygame.error as e:
        print("(load_music) Impossible de charger la musique à l'adresse : {}".format(path))
        print("(load_music_object) Fichier existant : {}".format(os.path.exists(path)))
        print("[REE] Err: %s" % e)


@warning
def play_music(loops: int=-1):
    try:
        pygame.mixer.music.play(loops=loops)
    except pygame.error as e:
        print("[REE] Err: %s" % e)


def stop_music(s: sound or pygame.mixer.Sound):
    global ssound
    if ssound:
        c = s.num_music_channels
        ssound.get_channel(c).stop()
    else:
        try:
            s.stop()
            pygame.mixer.stop()
        except pygame.error as e:
            print("[REE] Err: %s" % e)


@warning
def fadeout_music(value: float):
    if ssound:
        pass
    else:
        try:
            pygame.mixer.music.fadeout(value)
        except pygame.error as e:
            print("[REE] Err: %s" % e)


def is_mixer_busy() -> bool:
    if ssound:
        return fmod.get_disk_busy()
    return pygame.mixer.get_busy()


def create_rect(x: int, y: int, w: int, h: int) -> pygame.Rect:
    return pygame.Rect(x, y, w, h)


def get_alpha_channel() -> int or float:
    return pygame.SRCALPHA


def gfxdraw_filled_circle(image, x, y, r, color):
    pygame.gfxdraw.filled_circle(image, x, y, r, color)


def create_mask_from_surface(surface: surf) -> mask:
    return pygame.mask.from_surface(surface)


def collide_rect_with_mask(mask_: mask, rectangle: rect) -> bool:
    overlapper = mask((rectangle[2], rectangle[3]))
    c = mask_.overlap_mask(overlapper, (int(rectangle[0]), int(rectangle[1]))).count()
    return c