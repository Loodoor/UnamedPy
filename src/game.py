import pygame
from pygame.locals import *
from fpsregulator import IAFPS
from exceptions import FonctionnaliteNonImplementee
from constantes import *
from glob import glob
import carte
import personnage
import sys
import os

import inventaire
import indexer
import captureurs
import creatures_mgr
import tab_types
import objets_manager
import equipe_manager
import atk_sys
import menu_in_game
import computer_manager
import pnj_manager


class Game:
    def __init__(self, ecran: pygame.Surface, controles: dict={}):
        # self.fps_regulator = IAFPS(FPS_base)
        self.fps_regulator = pygame.time.Clock()
        self.continuer = 1
        self.ecran = ecran
        self.current_rendering = RENDER_GAME
        self.last_rendering = RENDER_GAME
        self.show_fps = False

        self.right = False
        self.left = False
        self.top = False
        self.bottom = False

        # Polices
        self.police_normale = pygame.font.SysFont("arial", POL_NORMAL_TAILLE)
        self.police_gras = pygame.font.SysFont("arial", POL_NORMAL_TAILLE, bold=True)
        self.police_italique = pygame.font.SysFont("arial", POL_NORMAL_TAILLE, italic=True)
        self.police_grande = pygame.font.SysFont("arial", POL_GRANDE_TAILLE)
        self.police_petite = pygame.font.SysFont("arial", POL_PETITE_TAILLE)

        # Managers
        self.carte_mgr = carte.CarteManager(self.ecran)
        self.inventaire = inventaire.Inventaire(self.ecran, self.police_grande)
        self.indexeur = indexer.Indexer(self.ecran, self.police_grande)
        self.equipe_mgr = equipe_manager.EquipeManager(self.ecran, self.police_grande)
        self.pc_mgr = computer_manager.ComputerManager(self.ecran, self.police_grande)
        self.tab_types = tab_types.Storage()
        self.cur_combat = None
        self.menu_in_game = menu_in_game.Menu(self.ecran, self.police_grande)

        # Entités
        self.personnage = personnage.Personnage(self.ecran, self.carte_mgr)

        # Contrôles
        self.controles = {
            HAUT: K_UP,
            BAS: K_DOWN,
            GAUCHE: K_LEFT,
            DROITE: K_RIGHT,
            INVENTAIRE: K_RSHIFT,
            MENU: K_ESCAPE,
            SCREENSCHOT: K_F5,
            SHOW_FPS: K_BACKSPACE
        } if not controles else controles

        self.__ctrls = {
            NEXT_PAGE: K_RIGHT,
            PREVIOUS_PAGE: K_LEFT
        }

        self.load()

    def load(self):
        self.carte_mgr.load()
        self.personnage.load()
        self.inventaire.load()
        self.indexeur.load()
        self.equipe_mgr.load()
        self.pc_mgr.load()

        self.tab_types.init_tab()

        self.pnj = pnj_manager.PNJ(self.ecran, self.carte_mgr, (64, 64), pnj_manager.STANDART_MOVE, self.police_grande)

    def save(self):
        print("Sauvegarde ...")
        self.carte_mgr.save()
        self.personnage.save()
        #self.inventaire.save()
        #self.indexeur.save()
        #self.equipe_mgr.save()
        #self.pc_mgr.save()

    def invert_rendering(self):
        tmp = self.last_rendering
        self.last_rendering = self.current_rendering
        self.current_rendering = tmp

    def screenshot(self):
        pygame.image.save(self.ecran, os.path.join("..", "screenshots", str(len(glob(os.path.join("..", "screenshots", "*.png")))) + ".png"))
        print("Screenshot sauvegardée")

    def process_events(self, events: pygame.event, dt: int=1):
        for event in events:
            if event.type == QUIT:
                self.save()
                sys.exit()

            # Différents mode de gestion des événements
            if self.current_rendering == RENDER_GAME:
                self.process_events_game(event, dt)
            elif self.current_rendering == RENDER_INVENTAIRE:
                self.process_events_inventaire(event, dt)
            elif self.current_rendering == RENDER_COMBAT:
                self.process_events_combat(event, dt)
            elif self.current_rendering == RENDER_BOUTIQUE:
                self.process_events_boutique(event, dt)
            elif self.current_rendering == RENDER_MENU_IN_GAME:
                self.process_events_menu_in_game(event, dt)
            elif self.current_rendering == RENDER_SAVE:
                self.process_events_save(event, dt)
            elif self.current_rendering == RENDER_CARTE:
                self.process_events_carte(event, dt)
            elif self.current_rendering == RENDER_CREATURES:
                self.process_events_creatures(event, dt)
            elif self.current_rendering == RENDER_PC:
                self.process_events_pc(event, dt)
            elif self.current_rendering == RENDER_POKEDEX:
                self.process_events_pokedex(event, dt)
            elif self.current_rendering == RENDER_ERROR:
                raise FonctionnaliteNonImplementee("Cas non géré. Merci de repoter ce traceback à Folaefolc, main dev d'Unamed")

            # Global
            if event.type == KEYUP:
                if event.key == self.controles[SCREENSCHOT]:
                    self.screenshot()
                if event.key == self.controles[SHOW_FPS]:
                    self.show_fps = not self.show_fps

    def process_events_carte(self, event: pygame.event, dt: int=1):
        raise FonctionnaliteNonImplementee

    def process_events_save(self, event: pygame.event, dt: int=1):
        raise FonctionnaliteNonImplementee

    def process_events_pokedex(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.controles[MENU]:
                self.invert_rendering()

    def process_events_pc(self, event: pygame.event, dt: int=1):
        raise FonctionnaliteNonImplementee

    def process_events_menu_in_game(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.controles[MENU]:
                self.invert_rendering()
            if event.key == K_RIGHT:
                self.menu_in_game.next()
            if event.key == K_UP:
                self.menu_in_game.double_next()
            if event.key == K_LEFT:
                self.menu_in_game.previous()
            if event.key == K_DOWN:
                self.menu_in_game.double_previous()
            if event.key == K_RETURN:
                self.last_rendering = self.current_rendering
                new_renderer = self.menu_in_game.valider_choix()
                self.current_rendering = new_renderer
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos
            tmp = self.menu_in_game.clic(xp, yp)
            if tmp != RENDER_ERROR:
                self.last_rendering = self.current_rendering
                self.current_rendering = tmp

    def process_events_creatures(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.invert_rendering()
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos

    def process_events_boutique(self, event: pygame.event, dt: int=1):
        raise FonctionnaliteNonImplementee

    def process_events_combat(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            pass
        if event.type == KEYUP:
            pass
        if event.type == MOUSEBUTTONDOWN:
            xp, yp = event.pos
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos

    def process_events_inventaire(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.controles[INVENTAIRE] or event.key == self.controles[MENU]:
                self.invert_rendering()
            if event.key == self.__ctrls[NEXT_PAGE]:
                self.inventaire.next()
            if event.key == self.__ctrls[PREVIOUS_PAGE]:
                self.inventaire.previous()
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos
            self.inventaire.clic(xp, yp)

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
                self.last_rendering = self.current_rendering
                self.current_rendering = RENDER_INVENTAIRE
            if event.key == self.controles[MENU]:
                self.last_rendering = self.current_rendering
                self.current_rendering = RENDER_MENU_IN_GAME
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
        self.current_rendering = RENDER_GAME
        self.last_rendering = RENDER_GAME

        self.load()
        pygame.key.set_repeat(200, 100)

    def render(self, dt: int=1):
        self.carte_mgr.update()
        if self.current_rendering == RENDER_GAME:
            self.personnage.update()
            self.pnj.update(dt)  # c'était un test
        elif self.current_rendering == RENDER_INVENTAIRE:
            self.inventaire.update()
        elif self.current_rendering == RENDER_BOUTIQUE:
            raise FonctionnaliteNonImplementee
        elif self.current_rendering == RENDER_COMBAT:
            self.cur_combat = atk_sys.Combat(self.ecran, creatures_mgr.Creature("", T_NORMAL))
            raise FonctionnaliteNonImplementee
        elif self.current_rendering == RENDER_MENU_IN_GAME:
            self.menu_in_game.update()
        elif self.current_rendering == RENDER_SAVE:
            self.save()
            self.invert_rendering()
            print("Erreur future à corriger ici (fct render dans game.py)")
        elif self.current_rendering == RENDER_CARTE:
            raise FonctionnaliteNonImplementee
        elif self.current_rendering == RENDER_CREATURES:
            self.equipe_mgr.update()
        elif self.current_rendering == RENDER_POKEDEX:
            self.indexeur.update()
        elif self.current_rendering == RENDER_PC:
            self.pc_mgr.update()

        if self.show_fps:
            self.ecran.blit(self.police_italique.render(str(self.fps_regulator.get_fps()), 1, (255, 150, 150)), (0, 0))

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