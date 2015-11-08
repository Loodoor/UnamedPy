# coding=utf-8

from constantes import *


class RendererManager:
    def __init__(self):
        self.current_renderer = RENDER_GAME
        self.queue = []

    def clear_all(self):
        self.queue = []
        self.current_renderer = RENDER_GAME

    def get_renderer(self):
        return self.current_renderer

    def change_renderer_for(self, new_renderer: int):
        self.queue.append(self.current_renderer)
        self.current_renderer = new_renderer

    def change_for_last_renderer(self):
        self.current_renderer = self.queue.pop(-1)

    def invert_renderer(self):
        tmp = self.current_renderer
        self.current_renderer = self.queue[-1]
        self.queue.append(tmp)