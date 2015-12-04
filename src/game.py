# coding=utf-8

import pygame
from pygame.locals import *
from fpsregulator import IAFPS
from exceptions import FonctionnaliteNonImplementee
from constantes import *
from glob import glob
import carte
import personnage
import renderer_manager as rd_mgr
from gui import GUISauvegarde
import sys
import os

import indexer
import money_mgr
import tab_types
import equipe_manager
import atk_sys
import menu_in_game
import computer_manager
import zones_attaques_manager


class Game:
    def __init__(self, ecran: pygame.Surface, controles: dict={}):
        # self.fps_regulator = IAFPS(FPS_base)
        self.fps_regulator = pygame.time.Clock()
        self.continuer = 1
        self.ecran = ecran
        self.renderer_manager = rd_mgr.RendererManager()
        self.show_fps = False

        self.right = False
        self.left = False
        self.top = False
        self.bottom = False

        # Polices
        self.police_normale = pygame.font.Font(POLICE_PATH, POL_NORMAL_TAILLE)
        self.police_grande = pygame.font.Font(POLICE_PATH, POL_GRANDE_TAILLE)
        self.police_petite = pygame.font.Font(POLICE_PATH, POL_PETITE_TAILLE)

        # Managers
        self.carte_mgr = carte.CartesManager(self.ecran, self.renderer_manager)
        self.indexeur = indexer.Indexer(self.ecran, self.police_grande, self.renderer_manager)
        self.equipe_mgr = equipe_manager.EquipeManager(self.ecran, self.police_grande, self.indexeur, self.renderer_manager)
        self.pc_mgr = computer_manager.ComputerManager(self.ecran, self.police_grande, self.renderer_manager)
        self.tab_types = tab_types.Storage()
        self.cur_combat = None
        self.menu_in_game = menu_in_game.Menu(self.ecran, self.police_grande)
        self.zones_manager = zones_attaques_manager.ZonesManager(self.indexeur)
        self.money = money_mgr.MoneyManager()
        self.gui_save_mgr = GUISauvegarde(self.ecran, self.police_grande)

        # Entités
        self.personnage = personnage.Personnage(self.ecran, self.carte_mgr, self.police_grande)

        # Contrôles
        self.controles = {
            HAUT: K_UP,
            BAS: K_DOWN,
            GAUCHE: K_LEFT,
            DROITE: K_RIGHT,
            INVENTAIRE: K_RSHIFT,
            MENU: K_ESCAPE,
            SCREENSCHOT: K_F5,
            SHOW_FPS: K_BACKSPACE,
            VALIDATION: K_RETURN
        }
        self.controles.update(controles)
        self.controles_joy = {

        }
        controles = {}  # vider le dico à chaque fois !

        self.__ctrls = {
            NEXT_PAGE: K_RIGHT,
            PREVIOUS_PAGE: K_LEFT
        }

        self.load()

    def load(self):
        self.carte_mgr.load()
        self.personnage.load()
        self.indexeur.load()
        self.equipe_mgr.load()
        self.pc_mgr.load()
        self.zones_manager.load()
        self.money.load()

        self.tab_types.init_tab()

    def save(self):
        print("Sauvegarde ...")
        self.carte_mgr.save()
        self.personnage.save()
        # self.money.save()
        # self.indexeur.save()
        # self.equipe_mgr.save()
        # self.pc_mgr.save()
        # self.zones_manager.save()

    def screenshot(self):
        path = os.path.join("..", "screenshots", str(len(glob(os.path.join("..", "screenshots", "*.png")))) + ".png")
        pygame.image.save(self.ecran, path)
        print("Screenshot sauvegardée sous '" + path + "'")

    def process_events(self, events: pygame.event, dt: int=1):
        for event in events:
            if event.type == QUIT:
                self.save()
                sys.exit()

            # Différents mode de gestion des événements
            if self.renderer_manager.get_renderer() == RENDER_GAME:
                # le jeu en lui même
                self.process_events_game(event, dt)
            elif self.renderer_manager.get_renderer() == RENDER_INVENTAIRE:
                # l'inventaire
                self.process_events_inventaire(event, dt)
            elif self.renderer_manager.get_renderer() == RENDER_COMBAT:
                # quand on est en combat
                self.process_events_combat(event, dt)
            elif self.renderer_manager.get_renderer() == RENDER_BOUTIQUE:
                # dans une boutique
                self.process_events_boutique(event, dt)
            elif self.renderer_manager.get_renderer() == RENDER_MENU_IN_GAME:
                # le menu intermédiaire
                self.process_events_menu_in_game(event, dt)
            elif self.renderer_manager.get_renderer() == RENDER_SAVE:
                # la sauvegarde
                self.process_events_save(event, dt)
            elif self.renderer_manager.get_renderer() == RENDER_CARTE:
                # la mini carte
                self.process_events_carte(event, dt)
            elif self.renderer_manager.get_renderer() == RENDER_CREATURES:
                # quand on consulte ses creatures
                self.process_events_creatures(event, dt)
            elif self.renderer_manager.get_renderer() == RENDER_PC:
                # quand on est sur un PC pour gérer ses creatures
                self.process_events_pc(event, dt)
            elif self.renderer_manager.get_renderer() == RENDER_POKEDEX:
                # le pokedex
                self.process_events_pokedex(event, dt)
            elif self.renderer_manager.get_renderer() == RENDER_ERROR:
                # autre ...
                raise FonctionnaliteNonImplementee("Cas non géré. Merci de reporter ce traceback à Folaefolc, main dev d'Unamed")

            # Global
            if event.type == KEYUP:
                if event.key == self.controles[SCREENSCHOT]:
                    self.screenshot()
                if event.key == self.controles[SHOW_FPS]:
                    self.show_fps = not self.show_fps

    def process_events_carte(self, event: pygame.event, dt: int=1):
        """
        if event.type == KEYDOWN:
            if event.key == self.controles[MENU]:
                self.invert_rendering()
        """
        raise FonctionnaliteNonImplementee

    def process_events_save(self, event: pygame.event, dt: int=1):
        pass

    def process_events_pokedex(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.controles[MENU]:
                self.renderer_manager.invert_renderer()
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos
            self.indexeur.clic(xp, yp)

    def process_events_pc(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.controles[MENU]:
                self.renderer_manager.invert_renderer()
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos
            self.pc_mgr.clic(xp, yp)

    def process_events_menu_in_game(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.controles[MENU]:
                self.renderer_manager.invert_renderer()
            if event.key == self.__ctrls[NEXT_PAGE]:
                self.menu_in_game.next()
            if event.key == self.__ctrls[PREVIOUS_PAGE]:
                self.menu_in_game.previous()
            if event.key == self.controles[VALIDATION]:
                new_renderer = self.menu_in_game.valider_choix()
                self.renderer_manager.change_renderer_for(new_renderer)
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos
            tmp = self.menu_in_game.clic(xp, yp)
            if tmp != RENDER_ERROR:
                self.renderer_manager.change_renderer_for(tmp)

        self.menu_in_game.mouseover(pygame.mouse.get_pos())

    def process_events_creatures(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.controles[MENU]:
                self.renderer_manager.invert_renderer()
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos
            self.equipe_mgr.clic(xp, yp)

    def process_events_boutique(self, event: pygame.event, dt: int=1):
        raise FonctionnaliteNonImplementee

    def process_events_combat(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            pass
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos

    def process_events_inventaire(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.controles[INVENTAIRE] or event.key == self.controles[MENU]:
                self.renderer_manager.invert_renderer()
            if event.key == self.__ctrls[NEXT_PAGE]:
                self.personnage.inventaire_next()
            if event.key == self.__ctrls[PREVIOUS_PAGE]:
                self.personnage.inventaire_previous()
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos
            self.personnage.inventaire_clic(xp, yp)

    def process_events_game(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.controles[HAUT]:
                self.top, self.bottom = True, False
            if event.key == self.controles[BAS]:
                self.top, self.bottom = False, True
            if event.key == self.controles[GAUCHE]:
                self.left, self.right = True, False
            if event.key == self.controles[DROITE]:
                self.left, self.right = False, True
            if event.key == self.controles[INVENTAIRE]:
                self.renderer_manager.change_renderer_for(RENDER_INVENTAIRE)
            if event.key == self.controles[MENU]:
                self.renderer_manager.change_renderer_for(RENDER_MENU_IN_GAME)
        if event.type == KEYUP:
            if event.key == self.controles[HAUT]:
                self.top = False
                self.personnage.end_move()
            if event.key == self.controles[BAS]:
                self.bottom = False
                self.personnage.end_move()
            if event.key == self.controles[GAUCHE]:
                self.left = False
                self.personnage.end_move()
            if event.key == self.controles[DROITE]:
                self.right = False
                self.personnage.end_move()
        self.move_perso(dt)

    def move_perso(self, dt: int=1):
        if self.top:
            self.personnage.move(HAUT, dt)
        if self.bottom:
            self.personnage.move(BAS, dt)
        if self.right:
            self.personnage.move(DROITE, dt)
        if self.left:
            self.personnage.move(GAUCHE, dt)

    def prepare(self):
        # Variables ayant besoin d'être rechargés avant le lancement du jeu (en cas de lancement multiple du jeu)
        self.continuer = 1

        self.renderer_manager.clear_all()
        self.renderer_manager.ban_renderer(RENDER_COMBAT)

        self.pc_mgr.add_equipe(self.equipe_mgr)
        self.equipe_mgr.add_pc(self.pc_mgr)

        self.load()
        pygame.key.set_repeat(200, 100)

    def render(self, dt: int=1):
        self.carte_mgr.update() if self.renderer_manager.can_i_render() else None

        if self.renderer_manager.get_renderer() == RENDER_GAME:
            self.personnage.update()
        elif self.renderer_manager.get_renderer() == RENDER_INVENTAIRE:
            self.personnage.inventaire_update()
        elif self.renderer_manager.get_renderer() == RENDER_BOUTIQUE:
            raise FonctionnaliteNonImplementee
        elif self.renderer_manager.get_renderer() == RENDER_COMBAT:
            if self.equipe_mgr.is_not_empty() and not self.cur_combat:
                self.cur_combat = atk_sys.Combat(self.ecran, self.equipe_mgr.get_creature(0), self.zones_manager,
                                                 self.carte_mgr.get_zid(), self.indexeur, self.police_normale)
                self.cur_combat.find_adv()
                self.top, self.bottom, self.right, self.left = [False] * 4
            if self.cur_combat and not self.cur_combat.is_finished():
                self.cur_combat.update()
            if not self.cur_combat.is_finished():
                self.renderer_manager.invert_renderer()
        elif self.renderer_manager.get_renderer() == RENDER_MENU_IN_GAME:
            self.menu_in_game.update()
        elif self.renderer_manager.get_renderer() == RENDER_SAVE:
            if not self.gui_save_mgr.is_saving():
                self.gui_save_mgr.start_saving(firstcall=self.save, callback=self.renderer_manager.invert_renderer)
            self.gui_save_mgr.update()
            if self.gui_save_mgr.is_saved_finished():
                self.gui_save_mgr.reinit()
        elif self.renderer_manager.get_renderer() == RENDER_CARTE:
            raise FonctionnaliteNonImplementee
        elif self.renderer_manager.get_renderer() == RENDER_CREATURES:
            self.equipe_mgr.update()
        elif self.renderer_manager.get_renderer() == RENDER_POKEDEX:
            self.indexeur.update()
        elif self.renderer_manager.get_renderer() == RENDER_PC:
            self.pc_mgr.update()

        if self.show_fps:
            self.ecran.blit(self.police_normale.render(str(self.fps_regulator.get_fps()), 1, (0, 0, 0)), (10, 10))

    def start(self):
        self.prepare()

        while self.continuer:
            # FPS
            # self.fps_regulator.actualise() ; dt = self.fps_regulator.get_DeltaTime()
            dt = self.fps_regulator.tick(FPS_base)

            # Evénements
            self.process_events(pygame.event.get(), dt)

            # Affichage
            self.render(dt)

            pygame.display.flip()

        self.save()