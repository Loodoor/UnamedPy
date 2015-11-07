import pygame
import os
from pygame.locals import *
from creatures_mgr import Creature
import pickle
from constantes import *


class ComputerManager:
    def __init__(self, ecran: pygame.Surface, police: pygame.font.SysFont, max_size=PC_MAX_CREA):
        self.ecran = ecran
        self.police = police
        self.storage = []
        self.max_size = max_size
        self.path = os.path.join("..", "saves", "pc" + EXTENSION)
        self.current_page = 0
        self.per_page = 7

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "rb") as pc_rb:
                self.storage = pickle.Unpickler(pc_rb).load()

    def save(self):
        with open(self.path, "wb") as pc_wb:
            pickle.Pickler(pc_wb).dump(self.storage)

    def update(self):
        self.render()

    def next(self):
        self.current_page = self.current_page + 1 if self.current_page < MAX_CREATURES // 7 else self.current_page

    def previous(self):
        self.current_page = self.current_page - 1 if self.current_page > 0 else self.current_page

    def render(self):
        pygame.draw.rect(self.ecran, (180, 50, 50), (FCREA_X, FCREA_Y, FCREA_SIZE_X, FCREA_SIZE_Y))
        for i in range(len(self.storage[self.current_page:self.current_page + self.per_page])):
            creature = self.storage[i]
            pvs_format = self.police.render(str(creature.get_pvs()) + '/' + str(creature.get_max_pvs()), 1,
                                            (10, 10, 10))
            txt_format = self.police.render(creature.get_pseudo() + ' : niv.' + str(creature.get_niv()), 1,
                                            (10, 10, 10))
            pygame.draw.rect(self.ecran, (50, 180, 50), (FCREA_X + FCREA_MARGE_X,
                                                         FCREA_Y + FCREA_SIZE_Y_CASE * i + FCREA_MARGE_Y * (i + 1),
                                                         FCREA_SIZE_X_CASE,
                                                         FCREA_SIZE_Y_CASE))
            self.ecran.blit(txt_format,
                            (FCREA_X + FCREA_MARGE_X + FCREA_MARGE_TXT_X,
                             FCREA_Y + FCREA_SIZE_Y_CASE * i + FCREA_MARGE_Y * (i + 1) + FCREA_MARGE_TXT_Y))
            self.ecran.blit(pvs_format,
                            (FCREA_X + FCREA_MARGE_X + FCREA_MARGE_TXT_X,
                             FCREA_Y + FCREA_SIZE_Y_CASE * i + FCREA_MARGE_Y * (i + 1) + FCREA_MARGE_TXT_Y2))
        # boutons previous et next
        pygame.draw.rect(self.ecran, (180, 50, 180), (FCREA_PREVIOUS_X, FCREA_PREVIOUS_Y))

    def move_creature_to_equipe(self, which: int, equipe):
        if equipe.add_creature(self.storage[which]):
            self.pop_creature(which)

    def add_creature(self, new: Creature):
        if len(self.storage) < self.max_size:
            self.storage.append(new)
            return True
        return False

    def get_creature(self, index: int):
        return self.storage[index] if 0 <= index < len(self.storage) else PC_GET__ERROR

    def pop_creature(self, index: int):
        return self.storage.pop(index) if 0 <= index < len(self.storage) else PC_POP__ERROR