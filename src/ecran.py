# coding=utf-8

import pygame
from constantes import *


class MyScreen(pygame.Surface):
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface.get_size())
        self._surface = surface
        self._original = self._surface
        self._bw = False
        self._converted = {}

    @staticmethod
    def _set_to_bw(surface: pygame.Surface) -> pygame.Surface:
        surface.lock()
        for pixel in range(surface.get_width() * surface.get_height()):
            x, y = pixel // surface.get_height(), pixel % surface.get_height()
            try:
                last_color = surface.get_at((x, y))
                f = int(0.299 * last_color.r + 0.587 * last_color.g + 0.114 * last_color.b)
                new_color = pygame.Color(f, f, f, last_color.a)
                surface.set_at((x, y), new_color)
            except IndexError:
                print("[!] Essaie de modification d'un pixel trop lointain ...")
                sys.exit(0)
        surface.unlock()

        return surface

    def set_bw(self, bw: bool):
        self._bw = bw
        if bw:
            self._surface = MyScreen._set_to_bw(self._surface)
            self._original = self._surface
            print(">> En activant cette fonctionnalité, il est fort possible que le jeu vienne à ralentir !")
        else:
            self._surface = self._original

    def blit(self, new: pygame.Surface, at: tuple=(0, 0)):
        if self._bw:
            if new not in self._converted.keys():
                tmp = new
                new = MyScreen._set_to_bw(new)
                self._converted[tmp] = new
                del tmp
            self._surface.blit(self._converted[new], at)
        else:
            self._surface.blit(new, at)
        self._original = self._surface