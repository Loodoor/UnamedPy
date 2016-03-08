# coding=utf-8

from constantes import *


class Menu:
    def __init__(self, ecran: pygame.Surface, police: pygame.font.Font) -> None:
        self.ecran = ecran
        self.police = police
        self.select = 0
        self.categories = [
            MENU_CREATURES,
            MENU_SAC,
            MENU_CARTE,
            MENU_SAUV,
            MENU_POKEDEX,
            MENU_QUITTER
        ]
        self.fond = pygame.image.load(os.path.join("..", "assets", "gui", "fd_menu.png")).convert_alpha()
        self.fond_cat = pygame.image.load(os.path.join("..", "assets", "gui", "fd_categorie_menu.png")).convert_alpha()
        self.fond_cat_sel = pygame.image.load(os.path.join("..", "assets", "gui", "fd_categorie_selected_menu.png")).convert_alpha()

    def update(self):
        self.render()

    def render(self):
        self.ecran.blit(self.fond, (MENU_X, MENU_Y))
        self.render_categories()

    def render_categories(self):
        if self.categories[0] != self.select:
            self.ecran.blit(self.fond_cat, (MENU_X + MENU_X_CAT, MENU_Y + MENU_Y_CAT))
        else:
            self.ecran.blit(self.fond_cat_sel, (MENU_X + MENU_X_CAT, MENU_Y + MENU_Y_CAT))
        self.ecran.blit(self.police.render("Créatures", 1, (255, 255, 255)), (MENU_X + MENU_TXT_CAT_X + MENU_X_CAT,
                                                                              MENU_Y + MENU_TXT_CAT_Y + MENU_Y_CAT))

        if self.categories[1] != self.select:
            self.ecran.blit(self.fond_cat, (MENU_X + MENU_X_CAT * 2 + MENU_SIZE_X_CAT, MENU_Y + MENU_Y_CAT))
        else:
            self.ecran.blit(self.fond_cat_sel, (MENU_X + MENU_X_CAT * 2 + MENU_SIZE_X_CAT, MENU_Y + MENU_Y_CAT))
        self.ecran.blit(self.police.render("Inventaire", 1, (255, 255, 255)),
                        (MENU_X + MENU_TXT_CAT_X + MENU_X_CAT * 2 + MENU_SIZE_X_CAT,
                         MENU_Y + MENU_TXT_CAT_Y + MENU_Y_CAT))

        if self.categories[2] != self.select:
            self.ecran.blit(self.fond_cat, (MENU_X + MENU_X_CAT * 2 + MENU_SIZE_X_CAT, MENU_Y + MENU_Y_CAT * 2 + MENU_SIZE_Y_CAT))
        else:
            self.ecran.blit(self.fond_cat_sel, (MENU_X + MENU_X_CAT * 2 + MENU_SIZE_X_CAT, MENU_Y + MENU_Y_CAT * 2 + MENU_SIZE_Y_CAT))
        self.ecran.blit(self.police.render("Carte", 1, (255, 255, 255)),
                        (MENU_X + MENU_TXT_CAT_X + MENU_X_CAT * 2 + MENU_SIZE_X_CAT,
                         MENU_Y + MENU_TXT_CAT_Y + MENU_Y_CAT * 2 + MENU_SIZE_Y_CAT))

        if self.categories[3] != self.select:
            self.ecran.blit(self.fond_cat, (MENU_X + MENU_X_CAT, MENU_Y + MENU_Y_CAT * 2 + MENU_SIZE_Y_CAT))
        else:
            self.ecran.blit(self.fond_cat_sel, (MENU_X + MENU_X_CAT, MENU_Y + MENU_Y_CAT * 2 + MENU_SIZE_Y_CAT))
        self.ecran.blit(self.police.render("Sauvegarder", 1, (255, 255, 255)),
                        (MENU_X + MENU_TXT_CAT_X + MENU_X_CAT,
                         MENU_Y + MENU_TXT_CAT_Y + MENU_Y_CAT * 2 + MENU_SIZE_Y_CAT))

        if self.categories[4] != self.select:
            self.ecran.blit(self.fond_cat, (MENU_X + MENU_X_CAT, MENU_Y + MENU_Y_CAT * 3 + MENU_SIZE_Y_CAT * 2))
        else:
            self.ecran.blit(self.fond_cat_sel, (MENU_X + MENU_X_CAT, MENU_Y + MENU_Y_CAT * 3 + MENU_SIZE_Y_CAT * 2))
        self.ecran.blit(self.police.render("Indexer", 1, (255, 255, 255)),
                        (MENU_X + MENU_TXT_CAT_X + MENU_X_CAT,
                         MENU_Y + MENU_TXT_CAT_Y + MENU_Y_CAT * 3 + MENU_SIZE_Y_CAT * 2))

        if self.categories[5] != self.select:
            self.ecran.blit(self.fond_cat, (MENU_X + MENU_X_CAT * 2 + MENU_SIZE_X_CAT, MENU_Y + MENU_Y_CAT * 3 + MENU_SIZE_Y_CAT * 2))
        else:
            self.ecran.blit(self.fond_cat_sel, (MENU_X + MENU_X_CAT * 2 + MENU_SIZE_X_CAT, MENU_Y + MENU_Y_CAT * 3 + MENU_SIZE_Y_CAT * 2))
        self.ecran.blit(self.police.render("Retour", 1, (255, 255, 255)),
                        (MENU_X + MENU_TXT_CAT_X + MENU_X_CAT + MENU_X_CAT * 2 + MENU_SIZE_X_CAT,
                         MENU_Y + MENU_TXT_CAT_Y + MENU_Y_CAT * 3 + MENU_SIZE_Y_CAT * 2))

    def next(self):
        self.select = self.select + 1 if self.select + 1 < len(self.categories) else 0

    def previous(self):
        self.select = self.select - 1 if self.select > 0 else len(self.categories) - 1

    def valider_choix(self):
        if self.select == MENU_SAC:
            work = RENDER_INVENTAIRE
        elif self.select == MENU_SAUV:
            work = RENDER_SAVE
        elif self.select == MENU_QUITTER:
            work = RENDER_GAME
        elif self.select == MENU_CARTE:
            work = RENDER_CARTE
        elif self.select == MENU_CREATURES:
            work = RENDER_CREATURES
        elif self.select == MENU_POKEDEX:
            work = RENDER_POKEDEX
        else:
            work = RENDER_ERROR

        return work

    def clic(self, xp: int, yp: int):
        real_x, real_y = (xp - MENU_X) // MENU_SIZE_X_CAT, (yp - MENU_Y) // MENU_SIZE_Y_CAT
        if (real_x, real_y) == (0, 0):
            self.select = MENU_CREATURES
        if (real_x, real_y) == (1, 0):
            self.select = MENU_SAC
        if (real_x, real_y) == (0, 1):
            self.select = MENU_SAUV
        if (real_x, real_y) == (1, 1):
            self.select = MENU_CARTE
        if (real_x, real_y) == (0, 2):
            self.select = MENU_POKEDEX
        if (real_x, real_y) == (1, 2):
            self.select = MENU_QUITTER
        return self.valider_choix()

    def mouseover(self, pos: tuple):
        real_x = (pos[0] - MENU_X) // MENU_SIZE_X_CAT
        real_y = (pos[1] - MENU_Y) // (MENU_SIZE_Y_CAT + MENU_Y_CAT)

        if (real_x, real_y) == (0, 0):
            self.select = MENU_CREATURES
        if (real_x, real_y) == (1, 0):
            self.select = MENU_SAC
        if (real_x, real_y) == (0, 1):
            self.select = MENU_SAUV
        if (real_x, real_y) == (1, 1):
            self.select = MENU_CARTE
        if (real_x, real_y) == (0, 2):
            self.select = MENU_POKEDEX
        if (real_x, real_y) == (1, 2):
            self.select = MENU_QUITTER