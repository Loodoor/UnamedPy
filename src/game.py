import os
import pygame
from pygame.locals import *
from fpsregulator import IAFPS
from constantes import *
import carte
import personnage


class Game:
    def __init__(self, ecran):
        self.fps_regulator = IAFPS(FPS_base)
        self.continuer = 1
        self.ecran = ecran

        #Managers
        self.carte_mgr = carte.CarteManager(self.ecran)

        #Entités
        self.personnage = personnage.Personnage(self.ecran)

        self.load()

    def load(self):
        pass

    def save(self):
        self.carte_mgr.save()

    def process_events(self, events):
        for event in events:
            if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
                self.continuer = 0

    def prepare(self):
        #Variables ayant besoin d'être rechargés avant le lancement du jeu (en cas de lancement multiple du jeu)
        self.continuer = 1

        pygame.key.set_repeat(200, 100)

    def render(self):
        pygame.draw.rect(self.ecran, (55, 178, 25), (0, 0) + self.ecran.get_size())
        self.carte_mgr.update()
        self.personnage.update()

    def start(self):
        self.prepare()
        print("Working !")

        while self.continuer:
            #Evénements
            self.process_events(pygame.event.get())

            #FPS
            self.fps_regulator.actualise()
            dt = self.fps_regulator.get_DeltaTime()

            #Affichage
            self.render()

            pygame.display.flip()

        self.save()