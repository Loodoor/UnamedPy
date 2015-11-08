# coding=utf-8

import pygame


class BaseAnimator:
    def __init__(self, base_image: pygame.Surface, velocity: float):
        self.base_image = base_image
        self.velocity = velocity
        self.decalage = int(self.base_image.get_width() // self.velocity + 1)
        self.output = []
        self.time = 0

    def load(self):
        for i in range(self.decalage):
            self.surf = pygame.Surface((30, 30))
            self.surf.fill((76, 76, 76))
            self.surf.set_colorkey((76, 76, 76))

            self.surf.blit(self.base_image, (self.time - self.base_image.get_width(), 0))
            self.surf.blit(self.base_image, (self.time, 0))

            self.surf.convert_alpha()

            self.time += self.velocity
            self.time %= self.base_image.get_width()
            self.output.append(self.surf)

    def draw_at(self, ecran: pygame.Surface, pos: tuple=(-1, -1)):
        self.time += self.velocity
        ecran.blit(self.output[int(self.time % len(self.output))], pos)