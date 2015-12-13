# coding=utf-8

import pygame
from pygame.locals import *


class TextBox:
    def __init__(self, window: pygame.Surface, **kwargs):
        """
        args :
            font            (default : pygame.font.SysFont("arial", 18))
            max_length      (default : 32)
            color           (default : (255, 255, 255))
            x               (default : 0)
            y               (default : 0)
            sx              (default : 120)
            sy              (default : 35)
            bgcolor         (default : (0, 0, 0))
        """
        self.window = window
        self.input = ""
        self.running = False

        self.font = kwargs.get("font", pygame.font.SysFont("arial", 18))
        self.max_length = kwargs.get("max_length", 32)
        self.color = kwargs.get("color", (255, 255, 255))
        self.pos_x = kwargs.get("x", 0)
        self.pos_y = kwargs.get("y", 0)
        self.sx = kwargs.get("sx", 120)
        self.sy = kwargs.get("sy", 35)
        self.bg_color = kwargs.get("bgcolor", (0, 0, 0))

    def event(self, e: pygame.event):
        if e.type == QUIT:
            self.running = False
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE or e.key == K_RETURN:
                self.running = False
            elif e.key == K_BACKSPACE:
                self.input = self.input[:-1]
            elif len(self.input) < self.max_length:
                self.input += e.unicode

    def render(self):
        pygame.draw.rect(self.window, self.bg_color, (self.pos_x, self.pos_y, self.sx, self.sy))
        texte = self.font.render(self.input, 1, self.color)
        text_width = texte.get_width()
        self.window.blit(texte, (self.pos_x - text_width // 2, self.pos_y))

    def mainloop(self):
        self.running = True

        while self.running:
            for event in pygame.event.get():
                self.event(event)

            self.render()
            pygame.display.flip()

    def is_running(self):
        return self.running

    def reinit(self):
        self.input = ""

    def get_text(self):
        #self.mainloop()

        return self.input