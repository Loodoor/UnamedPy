import pygame
from pygame.locals import *
from fpsregulator import IAFPS
from constantes import *
from glob import glob
import carte
import personnage
import sys
import inventaire
import indexer
import captureurs
import tab_types
import objets_manager
import os


class Game:
    def __init__(self, ecran: pygame.Surface):
        self.fps_regulator = IAFPS(FPS_base)
        self.continuer = 1
        self.ecran = ecran
        self.current_rendering = RENDER_GAME
        self.last_rendering = RENDER_GAME

        # Polices
        self.police_normale = pygame.font.SysFont("arial", POL_NORMAL_TAILLE)
        self.police_gras = pygame.font.SysFont("arial", POL_NORMAL_TAILLE, bold=True)
        self.police_italique = pygame.font.SysFont("arial", POL_NORMAL_TAILLE, italic=True)
        self.police_grande = pygame.font.SysFont("arial", POL_GRANDE_TAILLE)
        self.police_petite = pygame.font.SysFont("arial", POL_PETITE_TAILLE)

        # Managers
        self.carte_mgr = carte.CarteManager(self.ecran)
        self.inventaire = inventaire.Inventaire(self.ecran, self.police_grande)
        self.indexeur = indexer.Indexer(self.ecran)
        self.tab_types = tab_types.Storage()

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
            NEXT_PAGE: K_RIGHT,
            PREVIOUS_PAGE: K_LEFT
        }

        self.load()

    def load(self):
        self.carte_mgr.load()
        self.personnage.load()
        #self.inventaire.load()
        #self.indexeur.load()
        self.tab_types.init_tab()
        self.create_objects()

    def save(self):
        self.carte_mgr.save()
        self.personnage.save()
        self.inventaire.save()
        self.indexeur.save()

    def create_objects(self):
        self.att_p = objets_manager.Objet("Attaque+", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test attaque"))
        self.def_p = objets_manager.Objet("Défense+", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test defense"))
        self.vit_p = objets_manager.Objet("Vitesse+", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test vitesse"))
        self.pps_p = objets_manager.Objet("PP+", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test pps"))
        self.regen_pps_5 = objets_manager.Objet("Elixir", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pps 5"))
        self.regen_pps_10 = objets_manager.Objet("Elixir Augmenté", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pps 10"))
        self.regen_pps_30 = objets_manager.Objet("Super Elixir", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pps 30"))
        self.regen_pps_75 = objets_manager.Objet("Hyper Elixir", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pps 75"))
        self.regen_pps_max = objets_manager.Objet("Elixir Max", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pps max"))
        self.pvs_p = objets_manager.Objet("PV+", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test pvs"))
        self.regen_pvs_20 = objets_manager.Objet("Potion Simple", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pvs 20"))
        self.regen_pvs_60 = objets_manager.Objet("Super Potion", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pvs 60"))
        self.regen_pvs_100 = objets_manager.Objet("Hyper Potion", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pvs 100"))
        self.regen_pvs_200 = objets_manager.Objet("Mega Potion", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pvs 200"))
        self.regen_pvs_max = objets_manager.Objet("Potion Max", "AIDE", [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pvs max"))
        self.chaussures = objets_manager.Objet("Chaussures", "AIDE", [1, 1], objets_manager.ObjectAction(print, "test chaussures"))
        self.velo = objets_manager.Objet("Velo", "AIDE", [0, 1], objets_manager.ObjectAction(print, "test velo"))

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

            # Global
            if event.type == KEYDOWN:
                if event.key == self.controles[MENU]:
                        self.continuer = 0
            if event.type == KEYUP:
                if event.key == self.controles[SCREENSCHOT]:
                        self.screenshot()

    def process_events_menu_in_game(self, event: pygame.event, dt: int=1):
        raise NotImplementedError

    def process_events_boutique(self, event: pygame.event, dt: int=1):
        raise NotImplementedError

    def process_events_combat(self, event: pygame.event, dt: int=1):
        raise NotImplementedError

    def process_events_inventaire(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.controles[INVENTAIRE]:
                tmp = self.last_rendering
                self.last_rendering = self.current_rendering
                self.current_rendering = tmp
            if event.key == self.controles[NEXT_PAGE]:
                self.inventaire.next()
            if event.key == self.controles[PREVIOUS_PAGE]:
                self.inventaire.previous()
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos
            self.inventaire.clic(xp, yp)

    def process_events_game(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.controles[HAUT]:
                self.personnage.move(HAUT, dt)
            if event.key == self.controles[BAS]:
                self.personnage.move(BAS, dt)
            if event.key == self.controles[GAUCHE]:
                self.personnage.move(GAUCHE, dt)
            if event.key == self.controles[DROITE]:
                self.personnage.move(DROITE, dt)
            if event.key == self.controles[INVENTAIRE]:
                self.last_rendering = self.current_rendering
                self.current_rendering = RENDER_INVENTAIRE
        if event.type == KEYUP:
            if event.key == self.controles[HAUT]:
                self.personnage.end_move()
            if event.key == self.controles[BAS]:
                self.personnage.end_move()
            if event.key == self.controles[GAUCHE]:
                self.personnage.end_move()
            if event.key == self.controles[DROITE]:
                self.personnage.end_move()

    def prepare(self):
        # Variables ayant besoin d'être rechargés avant le lancement du jeu (en cas de lancement multiple du jeu)
        self.continuer = 1
        self.current_rendering = RENDER_GAME
        self.last_rendering = RENDER_GAME

        self.load()
        pygame.key.set_repeat(200, 100)

    def render(self):
        if self.current_rendering == RENDER_GAME:
            self.carte_mgr.update()
            self.personnage.update()
        elif self.current_rendering == RENDER_INVENTAIRE:
            self.inventaire.update()
        elif self.current_rendering == RENDER_BOUTIQUE:
            raise NotImplementedError
        elif self.current_rendering == RENDER_COMBAT:
            raise NotImplementedError
        elif self.current_rendering == RENDER_MENU_IN_GAME:
            raise NotImplementedError

    def start(self):
        self.prepare()

        while self.continuer:
            # FPS
            self.fps_regulator.actualise()
            dt = self.fps_regulator.get_DeltaTime()

            # Evénements
            self.process_events(pygame.event.get(), dt)

            # Affichage
            self.render()

            pygame.display.flip()

        self.save()