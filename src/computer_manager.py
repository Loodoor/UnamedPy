# coding=utf-8

import pygame
from pygame.locals import *
from creatures_mgr import Creature
import pickle
from constantes import *
import os


class ComputerManager:
    def __init__(self, ecran: pygame.Surface, police: pygame.font.SysFont, render_manager, max_size=PC_MAX_CREA):
        self.ecran = ecran
        self.police = police
        self.storage = []
        self.max_size = max_size
        self.path = os.path.join("..", "saves", "pc" + EXTENSION)
        self.current_page = 0
        self.per_page = 7
        self.titre = self.police.render("PC", POL_ANTIALISING, (255, 255, 255))
        self.rd_mgr = render_manager
        self.selected_crea = -1
        self.equipe = None
        self.fond = pygame.image.load(os.path.join("..", "assets", "gui", "fd_creatures.png")).convert_alpha()
        self._fond_case = pygame.image.load(os.path.join("..", "assets", "gui", "fd_case_creature.png")).convert_alpha()
        self._fond_case_selected = pygame.image.load(os.path.join("..", "assets", "gui", "fd_case_creature_selected.png")).convert_alpha()
        self._btn_next = pygame.image.load(os.path.join("..", "assets", "gui", "fd_bouton_next.png")).convert_alpha()
        self._btn_previous = pygame.image.load(os.path.join("..", "assets", "gui", "fd_bouton_previous.png")).convert_alpha()
        self._btn_creatures = pygame.image.load(os.path.join("..", "assets", "gui", "fd_bouton_poche_creatures.png")).convert_alpha()
        self._btn_to_creatures = pygame.image.load(os.path.join("..", "assets", "gui", "fd_bouton_to_poche_creatures.png")).convert_alpha()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "rb") as pc_rb:
                self.storage = pickle.Unpickler(pc_rb).load()

    def save(self):
        with open(self.path, "wb") as pc_wb:
            pickle.Pickler(pc_wb).dump(self.storage)

    def add_equipe(self, new_equipe):
        self.equipe = new_equipe

    def update(self):
        self.render()

    def change_renderer(self):
        self.rd_mgr.change_without_logging_last(RENDER_CREATURES)

    def clic(self, xp: int, yp: int):
        if FCREA_PREVIOUS_X <= xp <= FCREA_PREVIOUS_X + FCREA_BTN_SX and FCREA_PREVIOUS_Y <= yp <= FCREA_PREVIOUS_Y + FCREA_BTN_SY:
            self.previous()
        if FCREA_NEXT_X <= xp <= FCREA_NEXT_X + FCREA_BTN_SX and FCREA_NEXT_Y <= yp <= FCREA_NEXT_Y + FCREA_BTN_SY:
            self.next()
        if FCREA_AUTRE_MGR_X <= xp <= FCREA_AUTRE_MGR_X + FCREA_AUTRE_MGR_SX and FCREA_AUTRE_MGR_Y <= yp <= FCREA_AUTRE_MGR_Y + FCREA_AUTRE_MGR_SY:
            self.change_renderer()
        if FCREA_PASSE_CREA_TO__X <= xp <= FCREA_PASSE_CREA_TO__X + FCREA_PASSE_CREA_TO__SX and \
                FCREA_PASSE_CREA_TO__Y <= yp <= FCREA_PASSE_CREA_TO__Y + FCREA_PASSE_CREA_TO__SY:
            if self.selected_crea != -1:
                self.move_creature_to_equipe(self.selected_crea)
        if FCREA_X <= xp <= FCREA_X + FCREA_SIZE_X_CASE and FCREA_Y + FCREA_IMAGE_XY_MARGE <= yp <= \
                FCREA_Y + FCREA_IMAGE_XY_MARGE + FCREA_SIZE_Y_CASE * len(self.storage) + FCREA_MARGE_Y * \
                (len(self.storage[self.current_page:self.current_page + self.per_page]) + 1) + FCREA_MARGE_Y_RAPPORT_TITRE:
            real_y = yp - FCREA_Y - FCREA_IMAGE_XY_MARGE - FCREA_MARGE_Y_RAPPORT_TITRE
            real_y /= (FCREA_SIZE_Y_CASE + FCREA_MARGE_Y)
            real_y = int(real_y)
            if 0 <= real_y < len(self.storage):
                self.selected_crea = real_y + self.current_page * self.per_page

    def next(self):
        self.current_page = self.current_page + 1 if self.current_page < MAX_CREATURES // 7 else self.current_page

    def previous(self):
        self.current_page = self.current_page - 1 if self.current_page > 0 else self.current_page

    def move_locals_creatures(self, first: int, second: int):
        self.storage[first], self.storage[second] = self.storage[second], self.storage[first]

    def render(self):
        self.ecran.blit(self.fond, (FCREA_X, FCREA_Y))
        self.ecran.blit(self.titre, ((FEN_large - self.titre.get_width()) // 2, FCREA_TITRE_Y))
        for i in range(len(self.storage[self.current_page:self.current_page + self.per_page])):
            creature = self.storage[i + self.current_page * self.per_page]
            pvs_format = self.police.render(str(creature.get_pvs()) + '/' + str(creature.get_max_pvs()), POL_ANTIALISING,
                                            (10, 10, 10))
            txt_format = self.police.render(creature.get_pseudo() + ' : niv.' + str(creature.get_niv()), POL_ANTIALISING,
                                            (10, 10, 10))
            if i == self.selected_crea:
                self.ecran.blit(self._fond_case_selected, (FCREA_X + FCREA_MARGE_X, FCREA_Y + FCREA_SIZE_Y_CASE * i + FCREA_MARGE_Y * (i + 1) + FCREA_MARGE_Y_RAPPORT_TITRE))
            else:
                self.ecran.blit(self._fond_case, (FCREA_X + FCREA_MARGE_X, FCREA_Y + FCREA_SIZE_Y_CASE * i + FCREA_MARGE_Y * (i + 1) + FCREA_MARGE_Y_RAPPORT_TITRE))
            self.ecran.blit(txt_format,
                            (FCREA_X + FCREA_MARGE_X + FCREA_MARGE_TXT_X,
                             FCREA_Y + FCREA_SIZE_Y_CASE * i + FCREA_MARGE_Y * (i + 1) + FCREA_MARGE_TXT_Y +
                             FCREA_MARGE_Y_RAPPORT_TITRE))
            self.ecran.blit(pvs_format,
                            (FCREA_X + FCREA_MARGE_X + FCREA_MARGE_TXT_X,
                             FCREA_Y + FCREA_SIZE_Y_CASE * i + FCREA_MARGE_Y * (i + 1) + FCREA_MARGE_TXT_Y2 +
                             FCREA_MARGE_Y_RAPPORT_TITRE))
            # image de la créature
            self.ecran.blit(creature.get_image_with_size((FCREA_IMAGE_SX, FCREA_IMAGE_SY)),
                            (FCREA_X + FCREA_IMAGE_X + FCREA_IMAGE_XY_MARGE,
                             FCREA_Y + FCREA_IMAGE_Y + (
                                 i + 1) * FCREA_MARGE_Y + i * FCREA_SIZE_Y_CASE + FCREA_MARGE_Y_RAPPORT_TITRE - FCREA_IMAGE_XY_MARGE))
        # boutons previous et next
        self.ecran.blit(self._btn_next, (FCREA_NEXT_X, FCREA_NEXT_Y))
        self.ecran.blit(self._btn_previous, (FCREA_PREVIOUS_X, FCREA_PREVIOUS_Y))

        self.ecran.blit(self._btn_creatures, (FCREA_AUTRE_MGR_X, FCREA_AUTRE_MGR_Y))
        self.ecran.blit(self._btn_to_creatures, (FCREA_PASSE_CREA_TO__X, FCREA_PASSE_CREA_TO__Y))

    def move_creature_to_equipe(self, which: int):
        if self.equipe.add_creature(self.storage[which]):
            self.pop_creature(which)

    def add_creature(self, new: Creature):
        if len(self.storage) < self.max_size:
            self.storage.append(new)
            return True
        return False

    def get_creature(self, index: int):
        return self.storage[index] if 0 <= index < len(self.storage) else PC_GET__ERROR

    def get_all(self):
        return self.storage

    def get_selected_creature(self):
        if self.selected_crea != -1:
            return self.storage[self.selected_crea]
        raise ValueError("Impossible d'obtenir la créature demandée")

    def pop_creature(self, index: int):
        return self.storage.pop(index) if 0 <= index < len(self.storage) else PC_POP__ERROR