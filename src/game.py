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
import os


class Game:
    def __init__(self, ecran):
        self.fps_regulator = IAFPS(FPS_base)
        self.continuer = 1
        self.ecran = ecran
        self.current_rendering = RENDER_GAME
        self.last_rendering = RENDER_GAME

        #Managers
        self.carte_mgr = carte.CarteManager(self.ecran)
        self.inventaire = inventaire.Inventaire(self.ecran)
        self.indexeur = indexer.Indexer(self.ecran)
        self.tab_types = tab_types.Storage()

        #Entités
        self.personnage = personnage.Personnage(self.ecran, self.carte_mgr)

        #Contrôles
        self.controles = {
            HAUT: K_UP,
            BAS: K_DOWN,
            GAUCHE: K_LEFT,
            DROITE: K_RIGHT,
            INVENTAIRE: K_RSHIFT,
            MENU: K_ESCAPE,
            SCREENSCHOT: K_F5
        }

        self.load()

    def load(self):
        self.carte_mgr.load()
        self.personnage.load()
        self.inventaire.load()
        self.indexeur.load()
        self.tab_types.init_tab()

    def save(self):
        self.carte_mgr.save()
        self.personnage.save()
        self.inventaire.save()
        self.indexeur.save()

    def screenschot(self):
        pygame.image.save(self.ecran, os.path.join("..", "screenschots", str(len(glob(os.path.join("..", "screenschots", "*.png")))) + ".png"))

    def process_events(self, events, dt=1):
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
                        self.screenschot()

    def process_events_menu_in_game(self, event, dt):
        raise NotImplementedError

    def process_events_boutique(self, event, dt):
        raise NotImplementedError

    def process_events_combat(self, event, dt):
        raise NotImplementedError

    def process_events_inventaire(self, event, dt):
        if event.type == KEYDOWN:
            if event.key == self.controles[INVENTAIRE]:
                tmp = self.last_rendering
                self.last_rendering = self.current_rendering
                self.current_rendering = tmp

    def process_events_game(self, event, dt):
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
        #Variables ayant besoin d'être rechargés avant le lancement du jeu (en cas de lancement multiple du jeu)
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
            #FPS
            self.fps_regulator.actualise()
            dt = self.fps_regulator.get_DeltaTime()

            #Evénements
            self.process_events(pygame.event.get(), dt)

            #Affichage
            self.render()

            pygame.display.flip()

        self.save()