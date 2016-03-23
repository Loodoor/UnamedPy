# coding=utf-8

import pygame

METHOD = "pygame"


def init():
    if METHOD == "pygame":
        return pygame.init()


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


def create_surface(*args) -> object:
    if METHOD == "pygame":
        return pygame.Surface(*args)


def get_surface_class() -> object:
    if METHOD == "pygame":
        return pygame.Surface


def flip():
    if METHOD == "pygame":
        pygame.display.flip()


def rescale(image: object, size: tuple) -> object:
    if METHOD == "pygame":
        return pygame.transform.scale(image, size)