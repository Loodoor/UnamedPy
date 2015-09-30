import pygame
import os
from pygame.locals import *
from creatures_mgr import Creature
import pickle
from constantes import *


class EquipeManager:
    def __init__(self, ecran: pygame.Surface, police: pygame.font.SysFont, size: int=6):
        self.size = size
        self.ecran = ecran
        self.police = police
        self.creatures = [
            Creature("Habalu", T_NORMAL, alea_niv=(5, 5), specs_range=(5, 12))
        ]
        self.path = os.path.join("..", "saves", "equipe" + EXTENSION)

    def update(self):
        self.render()

    def render(self):
        pygame.draw.rect(self.ecran, (180, 50, 50), (FCREA_X, FCREA_Y, FCREA_SIZE_X, FCREA_SIZE_Y))
        for i in range(len(self.creatures)):
            creature = self.creatures[i]
            pvs_format = self.police.render(str(creature.get_pvs()) + '/' + str(creature.get_max_pvs()), 1, (10, 10, 10))
            txt_format = self.police.render(creature.get_pseudo() + ' : niv.' + str(creature.get_niv()), 1, (10, 10, 10))
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

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "rb") as equipe_rb:
                self.creatures = pickle.Unpickler(equipe_rb).load()

    def save(self):
        with open(self.path, "wb") as equipe_wb:
            pickle.Pickler(equipe_wb).dump(self.creatures)

    def add_creature(self, new: Creature):
        if len(self.creatures) < self.size:
            self.creatures.append(new)

    def move_creature(self, first: int, second: int):
        ftmp = self.creatures[first]
        stmp = self.creatures[second]
        self.creatures[first] = stmp
        self.creatures[second] = ftmp

    def remove_creature(self, index: int):
        return self.creatures.pop(index)

    def get_creature(self, index: int):
        return self.creatures[index]

    def get_all(self):
        return self.creatures