import os
import pygame
from pygame.locals import *
from constantes import *
import pickle
import objets_manager


class Inventaire:
    def __init__(self, ecran, police):
        self.ecran = ecran
        self.police = police

        self.cur_categorie = POCHE_COMMUNS
        self.selected_item = -1

        #Objets
        self.objets = [
            [objets_manager.Objet("Test", "Je suis un test !", [10, 10], objets_manager.ObjectAction(print, "Salut ! Le test fonctionne chef !"))],  # Poche communs
            [],  # Poche capturateurs
            [],  # Poche médicaments
            [],  # Poche Objets Rares
            []   # Poche CT/CS
        ]

    def update(self):
        self.render()

    def render(self):
        pygame.draw.rect(self.ecran, (50, 180, 70), (20, 20, INVENT_X_SIZE, INVENT_Y_SIZE))
        self.ecran.blit(self.police.render("Inventaire", 1, (10, 10, 10)), (FEN_large // 2, 30))
        for i in range(len(self.objets[self.cur_categorie])):
            texte = self.objets[self.cur_categorie][i].name() + ' : ' + str(self.objets[self.cur_categorie][i].tot_quantite())
            item = self.police.render(texte, 1, (10, 10, 10))
            self.ecran.blit(item, (INVENT_X_ITEM, INVENT_Y_ITEM + i * INVENT_ESP_ITEM))
        if self.selected_item != -1:
            pygame.draw.rect(self.ecran, (180, 50, 75), (INVENT_BTN_JETER_X, INVENT_BTN_JETER_Y, INVENT_SIZE_BTN_X, INVENT_SIZE_BTN_Y))

    def clic(self, xp, yp):
        real_y = (yp - INVENT_Y_ITEM) // INVENT_ESP_ITEM
        if INVENT_X_ITEM <= xp <= INVENT_MAX_X_ITEM:
            if 0 <= real_y <= len(self.objets[self.cur_categorie]):
                self.selected_item = real_y
            else:
                self.selected_item = -1
        elif INVENT_BTN_JETER_Y <= yp <= INVENT_BTN_JETER_Y + INVENT_SIZE_BTN_Y and \
                    INVENT_BTN_JETER_X <= xp <= INVENT_BTN_JETER_X + INVENT_SIZE_BTN_X:
                self.jeter(real_y)
        else:
            self.selected_item = -1

    def next(self):
        self.cur_categorie = self.cur_categorie + 1 if self.cur_categorie + 1 < len(self.objets) else 0

    def previous(self):
        self.cur_categorie = self.cur_categorie - 1 if self.cur_categorie - 1 >= 0 else len(self.objets) - 1

    def jeter(self, item: int):
        self.objets[self.cur_categorie][item].jeter()

    def load(self):
        if os.path.exists(os.path.join("..", "saves", "inventaire" + EXTENSION)):
            with open(os.path.join("..", "saves", "inventaire" + EXTENSION), "rb") as read_inventaire:
                self.objets = pickle.Unpickler(read_inventaire).load()

    def save(self):
        with open(os.path.join("..", "saves", "inventaire" + EXTENSION), "wb") as wrb_inventaire:
            pickle.Pickler(wrb_inventaire).dump(self.objets)