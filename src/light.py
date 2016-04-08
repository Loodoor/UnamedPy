import pygame
from pygame import gfxdraw
import random


class PreRenderedLight():
    def __init__(self, id_: int, pos: tuple, size: int, color: tuple, variation: int=0,
                 ambiantLight: int=176, threshold: float=12):
        self.lightID = id_
        self.lightPos = pos
        self.lightSize = size
        self.lightColor = color
        self.variation = variation
        self.imageList = []
        self.nbImages = 10
        self.indexBlit = 0
        self.ambiantLight = ambiantLight
        self.threshold = threshold
        self._t = 0
    
    def load(self):
        for number in range(0, self.nbImages):
            self.imageList.append(pygame.Surface((self.lightSize * 2 + self.variation, self.lightSize * 2 + self.variation), pygame.SRCALPHA, 32))
            self.imageList[number].convert_alpha()
            self.imageList[number].fill((0, 0, 0, 0))
        self._render()

    def move(self, pos):
        self.lightPos = pos
    
    def _render(self):
        for number in range(0, self.nbImages):
            maxRange = int(self.lightSize + random.random() * self.variation)
            for i in range(1, maxRange):
                r = self.lightColor[0] * (i / maxRange)
                g = self.lightColor[1] * (i / maxRange)
                b = self.lightColor[2] * (i / maxRange)
                t = int(255 - (self.ambiantLight * (i / maxRange)))
                # print("Color:", r, g, b, "Transparency:", t, "at", i)
                pygame.gfxdraw.filled_circle(
                    self.imageList[number],
                    int(self.lightSize + self.variation / 2),
                    int(self.lightSize + self.variation / 2),
                    maxRange - i,
                    (r, g, b, t)
                )

    def blit(self, surf, carte_mgr):
        xFillRect = self.lightPos[0] + carte_mgr.get_of1()
        yFillRect = self.lightPos[1] + carte_mgr.get_of2()

        if 0 <= xFillRect < surf.get_width() + self.imageList[self.indexBlit].get_width() and 0 <= yFillRect < surf.get_height() + self.imageList[self.indexBlit].get_height():
            surf.blit(self.imageList[self.indexBlit], (xFillRect, yFillRect))

        self._t += 1
        if self._t >= self.threshold:
            self._t = 0
            self.indexBlit += 1

        self.indexBlit %= self.nbImages