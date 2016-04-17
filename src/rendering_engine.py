# coding=utf-8

try:
    import pygame
except ImportError:
    try:
        import sfml as sf
    except ImportError:
        print("Impossible de charger une lib graphique")
    else:
        METHOD = "pysfml"
else:
    METHOD = "pygame"


"""
Disponnibles :
    * pysfml (pas encore supporté totalement)
    * opengl (pas encore supporté, why not ?)
    * pygame (actuellement utilisé)
"""
_window = None


def init():
    if METHOD == "pygame":
        return pygame.init()
    if METHOD == "pysfml":
        return 0, 0


def init_font():
    if METHOD == "pygame":
        return pygame.font.init()
    if METHOD == "pysfml":
        pass


def init_mixer():
    if METHOD == "pygame":
        return pygame.mixer.init()
    if METHOD == "pysfml":
        return


def init_joystick():
    if METHOD == "pygame":
        return pygame.joystick.init()
    if METHOD == "pysfml":
        pass


def count_joysticks() -> int:
    if METHOD == "pygame":
        return pygame.joystick.get_count()
    if METHOD == "pysfml":
        pass


def create_joystick() -> object:
    if METHOD == "pygame":
        return pygame.joystick.Joystick(0)
    if METHOD == "pysfml":
        pass


def set_key_repeat(after: int, each: int):
    if METHOD == "pygame":
        pygame.key.set_repeat(after, each)
    if METHOD == "pysfml":
        pass


def quit_():
    if METHOD == "pygame":
        return pygame.quit()
    if METHOD == "pysfml":
        return _window.close()


def create_window(size: tuple, *flags) -> object:
    global _window
    if METHOD == "pygame":
        _window = pygame.display.set_mode(size, *flags)
    if METHOD == "pysfml":
        _window = sf.RenderWindow(sf.VideoMode(*size), "")
    return _window


def draw_rect(screen, rect: tuple, fgcolor: tuple, bgcolor: tuple=(0, 0, 0), width: int=0):
    if METHOD == "pygame":
        pygame.draw.rect(screen, fgcolor, rect, width)
    if METHOD == "pysfml":
        pass


def load_image(path: str) -> object:
    if METHOD == "pygame":
        return pygame.image.load(path).convert_alpha()
    if METHOD == "pysfml":
        pass


def load_sys_font(name: str, size: int) -> object:
    if METHOD == "pygame":
        return pygame.font.SysFont(name, size)
    if METHOD == "pysfml":
        pass


def load_font(path: str, size: int) -> object:
    if METHOD == "pygame":
        return pygame.font.Font(path, size)
    if METHOD == "pysfml":
        pass


def create_surface(*args) -> object:
    if METHOD == "pygame":
        return pygame.Surface(*args)
    if METHOD == "pysfml":
        pass


def create_clock() -> object:
    if METHOD == "pygame":
        return pygame.time.Clock()
    if METHOD == "pysfml":
        pass


def get_surface_class() -> object:
    if METHOD == "pygame":
        return pygame.Surface
    if METHOD == "pysfml":
        pass


def flip():
    if METHOD == "pygame":
        pygame.display.flip()
    if METHOD == "pysfml":
        _window.display()


def rescale(image: object, size: tuple) -> object:
    if METHOD == "pygame":
        return pygame.transform.scale(image, size)
    if METHOD == "pysfml":
        pass


def poll_event() -> object:
    if METHOD == "pygame":
        return pygame.event.poll()
    if METHOD == "pysfml":
        pass


def get_event() -> list:
    if METHOD == "pygame":
        return pygame.event.get()
    if METHOD == "pysfml":
        return _window.events


def set_caption(caption: str=""):
    if METHOD == "pygame":
        pygame.display.set_caption(caption)
    if METHOD == "pysfml":
        _window.title = caption


def save_image(image: object, path: str):
    if METHOD == "pygame":
        pygame.image.save(image, path)
    if METHOD == "pysfml":
        pass


def get_mouse_pos() -> tuple:
    if METHOD == "pygame":
        return pygame.mouse.get_pos()
    if METHOD == "pysfml":
        pass


def get_rel_mouse_move() -> tuple:
    if METHOD == "pygame":
        return pygame.mouse.get_rel()
    if METHOD == "pysfml":
        pass


def set_mouse_visible(visible: bool=True):
    if METHOD == "pygame":
        pygame.mouse.set_visible(visible)
    if METHOD == "pysfml":
        pass


def set_mouse_pos(new_x: int, new_y: int):
    if METHOD == "pygame":
        pygame.mouse.set_pos(new_x, new_y)
    if METHOD == "pysfml":
        pass


def get_key_name(key: int) -> str:
    if METHOD == "pygame":
        return pygame.key.name(key)
    if METHOD == "pysfml":
        return


def load_music_object(path: str) -> object:
    if METHOD == "pygame":
        return pygame.mixer.Sound(path)
    if METHOD == "pysfml":
        return


def load_music(path: str):
    if METHOD == "pygame":
        pygame.mixer.music.load(path)
    if METHOD == "pysfml":
        pass


def play_music(loops: int=-1):
    if METHOD == "pygame":
        pygame.mixer.music.play(loops=loops)
    if METHOD == "pysfml":
        pass


def stop_music():
    if METHOD == "pygame":
        pygame.mixer.music.stop()
    if METHOD == "pysfml":
        pass


def fadeout_music(value: float):
    if METHOD == "pygame":
        pygame.mixer.music.fadeout(value)
    if METHOD == "pysfml":
        pass


def is_mixer_busy() -> bool:
    if METHOD == "pygame":
        return pygame.mixer.get_busy()
    if METHOD == "pysfml":
        return


def create_rect(x: int, y: int, w: int, h: int) -> object:
    if METHOD == "pygame":
        return pygame.Rect(x, y, w, h)
    if METHOD == "pysfml":
        return


def get_alpha_channel():
    if METHOD == "pygame":
        return pygame.SRCALPHA
    if METHOD == "pysfml":
        return