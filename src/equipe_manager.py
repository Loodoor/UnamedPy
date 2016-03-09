# coding=utf-8

from creatures_mgr import Creature
import pickle
from constantes import *


class EquipeManager:
    def __init__(self, ecran: pygame.Surface, police: pygame.font.SysFont, indexer, render_manager, size: int=6):
        self.size = size
        self.ecran = ecran
        self.police = police
        self.creatures = []
        self.indexer = indexer
        self.path = os.path.join("..", "saves", "equipe" + EXTENSION)
        self.titre = self.police.render("Equipe", 1, (255, 255, 255))
        self.rd_mgr = render_manager
        self.selected_crea = -1
        self.pc = None
        self.fond = pygame.image.load(os.path.join("..", "assets", "gui", "fd_creatures.png")).convert_alpha()
        self._fond_case = pygame.image.load(os.path.join("..", "assets", "gui", "fd_case_creature.png")).convert_alpha()
        self._fond_case_selected = pygame.image.load(os.path.join("..", "assets", "gui", "fd_case_creature_selected.png")).convert_alpha()
        self._btn_pc = pygame.image.load(os.path.join("..", "assets", "gui", "fd_bouton_pc.png")).convert_alpha()
        self._btn_to_pc = pygame.image.load(os.path.join("..", "assets", "gui", "fd_bouton_to_pc.png")).convert_alpha()

    def get_selected_creature(self) -> Creature:
        if self.selected_crea != -1:
            return self.creatures[self.selected_crea]
        return None

    def is_a_creature_selected(self):
        return self.get_selected_creature() is not None

    def update(self):
        self.render()

    def render(self):
        self.ecran.blit(self.fond, (FCREA_X, FCREA_Y))
        self.ecran.blit(self.titre, ((FEN_large - self.titre.get_width()) // 2, FCREA_TITRE_Y))
        for i in range(len(self.creatures)):
            creature = self.creatures[i]
            pvs_format = self.police.render(str(creature.get_pvs()) + '/' + str(creature.get_max_pvs()), 1, (10, 10, 10))
            txt_format = self.police.render(creature.get_pseudo() + ' : niv.' + str(creature.get_niv()), 1, (10, 10, 10))
            if i == self.selected_crea:
                self.ecran.blit(self._fond_case_selected, (FCREA_X + FCREA_MARGE_X,
                                                           FCREA_Y + FCREA_SIZE_Y_CASE * i + FCREA_MARGE_Y * (i + 1) + FCREA_MARGE_Y_RAPPORT_TITRE))
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
                             FCREA_Y + FCREA_IMAGE_Y + (i + 1) * FCREA_MARGE_Y + i * FCREA_SIZE_Y_CASE + FCREA_MARGE_Y_RAPPORT_TITRE - FCREA_IMAGE_XY_MARGE))
        # boutons
        self.ecran.blit(self._btn_pc, (FCREA_AUTRE_MGR_X, FCREA_AUTRE_MGR_Y))
        self.ecran.blit(self._btn_to_pc, (FCREA_PASSE_CREA_TO__X, FCREA_PASSE_CREA_TO__Y))

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "rb") as equipe_rb:
                self.creatures = pickle.Unpickler(equipe_rb).load()

    def save(self):
        with open(self.path, "wb") as equipe_wb:
            pickle.Pickler(equipe_wb).dump(self.creatures)

    def add_pc(self, new_pc):
        self.pc = new_pc

    def change_renderer(self):
        self.rd_mgr.change_without_logging_last(RENDER_PC)

    def clic(self, xp: int, yp: int):
        if FCREA_AUTRE_MGR_X <= xp <= FCREA_AUTRE_MGR_X + FCREA_AUTRE_MGR_SX and FCREA_AUTRE_MGR_Y <= yp <= FCREA_AUTRE_MGR_Y + FCREA_AUTRE_MGR_SY:
            self.change_renderer()
        if FCREA_PASSE_CREA_TO__X <= xp <= FCREA_PASSE_CREA_TO__X + FCREA_PASSE_CREA_TO__SX and \
                FCREA_PASSE_CREA_TO__Y <= yp <= FCREA_PASSE_CREA_TO__Y + FCREA_PASSE_CREA_TO__SY:
            if self.selected_crea != -1:
                self.move_creature_to_pc(self.selected_crea)
        if FCREA_X <= xp <= FCREA_X + FCREA_SIZE_X_CASE and FCREA_Y + FCREA_IMAGE_XY_MARGE <= yp <= \
                FCREA_Y + FCREA_IMAGE_XY_MARGE + FCREA_SIZE_Y_CASE * len(self.creatures) + FCREA_MARGE_Y * \
                (len(self.creatures) + 1) + FCREA_MARGE_Y_RAPPORT_TITRE:
            real_y = yp - FCREA_Y - FCREA_IMAGE_XY_MARGE - FCREA_MARGE_Y_RAPPORT_TITRE
            real_y /= (FCREA_SIZE_Y_CASE + FCREA_MARGE_Y)
            real_y = int(real_y)
            if 0 <= real_y < len(self.creatures):
                self.selected_crea = real_y

    def add_creature(self, new: Creature):
        if len(self.creatures) < self.size:
            self.creatures.append(new)
            return True
        else:
            return self.pc.add_creature(new)

    def move_locals_creatures(self, first: int, second: int):
        self.creatures[first], self.creatures[second] = self.creatures[first] = self.creatures[second]

    def move_creature_to_pc(self, which: int):
        if self.pc.add_creature(self.creatures[which]):
            self.remove_creature(which)

    def remove_creature(self, index: int):
        return self.creatures.pop(index)

    def get_creature(self, index: int):
        return self.creatures[index]

    def get_all(self):
        return self.creatures

    def is_not_empty(self):
        return True if self.creatures else False