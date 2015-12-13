# coding=utf-8

import pygame
from pygame.locals import *

import textentry
from constantes import *
from network_event_listener import NetworkEventsListener


class ChatManager:
    def __init__(self, ecran: pygame.Surface, font: pygame.font.SysFont, reseau_mgr: NetworkEventsListener,
                 pseudo: str, rang: int):
        self.ecran = ecran
        self.font = font
        self.reseau_mgr = reseau_mgr
        self.pseudo = pseudo
        self.rang = rang
        self.stack = []
        self.text_entry = textentry.TextBox(self.ecran, x=CHAT_X_BOX, y=CHAT_Y_BOX,
                                            sx=CHAT_SX_BOX, sy=CHAT_SY_BOX, bgcolor=(70, 70, 70))
        self.quit = None

    def update_quit_event(self, new):
        self.quit = new

    def update(self):
        self.render()

        if not self.text_entry.type_enter():
            self.text_entry.render()
        else:
            self.reseau_mgr.chat_message(self.text_entry.get_text(), self.pseudo, self.rang)
            self.new_message(self.text_entry.get_text())
            self.text_entry.reset()

    def network_fetch_messages(self):
        self.stack = self.reseau_mgr.get_chat_messages()

    def get_messages(self):
        if self.reseau_mgr.is_enabled():
            pass
        return self.stack[::-1]

    def update_name(self, new_name: str):
        self.pseudo = new_name

    def update_rang(self, new_rang: int):
        self.rang = new_rang

    def is_running(self):
        return self.text_entry.is_running()

    def event(self, e: pygame.event):
        if e.type == KEYDOWN and e.key != self.quit:
            self.text_entry.event(e)

    def new_message(self, msg: str):
        self.stack += [
            {
                "message": self.pseudo + " : " + msg,
                "rang": self.rang
            }
        ]

    def render(self):
        pygame.draw.rect(self.ecran, (50, 180, 180), (CHAT_X_MESSAGES, CHAT_Y_MESSAGES,
                                                      CHAT_SX, CHAT_SY))
        i = 0
        color = (255, 255, 255)
        for msg in self.get_messages():
            if msg["rang"] == RANG_ADMIN:
                color = CHAT_COULEUR_ADMIN
            if msg["rang"] == RANG_MODO:
                color = CHAT_COULEUR_MODO
            if msg["rang"] == RANG_JOUEUR:
                color = CHAT_COULEUR_JOUEUR
            self.ecran.blit(self.font.render(msg["message"], 1, color),
                            (CHAT_X_MESSAGES, CHAT_Y_MESSAGES + i * CHAT_SY_MESSAGE))
            i += 1