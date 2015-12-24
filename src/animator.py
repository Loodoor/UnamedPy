# coding=utf-8

import pygame
from exceptions import ListePleine
import glob
from constantes import *


class BaseAnimator:
    def __init__(self, base_image: pygame.Surface, velocity: float, vertical):
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
            surf = pygame.Surface((30, 30))
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


class FluidesAnimator(BaseAnimator):
    def __init__(self, base_image: pygame.Surface, velocity: float, where):
        super().__init__(base_image, velocity, False)
        self.where = where

    def draw(self, at: list, ecran: pygame.Surface, carte_mgr):
        self._draw()
        for elem in at:
            if carte_mgr.get_tile_code_at(elem[0], elem[1]) == self.where:
                self.draw_at(ecran, elem)


class PlayerAnimator:
    def __init__(self, path: str):
        self.path = path
        self.anims = []

        self._create_anims()

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