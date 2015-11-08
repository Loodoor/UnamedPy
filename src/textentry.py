# coding=utf-8

import pygame
from pygame.locals import *


class TextBox:
    def __init__(self, window, **kwargs):
        """
        args :
            font            (default : pygame.font.SysFont("arial", 18))
            max_length      (default : 32)
            color           (default : (255, 255, 255))
            x               (default : 0)
            y               (default : 0)
        """
        self.window = window
        self.input = ""
        self.running = False

        self.font = kwargs.get("font", pygame.font.SysFont("arial", 18))
        self.max_length = kwargs.get("max_length", 32)
        self.color = kwargs.get("color", (255, 255, 255))
        self.pos_x = kwargs.get("x", 0)
        self.pos_y = kwargs.get("y", 0)

    def _event(self, e):
        if e.type == QUIT:
            self.running = False
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE or e.key == K_RETURN:
                self.running = False
            elif e.key == K_BACKSPACE:
                self.input = self.input[:-1]
            elif len(self.input) < self.max_length:
                self.input += e.unicode

    def _render(self):
        texte = self.font.render(self.input, 1, self.color)
        text_width = texte.get_width()
        self.window.blit(texte, (self.pos_x + (- text_width) // 2, self.pos_y))

    def _mainloop(self):
        self.running = True

        while self.running:
            for event in pygame.event.get():
                self._event(event)

            self._render()
            pygame.display.flip()

    def get_text(self):
        self._mainloop()

        return self.input