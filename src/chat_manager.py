# coding=utf-8

import pygame
from constantes import *

import textentry


class ChatManager:
    def __init__(self, ecran: pygame.Surface):
        self.ecran = ecran
        self.stack = []
        self.text_entry = textentry.TextBox(self.ecran, x=CHAT_X_BOX, y=CHAT_Y_BOX,
                                            sx=CHAT_SX_BOX, sy=CHAT_SY_BOX, bgcolor=(70, 70, 70))

    def update(self):
        if self.text_entry.is_running():
            self.render()
        self.new_message(self.text_entry.get_text())
        self.text_entry.reinit()

    def is_running(self):
        return self.text_entry.is_running()

    def event(self, e: pygame.event):
        self.text_entry.event(e)

    def new_message(self, msg: str):
        self.stack.append(msg)

    def render(self):
        self.text_entry.render()