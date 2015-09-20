import os
import pygame
from pygame.locals import *
from constantes import *
import pickle
import objets_manager


class Inventaire:
    def __init__(self, ecran: pygame.Surface, police: pygame.font.Font):
        self.ecran = ecran
        self.police = police

        self.cur_categorie = POCHE_COMMUNS
        self.selected_item = -1

        self.titre = self.police.render("Inventaire", 1, (10, 10, 10))

        #Objets
        self.objets = [
            [],  # Poche communs
            [],  # Poche capturateurs
            [],  # Poche médicaments
            [],  # Poche Objets Rares
            []   # Poche CT/CS
        ]

    def __quelle_poche(self):
        tmp_poche = ""
        if self.cur_categorie == POCHE_COMMUNS:
            tmp_poche = "Communs"
        elif self.cur_categorie == POCHE_CAPTUREURS:
            tmp_poche = "Captureurs"
        elif self.cur_categorie == POCHE_MEDICAMENTS:
            tmp_poche = "Médicaments"
        elif self.cur_categorie == POCHE_OBJETS_RARES:
            tmp_poche = "Objets Rares"
        elif self.cur_categorie == POCHE_CT_CS:
            tmp_poche = "CT CS"
        else:
            tmp_poche = "ERREUR?"
        return tmp_poche

    def update(self):
        self.render()

    def render(self):
        pygame.draw.rect(self.ecran, (50, 180, 70), (INVENT_POSX, INVENT_POSY, INVENT_X_SIZE, INVENT_Y_SIZE))
        self.ecran.blit(self.titre, (FEN_large // 2 - self.titre.get_size()[0] // 2, 30))
        for i in range(len(self.objets[self.cur_categorie])):
            texte = self.objets[self.cur_categorie][i].name() + ' : ' + str(self.objets[self.cur_categorie][i].tot_quantite())
            item = self.police.render(texte, 1, (10, 10, 10))
            self.ecran.blit(item, (INVENT_X_ITEM, INVENT_Y_ITEM + i * INVENT_ESP_ITEM))
        if 0 <= self.selected_item < len(self.objets[self.cur_categorie]):
            # les boutons jeter et jeter tout
            pygame.draw.rect(self.ecran, (180, 50, 50), (INVENT_BTN_JETER_X, INVENT_BTN_JETER_Y, INVENT_SIZE_BTN_X, INVENT_SIZE_BTN_Y))
            pygame.draw.rect(self.ecran, (255, 50, 50), (INVENT_BTN_JETERTT_X, INVENT_BTN_JETERTT_Y, INVENT_SIZE_BTN_X, INVENT_SIZE_BTN_Y))
            # texte d'aide
            self.ecran.blit(self.police.render(self.objets[self.cur_categorie][self.selected_item].aide(), 1, (255, 255, 255)), (INVENT_TXT_AIDE_X, INVENT_TXT_AIDE_Y))

        # image de la poche
        pygame.draw.rect(self.ecran, (0, 0, 255), (INVENT_IMAGE_X, INVENT_IMAGE_Y, INVENT_IMAGE_SIZE, INVENT_IMAGE_SIZE))

        # les boutons next & previous
        pygame.draw.rect(self.ecran, (180, 75, 180), (INVENT_BTN_PREVIOUS, INVENT_BTN_PAGES, INVENT_BTN_PAGES_SX, INVENT_BTN_PAGES_SY))
        pygame.draw.rect(self.ecran, (180, 75, 180), (INVENT_BTN_NEXT, INVENT_BTN_PAGES, INVENT_BTN_PAGES_SX, INVENT_BTN_PAGES_SY))

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
                self.jeter(self.selected_item)
            elif INVENT_BTN_JETERTT_Y <= yp <= INVENT_BTN_JETERTT_Y + INVENT_SIZE_BTN_Y and \
                        INVENT_BTN_JETERTT_X <= xp <= INVENT_BTN_JETERTT_X + INVENT_SIZE_BTN_X:
                # DEMANDER CONFIRMATION AVANT !
                self.jeter_tout(self.selected_item)
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

    def jeter(self, item: int):
        if item != -1:
            self.objets[self.cur_categorie][item].jeter()

    def jeter_tout(self, item: int):
        if item != -1:
            self.objets[self.cur_categorie][item].jeter_tout()

    def load(self):
        if os.path.exists(os.path.join("..", "saves", "inventaire" + EXTENSION)):
            with open(os.path.join("..", "saves", "inventaire" + EXTENSION), "rb") as read_inventaire:
                self.objets = pickle.Unpickler(read_inventaire).load()
        else:
            anti_para = objets_manager.Objet("Anti-Para", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test anti para"))
            anti_brul = objets_manager.Objet("Anti-Brûle", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test anti brule"))
            anti_poison = objets_manager.Objet("Anti-Poison", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test anti poison"))
            att_p = objets_manager.Objet("Attaque+", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test attaque"))
            def_p = objets_manager.Objet("Défense+", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test defense"))
            vit_p = objets_manager.Objet("Vitesse+", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test vitesse"))
            pps_p = objets_manager.Objet("PP+", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test pps"))
            regen_pps_5 = objets_manager.Objet("Elixir", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pps 5"))
            regen_pps_10 = objets_manager.Objet("Elixir Augmenté", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pps 10"))
            regen_pps_30 = objets_manager.Objet("Super Elixir", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pps 30"))
            regen_pps_75 = objets_manager.Objet("Hyper Elixir", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pps 75"))
            regen_pps_max = objets_manager.Objet("Elixir Max", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pps max"))
            pvs_p = objets_manager.Objet("PV+", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test pvs"))
            regen_pvs_20 = objets_manager.Objet("Potion Simple", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pvs 20"))
            regen_pvs_60 = objets_manager.Objet("Super Potion", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pvs 60"))
            regen_pvs_100 = objets_manager.Objet("Hyper Potion", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pvs 100"))
            regen_pvs_200 = objets_manager.Objet("Mega Potion", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pvs 200"))
            regen_pvs_max = objets_manager.Objet("Potion Max", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pvs max"))
            chaussures = objets_manager.Objet("Chaussures", "AIDE", [1, 1], objets_manager.ObjectAction(print, "test chaussures"))
            velo = objets_manager.Objet("Velo", "AIDE", [0, 1], objets_manager.ObjectAction(print, "test velo"))

            self.objets = [
                [

                ],  # Poche communs
                [

                ],  # Poche capturateurs
                [
                    anti_para,
                    anti_brul,
                    anti_poison,
                    att_p,
                    def_p,
                    vit_p,
                    pps_p,
                    regen_pps_5,
                    regen_pps_10,
                    regen_pps_30,
                    regen_pps_75,
                    regen_pps_max,
                    pvs_p,
                    regen_pvs_20,
                    regen_pvs_60,
                    regen_pvs_100,
                    regen_pvs_200,
                    regen_pvs_max
                ],  # Poche médicaments
                [
                    velo,
                    chaussures
                ],  # Poche Objets Rares
                [

                ]   # Poche CT/CS
            ]

    def save(self):
        with open(os.path.join("..", "saves", "inventaire" + EXTENSION), "wb") as wrb_inventaire:
            pickle.Pickler(wrb_inventaire).dump(self.objets)