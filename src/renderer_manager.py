# coding=utf-8

from constantes import *


class RendererManager:
    def __init__(self):
        self.current_renderer = RENDER_GAME
        self.queue = []
        self.forbidden_renderers = []

    def can_i_render(self):
        return True if self.current_renderer not in self.forbidden_renderers else False

    def clear_all(self):
        self.queue = []
        self.current_renderer = RENDER_GAME

    def ban_renderer(self, *renderers: list):
        for renderer in renderers:
            self.forbidden_renderers.append(renderer)

    def get_renderer(self):
        return self.current_renderer

    def change_renderer_for(self, new_renderer: int):
        self.queue.append(self.current_renderer)
        self.current_renderer = new_renderer

    def change_without_logging(self, new_renderer: int):
        self.current_renderer = new_renderer

    def change_for_last_renderer(self):
        self.current_renderer = self.queue.pop()

    def invert_renderer(self):
        tmp = self.current_renderer
        self.current_renderer = self.queue[-1]
        self.queue.append(tmp)