# coding=utf-8

import pygame

"""
Disponnibles :
    * pysfml (pas encore supporté)
    * opengl (pas encore supporté, why not ?)
    * pygame (actuellement utilisé)
"""
METHOD = "pygame"


def init():
    if METHOD == "pygame":
        return pygame.init()


def init_font():
    if METHOD == "pygame":
        return pygame.font.init()


def init_joystick():
    if METHOD == "pygame":
        return pygame.joystick.init()


def count_joysticks() -> int:
    if METHOD == "pygame":
        return pygame.joystick.get_count()


def create_joystick() -> object:
    if METHOD == "pygame":
        return pygame.joystick.Joystick(0)


def set_key_repeat(after: int, each: int):
    if METHOD == "pygame":
        pygame.key.set_repeat(after, each)


def quit_():
    if METHOD == "pygame":
        return pygame.quit()


def create_window(size: tuple, *flags) -> object:
    if METHOD == "pygame":
        return pygame.display.set_mode(size, *flags)


def draw_rect(screen, rect: tuple, fgcolor: tuple, bgcolor: tuple=(0, 0, 0), width: int=0):
    if METHOD == "pygame":
        pygame.draw.rect(screen, fgcolor, rect, width)


def load_image(path: str) -> object:
    if METHOD == "pygame":
        return pygame.image.load(path)


def load_sys_font(name: str, size: int) -> object:
    if METHOD == "pygame":
        return pygame.font.SysFont(name, size)


def load_font(path: str, size: int) -> object:
    if METHOD == "pygame":
        return pygame.font.Font(path, size)


def create_surface(*args) -> object:
    if METHOD == "pygame":
        return pygame.Surface(*args)


def create_clock() -> object:
    if METHOD == "pygame":
        return pygame.time.Clock()


def get_surface_class() -> object:
    if METHOD == "pygame":
        return pygame.Surface


def flip():
    if METHOD == "pygame":
        pygame.display.flip()


def rescale(image: object, size: tuple) -> object:
    if METHOD == "pygame":
        return pygame.transform.scale(image, size)


def poll_event() -> object:
    if METHOD == "pygame":
        return pygame.event.poll()


def get_event() -> object:
    if METHOD == "pygame":
        return pygame.event.get()


def set_caption(caption: str=""):
    if METHOD == "pygame":
        pygame.display.set_caption(caption)


def save_image(image: object, path: str):
    if METHOD == "pygame":
        pygame.image.save(image, path)


def get_mouse_pos() -> tuple:
    if METHOD == "pygame":
        return pygame.mouse.get_pos()


def get_rel_mouse_move() -> tuple:
    if METHOD == "pygame":
        return pygame.mouse.get_rel()


def set_mouse_visible(visible: bool=True):
    if METHOD == "pygame":
        pygame.mouse.set_visible(visible)


def set_mouse_pos(new_x: int, new_y: int):
    if METHOD == "pygame":
        pygame.mouse.set_pos(new_x, new_y)