# coding=utf-8

from constantes import *
import pickle
import objets_manager
import textwrap as tw
from glob import glob
import debug


class Inventaire:
    def __init__(self, ecran: pygame.Surface, police: pygame.font.Font, carte):
        self.ecran = ecran
        self.police = police
        self.carte = carte
        self.xp, self.yp = 0, 0
        self.path = os.path.join("..", "saves", "inventaire" + EXTENSION)
        self.cur_categorie = POCHE_COMMUNS
        self.selected_item = -1
        self.titre = self.police.render("Inventaire", 1, (10, 10, 10))
        self.textes = {
            "jeter": self.police.render("Jeter", 1, (10, 10, 10)),
            "jeter tout": self.police.render("Vider", 1, (10, 10, 10)),
            "utiliser": self.police.render("Utiliser", 1, (10, 10, 10))
        }
        self._opened_from = None
        self.obj_messenger = None

        # Objets
        self.objets = [[], [], [], [], []]

        # Poches
        self.images_poches = {
            os.path.split(image_path)[1].split('.')[0]: pygame.image.load(image_path).convert_alpha() for image_path in glob(
                os.path.join("..", "assets", "inventaire", "poches", "*.png")
            )
        }

        self.fond = pygame.image.load(os.path.join("..", "assets", "gui", "fd_inventaire.png")).convert_alpha()

    def get_obj_messenger(self):
        if self.obj_messenger:
            return self.obj_messenger
        return None

    def clear_obj_messenger(self):
        self.obj_messenger = None

    def open(self, from_: int):
        self._opened_from = from_

    def close(self):
        self._opened_from = None

    def find_object(self, obj: list):
        self.objets[obj[1]].append(obj[0])

    @staticmethod
    def create_inventory_and_store(objs: list):
        tmp_path = os.path.join("..", "saves", "inventaire" + EXTENSION)
        with open(tmp_path, 'wb') as inventaire_wb:
            pickle.Pickler(inventaire_wb).dump(objs)

    def __quelle_poche(self):
        if self.cur_categorie == POCHE_COMMUNS:
            tmp_poche = "Communs"
        elif self.cur_categorie == POCHE_CAPTUREURS:
            tmp_poche = "Captureurs"
        elif self.cur_categorie == POCHE_MEDICAMENTS:
            tmp_poche = "Médicaments"
        elif self.cur_categorie == POCHE_OBJETS_RARES:
            tmp_poche = "Objets Rares"
        elif self.cur_categorie == POCHE_CT_CS:
            tmp_poche = "CT & CS"
        else:
            tmp_poche = "ERREUR?"
        return tmp_poche

    def update(self, pos_perso: tuple):
        self.xp, self.yp = pos_perso
        self.render()

    def render(self):
        self.ecran.blit(self.fond, (INVENT_POSX, INVENT_POSY))
        self.ecran.blit(self.titre, (FEN_large // 2 - self.titre.get_size()[0] // 2, 30))
        for i in range(len(self.objets[self.cur_categorie])):
            if self.objets[self.cur_categorie][i].nombre():
                texte = self.objets[self.cur_categorie][i].name() + ' : ' + str(self.objets[self.cur_categorie][i].tot_quantite())
                item = self.police.render(texte, 1, (10, 10, 10))
                self.ecran.blit(item, (INVENT_X_ITEM, INVENT_Y_ITEM + i * INVENT_ESP_ITEM))
        if 0 <= self.selected_item < len(self.objets[self.cur_categorie]) and self.objets[self.cur_categorie][self.selected_item].nombre():
            # les boutons jeter, jeter tout et utiliser
            pygame.draw.rect(self.ecran, (180, 50, 50), (INVENT_BTN_JETER_X, INVENT_BTN_JETER_Y, INVENT_SIZE_BTN_X, INVENT_SIZE_BTN_Y))
            pygame.draw.rect(self.ecran, (255, 50, 50), (INVENT_BTN_JETERTT_X, INVENT_BTN_JETERTT_Y, INVENT_SIZE_BTN_X, INVENT_SIZE_BTN_Y))
            pygame.draw.rect(self.ecran, (50, 50, 180), (INVENT_BTN_USE_X, INVENT_BTN_USE_Y, INVENT_SIZE_BTN_X, INVENT_SIZE_BTN_Y))
            # et leur texte
            self.ecran.blit(self.textes["jeter"], (INVENT_BTN_JETER_X + 2, INVENT_BTN_JETER_Y + 2))
            self.ecran.blit(self.textes["jeter tout"], (INVENT_BTN_JETERTT_X + 2, INVENT_BTN_JETERTT_Y + 2))
            self.ecran.blit(self.textes["utiliser"], (INVENT_BTN_USE_X + 2, INVENT_BTN_USE_Y + 2))
            # texte d'aide
            # DECOUPER LE TEXTE CAR TROP GRAND !
            texte_aide_str = self.objets[self.cur_categorie][self.selected_item].aide()
            texte_lst = tw.wrap(texte_aide_str, width=37)
            i = 0
            for texte_tmp in texte_lst:
                self.ecran.blit(self.police.render(texte_tmp, 1, (255, 255, 255)),
                                (INVENT_TXT_AIDE_X, INVENT_TXT_AIDE_Y + INVENT_ESP_ITEM * i))
                i += 1

        # image de la poche
        self.ecran.blit(self.images_poches[str(self.cur_categorie)], (INVENT_IMAGE_X, INVENT_IMAGE_Y))

        # les boutons next & previous
        pygame.draw.rect(self.ecran, (180, 180, 50), (INVENT_BTN_PREVIOUS, INVENT_BTN_PAGES, INVENT_BTN_PAGES_SX, INVENT_BTN_PAGES_SY))
        pygame.draw.rect(self.ecran, (180, 180, 50), (INVENT_BTN_NEXT, INVENT_BTN_PAGES, INVENT_BTN_PAGES_SX, INVENT_BTN_PAGES_SY))
        self.ecran.blit(self.police.render("<", 1, (10, 10, 10)), (INVENT_BTN_PREVIOUS + 6, INVENT_BTN_PAGES))
        self.ecran.blit(self.police.render(">", 1, (10, 10, 10)), (INVENT_BTN_NEXT + 6, INVENT_BTN_PAGES))

        # texte de la poche
        tmp_poche = self.__quelle_poche()
        poche_txt = self.police.render(tmp_poche, 1, (255, 255, 255))
        self.ecran.blit(poche_txt, (INVENT_TXT_POCHE_X - poche_txt.get_size()[0] // 2, INVENT_TXT_POCHE_Y))

    def clic(self, xp: int, yp: int):
        real_y = (yp - INVENT_Y_ITEM) // INVENT_ESP_ITEM
        if INVENT_X_ITEM <= xp <= INVENT_MAX_X_ITEM and 0 <= real_y < len(self.objets[self.cur_categorie]):
            self.selected_item = real_y
        else:
            if INVENT_BTN_JETER_Y <= yp <= INVENT_BTN_JETER_Y + INVENT_SIZE_BTN_Y and \
                    INVENT_BTN_JETER_X <= xp <= INVENT_BTN_JETER_X + INVENT_SIZE_BTN_X:
                # DEMANDER CONFIRMATION AVANT !
                debug.println("besoin de confirmation")
                self.jeter(self.selected_item)
            elif INVENT_BTN_JETERTT_Y <= yp <= INVENT_BTN_JETERTT_Y + INVENT_SIZE_BTN_Y and \
                    INVENT_BTN_JETERTT_X <= xp <= INVENT_BTN_JETERTT_X + INVENT_SIZE_BTN_X:
                # DEMANDER CONFIRMATION AVANT !
                debug.println("besoin de confirmation")
                self.jeter_tout(self.selected_item)
            elif INVENT_BTN_USE_Y <= yp <= INVENT_BTN_USE_Y + INVENT_SIZE_BTN_Y and \
                    INVENT_BTN_USE_X <= xp <= INVENT_BTN_USE_X + INVENT_SIZE_BTN_X:
                self.utiliser(self.selected_item)
            elif INVENT_BTN_PREVIOUS <= xp <= INVENT_BTN_PREVIOUS + INVENT_BTN_PAGES_SX and \
                    INVENT_BTN_PAGES <= yp <= INVENT_BTN_PAGES + INVENT_BTN_PAGES_SY:
                self.previous()
            elif INVENT_BTN_NEXT <= xp <= INVENT_BTN_NEXT + INVENT_BTN_PAGES_SX and \
                    INVENT_BTN_PAGES <= yp <= INVENT_BTN_PAGES + INVENT_BTN_PAGES_SY:
                self.next()

    def next(self):
        self.cur_categorie = self.cur_categorie + 1 if self.cur_categorie + 1 < len(self.objets) else 0

    def previous(self):
        self.cur_categorie = self.cur_categorie - 1 if self.cur_categorie - 1 >= 0 else len(self.objets) - 1

    def utiliser(self, item: int):
        if item != -1:
            object_used = self.objets[self.cur_categorie][item].use()
            if object_used:
                self.obj_messenger = objets_manager.ObjectMessenger(
                    depuis={
                        "name": "NA",
                        "renderer": self._opened_from
                    },
                    pour={
                        "name": "NA",
                        "renderer": object_used["on"]
                    },
                    objet=object_used
                )

    def jeter(self, item: int):
        if item != -1:
            objet = self.objets[self.cur_categorie][item].jeter()
            if objet != GLOBAL_ERROR:
                self.carte.drop_object_at(self.xp - TILE_SIZE, self.yp, objet,
                                          self.cur_categorie)
            del self.objets[self.cur_categorie][item]

    def jeter_tout(self, item: int):
        if item != -1:
            self.carte.drop_object_at(self.xp - TILE_SIZE, self.yp, self.objets[self.cur_categorie][item].jeter_tout(),
                                      self.cur_categorie)
            del self.objets[self.cur_categorie][item]

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "rb") as read_inventaire:
                self.objets = pickle.Unpickler(read_inventaire).load()

    def save(self):
        with open(self.path, "wb") as wrb_inventaire:
            pickle.Pickler(wrb_inventaire).dump(self.objets)