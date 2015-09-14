import pygame
from pygame.locals import *
from fpsregulator import IAFPS
from constantes import *
import carte
import personnage
import sys
import inventaire


class Game:
    def __init__(self, ecran):
        self.fps_regulator = IAFPS(FPS_base)
        self.continuer = 1
        self.ecran = ecran

        #Managers
        self.carte_mgr = carte.CarteManager(self.ecran)
        self.inventaire = inventaire.Inventaire(self.ecran)

        #Entités
        self.personnage = personnage.Personnage(self.ecran, self.carte_mgr)

        #Contrôles
        self.controles = {
            HAUT: K_UP,
            BAS: K_DOWN,
            GAUCHE: K_LEFT,
            DROITE: K_RIGHT,
            INVENTAIRE: K_RSHIFT,
            MENU: K_ESCAPE
        }

        self.load()

    def load(self):
        self.carte_mgr.load()
        self.personnage.load()
        self.inventaire.load()

    def save(self):
        self.carte_mgr.save()
        self.personnage.save()

    def process_events(self, events):
        for event in events:
            if event.type == QUIT:
                self.save()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == self.controles[HAUT]:
                    self.personnage.move(HAUT)
                if event.key == self.controles[BAS]:
                    self.personnage.move(BAS)
                if event.key == self.controles[GAUCHE]:
                    self.personnage.move(GAUCHE)
                if event.key == self.controles[DROITE]:
                    self.personnage.move(DROITE)
                if event.key == self.controles[INVENTAIRE]:
                    raise NotImplementedError
                if event.key == self.controles[MENU]:
                    self.continuer = 0
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

        pygame.key.set_repeat(200, 100)

    def render(self):
        self.carte_mgr.update()
        self.personnage.update()

    def start(self):
        self.prepare()

        while self.continuer:
            pygame.display.set_caption(str(self.personnage.get_pos()))
            #FPS
            self.fps_regulator.actualise()
            dt = self.fps_regulator.get_DeltaTime()

            #Affichage
            self.render()

            #Evénements
            self.process_events(pygame.event.get())

            pygame.display.flip()

        self.save()