# coding=utf-8

import pygame
from exceptions import ListePleine
import glob
from time import time
from constantes import *


class BaseSideAnimator:
    def __init__(self, base_image: pygame.Surface, velocity: float, vertical: bool):
        self.base_image = base_image
        self.velocity = velocity
        self.decalage = int(self.base_image.get_width() // self.velocity + 1)
        self.output = []
        self.time = 0
        self.vertical = vertical

    def load(self):
        if self.output:
            raise ListePleine

        time = 0
        for i in range(self.decalage):
            surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            surf.fill((76, 76, 76))
            surf.set_colorkey((76, 76, 76))

            if not self.vertical:
                surf.blit(self.base_image, (time - self.base_image.get_width(), 0))
                surf.blit(self.base_image, (time, 0))
            else:
                surf.blit(self.base_image, (0, time - self.base_image.get_height()))
                surf.blit(self.base_image, (0, time))

            surf.convert_alpha()

            time += self.velocity
            time %= self.base_image.get_width()
            self.output.append(surf)

    def _draw(self):
        self.time += self.velocity

    def draw_at(self, ecran: pygame.Surface, pos: tuple=(-1, -1)):
        ecran.blit(self.output[int(self.time % len(self.output))], pos)


class BaseMultipleSpritesAnimator:
    def __init__(self, path: str, wait: float=0.0):
        self.path = path
        self.anims = []
        self._wait = wait
        self._cur_anim = 0
        self._max_anim = 0
        self._last_time = 0

        self._create_anims()

    def next(self):
        if self._last_time + self._wait <= time():
            self._cur_anim += 1
            self._cur_anim %= self._max_anim

            self._last_time = time()

    def get_anim(self):
        return self.anims[self._cur_anim]

    def _create_anims(self):
        for img in glob.glob(os.path.join(self.path, "*.png")):
            self.anims.append(pygame.image.load(img).convert_alpha())
            self._max_anim += 1


class FluidesAnimator(BaseSideAnimator):
    def __init__(self, base_image: pygame.Surface, velocity: float):
        super().__init__(base_image, velocity, False)

    def next(self):
        self._draw()

    def get_anim(self):
        return self.output[int(self.time % len(self.output))]


class PlayerAnimator:
    def __init__(self, path: str):
        self.path = path
        self.anims = {}
        self._cur_anim = PAUSE
        self._correspondances = {
            PAUSE: ANIM1,
            ANIM1: ANIM2,
            ANIM2: ANIM1
        }

        self._create_anims()

    def pause(self):
        self._cur_anim = PAUSE

    def next(self):
        self._cur_anim += 1

    def get_anim_cursor(self):
        return self._cur_anim % 3

    def get_sprite(self, direc: int, anim_curs: int):
        if direc in self.anims.keys():
            if anim_curs < len(self.anims):
                return self.anims[direc][anim_curs]

    def get_sprite_from_dir(self, direc: int):
        if direc in self.anims.keys():
            return self.anims[direc][self.get_anim_cursor()]

    def _create_anims(self):
        lhaut = [pygame.image.load(_).convert_alpha() for _ in glob.glob(os.path.join(self.path, "haut*.png"))]
        lbas = [pygame.image.load(_).convert_alpha() for _ in glob.glob(os.path.join(self.path, "bas*.png"))]
        lgauche = [pygame.image.load(_).convert_alpha() for _ in glob.glob(os.path.join(self.path, "gauche*.png"))]
        ldroite = [pygame.image.load(_).convert_alpha() for _ in glob.glob(os.path.join(self.path, "droite*.png"))]

        self.anims = {
            HAUT: lhaut,
            BAS: lbas,
            GAUCHE: lgauche,
            DROITE: ldroite
        }